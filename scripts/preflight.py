#!/usr/bin/env python3
"""Read-only portable inventory: no installs, downloads, secret values or browser launch."""
import sys, json, platform, importlib.util, shutil, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # works under python -I
from pathlib import Path
from khaam_paths import config, models_dir, sfx_library, resolve, executable, toolkit_dir, elevenlabs_key, onboarding as read_onboarding, workspace, KEY_FILE, SKILL, GLOBAL_SKILL, installed_folder, same_path, apple_stub, clt_present, TOOLS
try: config()
except (ValueError, OSError) as e: raise SystemExit('Invalid local configuration: '+str(e))
def probe(path, args):
    if not path: return {'available': False, 'reason': 'not found'}
    try:
        p=subprocess.run([path]+args, capture_output=True, text=True, timeout=15)
        text=(p.stdout or p.stderr).strip()
        return {'available': p.returncode==0 and bool(text), 'exit_code':p.returncode, 'version':text.splitlines()[0] if text else ''}
    except (OSError, subprocess.TimeoutExpired) as e: return {'available':False, 'reason':type(e).__name__}
binaries={n:executable(n) if n in ['ffmpeg','ffprobe'] else shutil.which(n) for n in ['ffmpeg','ffprobe','node','npm','git']}
# 1.7.1, macOS: Apple's /usr/bin/git (and python3) open Apple's install window while the developer tools are missing: never run them
STUB={'available':False,'reason':"Apple's developer tools are not installed; running it would open Apple's install window"}
checks={n:(dict(STUB) if apple_stub(p) else probe(p, ['-version'] if n in ['ffmpeg','ffprobe'] else ['--version'])) for n,p in binaries.items()}
checks['python']={'available':True,'version':sys.version.split()[0],'supported':sys.version_info>=(3,9),'minimum':'3.9'}  # one floor (1.7.1): checked under 3.9
node=checks['node']; node['minimum']='18'
try: node['supported']=node['available'] and int(node['version'].lstrip('v').split('.')[0])>=18
except (ValueError,KeyError): node['supported']=False
im=shutil.which('magick') or shutil.which('montage')
checks['imagemagick']=dict(probe(im,['-version']),optional=True,path=im)
toolkit=toolkit_dir()
# Resolve Playwright from the selected project/toolkit, never via npx/network.
js="""const {createRequire}=require('node:module'),fs=require('node:fs'),path=require('node:path');
try {const req=createRequire(path.join(process.argv[1],'package.json'));const pw=req('playwright');
const browser=process.env.KHAAM_CHROMIUM || pw.chromium.executablePath();
console.log(JSON.stringify({package_available:true,browser_path:browser,browser_file_exists:fs.existsSync(browser),launch_tested:false}));}
catch(e){console.log(JSON.stringify({package_available:false,browser_file_exists:false,launch_tested:false,reason:e.code||e.name}));}"""
browser={'package_available':False,'browser_file_exists':False,'launch_tested':False,'reason':'Node unavailable or unsupported'}
if node['supported']:
    try:
        p=subprocess.run([binaries['node'],'-e',js,str(toolkit or Path.cwd())],capture_output=True,text=True,timeout=15)
        browser=json.loads(p.stdout) if p.returncode==0 else dict(browser,reason='Node probe failed')
    except (OSError,ValueError,subprocess.TimeoutExpired): browser['reason']='Browser probe failed'
r={'platform':platform.system(),'python':sys.version.split()[0],'current_python':sys.executable,'models_dir':str(models_dir()),'sfx_library':str(sfx_library()),'sfx_catalog_exists':(sfx_library()/'catalog.json').is_file(),'configured_audio_python':str(resolve('audio_python','KHAAM_AUDIO_PYTHON') or ''),'configured_toolkit':str(toolkit or ''),'binaries':binaries,'checks':checks,'playwright_chromium':browser,'packages_in_current_python':{}}
for n in ['numpy','scipy','librosa','soundfile','torch','transformers','panns_inference','conette','PIL']:
    try:r['packages_in_current_python'][n]=importlib.util.find_spec(n) is not None
    except (ImportError,ValueError):r['packages_in_current_python'][n]=False
onboarding=read_onboarding()
_key,_source=elevenlabs_key()
r.update(elevenlabs_key_present=bool(_key),elevenlabs_key_source=_source,elevenlabs_key_file=str(KEY_FILE),onboarding=onboarding,user_taste_exists=(Path.home()/'.cache'/'khaam-motion'/'user-taste.md').is_file())
del _key
# The workspace (scripts/workspace.py): where it is and whether its memory files exist.
ws=workspace()
r['workspace']={'recorded':bool(isinstance(onboarding,dict) and onboarding.get('workspace')),'path':str(ws) if ws else None,
                'exists':bool(ws),'handoff':bool(ws and (ws/'SESSION_HANDOFF.md').is_file()),'claude_md':bool(ws and (ws/'CLAUDE.md').is_file())}
