#!/usr/bin/env python3
"""Run the pinned upstream animated-diagrams code_to_svg helper compatibly.

The upstream script is preserved unchanged under reference/. Its current
source uses tokenize.FSTRING_START, which is absent in Python 3.11 and earlier.
Those Python versions tokenize an entire f-string as STRING, so a harmless
sentinel preserves the upstream classifier's behavior without editing its code.
"""
from __future__ import annotations

import runpy
import sys
import tokenize
from pathlib import Path


if not hasattr(tokenize, 'FSTRING_START'):
    tokenize.FSTRING_START = object()  # type: ignore[attr-defined]

UPSTREAM = (
    Path(__file__).resolve().parents[1]
    / 'reference'
    / 'animated-diagrams-upstream'
    / 'scripts'
    / 'code_to_svg.py'
)
sys.argv[0] = str(UPSTREAM)
runpy.run_path(str(UPSTREAM), run_name='__main__')
