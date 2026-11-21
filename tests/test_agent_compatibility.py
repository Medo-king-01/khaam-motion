import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'workspace.py'


class AgentCompatibilityTest(unittest.TestCase):
    def test_preflight_only_discovers_optional_blender_tools(self):
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ, HOME=home, USERPROFILE=home)
            result = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'preflight.py')],
                                    cwd=home, env=env, capture_output=True, text=True, check=True)
            report = json.loads(result.stdout)
            self.assertFalse(report['network_used'])
            self.assertFalse(report['installed_anything'])
            self.assertFalse(report['optional_blender']['mcp_connection_tested'])
            self.assertFalse(report['optional_blender']['addon_tested'])
            self.assertFalse(report['optional_creative_tools']['render_tested'])
            self.assertIsInstance(report['optional_blender']['blender_on_path'], bool)

    def test_install_resume_and_existing_agent_instructions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            home = root / 'home'
            home.mkdir()
            workspace = root / 'workspace'
            workspace.mkdir()
            agents = workspace / 'AGENTS.md'
            agents.write_text('# Existing instructions\nKeep this.\n', encoding='utf-8')
            global_skill = home / '.claude' / 'skills' / 'khaam-motion'
            global_skill.mkdir(parents=True)
            (global_skill / 'SKILL.md').write_text('existing global skill', encoding='utf-8')
            env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))

            def run(script, *args, cwd=workspace):
                result = subprocess.run([sys.executable, str(script), *map(str, args)],
                                        cwd=cwd, env=env, capture_output=True, text=True, check=True)
                return json.loads(result.stdout)

            plan = run(SCRIPT, '--plan', '--preserve-global', '--path', workspace)
            self.assertTrue(plan['preserve_global'])
            self.assertNotIn('بنقلها', plan['ask_user'])
            result = run(SCRIPT, '--create', '--install-skill', '--preserve-global', '--path', workspace)
            self.assertEqual(result['agents_md'], 'appended')
            self.assertEqual((global_skill / 'SKILL.md').read_text(), 'existing global skill')
            installed = workspace / '.claude' / 'skills' / 'khaam-motion'
            self.assertTrue((installed / 'reference' / 'agent-compatibility.md').is_file())
            self.assertFalse((installed / '.git').exists())
            self.assertFalse((installed / '.khaam').exists())
            text = agents.read_text(encoding='utf-8')
            self.assertIn('Keep this.', text)
            self.assertIn('## Khaam Motion workspace (agent-neutral)', text)
            # Re-creating a workspace must not duplicate its compatibility block.
            again = run(installed / 'scripts' / 'workspace.py', '--create', '--install-skill', '--preserve-global', '--path', workspace)
            self.assertEqual(again['agents_md'], 'present')
            self.assertEqual(agents.read_text(encoding='utf-8'), text)
            where = run(installed / 'scripts' / 'workspace.py', '--where')
            self.assertEqual(where['workspace'], str(workspace))
            video = run(installed / 'scripts' / 'workspace.py', '--new-video', 'Demo', '--slug', 'demo')
            self.assertTrue(video)
            state = run(installed / 'scripts' / 'workspace.py', '--state')
            self.assertIsInstance(state, dict)


if __name__ == '__main__':
    unittest.main()