# Where this skill runs from. Since 1.6 it lives in the user's folder; a global copy would load everywhere and hide updates.
_folder=installed_folder()
r['skill']={'dir':str(SKILL),'scope':'folder' if _folder else ('global' if same_path(SKILL,GLOBAL_SKILL) else 'other'),
            'folder':str(_folder) if _folder else None,
            'global_copy':str(GLOBAL_SKILL) if GLOBAL_SKILL.is_dir() and not same_path(GLOBAL_SKILL,SKILL) else None}
# Optional tools: yt-dlp (references from a link) and Node 22+ (HyperFrames).
yt=shutil.which('yt-dlp')
if yt: r['yt_dlp']=probe(yt,['--version'])
else:
    p=subprocess.run([sys.executable,'-m','yt_dlp','--version'],capture_output=True,text=True,timeout=30) if importlib.util.find_spec('yt_dlp') else None
    r['yt_dlp']={'available':bool(p and p.returncode==0),'version':(p.stdout.strip() if p else ''),'via':'python -m yt_dlp' if p else None}
try: _major=int(checks['node']['version'].lstrip('v').split('.')[0]) if checks['node'].get('available') else 0
except ValueError: _major=0
r['hyperframes']={'node_major':_major,'node_ok':_major>=22,'minimum_node':22,'pinned':'hyperframes@0.8.225','note':'Runs through npx; the first render downloads the CLI and its Chrome.'}
# Optional creative package files in this skill checkout. Presence is not a runtime or render test.
_creative = SKILL / 'integrations' / 'creative'
_creative_cache = SKILL / '.cache' / 'creative-tools'
r['optional_creative_tools'] = {
    'three_package_present': (_creative / 'node_modules' / 'three' / 'package.json').is_file(),
    'pixelfx_package_present': (_creative / 'node_modules' / 'pixelfx' / 'package.json').is_file(),
    'react_three_rapier_present': (_creative / 'node_modules' / '@react-three' / 'rapier' / 'package.json').is_file(),
    'react_postprocessing_present': (_creative / 'node_modules' / '@react-three' / 'postprocessing' / 'package.json').is_file(),
    'audio_env_present': (_creative_cache / 'audio-env' / 'pyvenv.cfg').is_file(),
    'shotcraft_source_present': (_creative_cache / 'video-shotcraft' / '.khaam-revision').is_file(),
    'awesome_opus_references_present': (_creative_cache / 'references' / 'awesome-opus5-5-videos' / '.khaam-revision').is_file(),
    'opus_prompts_references_present': (_creative_cache / 'references' / 'opus-video-prompts' / '.khaam-revision').is_file(),
    'lemo_source_present': (_creative_cache / 'lemo-opuscar' / '.khaam-revision').is_file(),
    'blender_mcp_env_present': any((_creative_cache / 'blender-env' / p).is_file() for p in ('bin/mcp-for-blender', 'Scripts/mcp-for-blender.exe')),
    'render_tested': False, 'note': 'File presence only; cache and node_modules may be absent after a reset.'
}
# Optional Blender tools: PATH discovery only. Do not launch Blender, connect to MCP or change settings.
_blender = shutil.which('blender')
_uv = shutil.which('uv')
_uvx = shutil.which('uvx')
r['optional_blender'] = {
    'blender_on_path': bool(_blender), 'blender_path': _blender,
    'uv_on_path': bool(_uv), 'uvx_on_path': bool(_uvx),
    'mcp_connection_tested': False, 'addon_tested': False,
    'note': 'PATH discovery only. Does not detect all installations or establish Blender/MCP readiness.'
}
# The free Khaam sound library (scripts/install_sounds.py): built or not, and how many sounds its catalog lists.
cat=Path.home()/'.cache'/'khaam-motion'/'sfx'/'catalog.json'
try: r['khaam_sound_library']={'installed':cat.is_file(),'sounds':len(json.loads(cat.read_text(encoding='utf-8'))) if cat.is_file() else 0}
except (OSError,ValueError): r['khaam_sound_library']={'installed':False,'unreadable':True}
if sys.platform=='darwin':  # 1.7.1: the Mac route (scripts/mac_tools.sh, reference/mac.md)
    r['mac']={'tools_dir':str(TOOLS),'tools_bin':(TOOLS/'bin').is_dir(),'apple_developer_tools':clt_present(),
              'path_line':'export PATH="$HOME/.cache/khaam-motion/tools/bin:$PATH"',
              'missing_tools':'bash "%s" plan' % (SKILL/'scripts'/'mac_tools.sh'),
              'note':'Start every shell command with path_line. Missing Python, Node 22+, FFmpeg/ffprobe or NumPy/SciPy/Pillow: run missing_tools, ask its ask_user, then its next_command. Never brew, never sudo.'}
r.update(network_used=False,installed_anything=False,note='Inventory only, not an all-ready gate. Browser file presence does not prove launch/GPU readiness; run the starter smoke test. ImageMagick is optional (Pillow/FFmpeg alternatives). Model files are optional; no inference readiness is implied. Keep this machine report local.')
print(json.dumps(r,indent=2))
