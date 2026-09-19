"""Hermes ``plugins install`` entry — delegates to the ``cruise_hermes`` package.

``hermes plugins install bytesbrains/cruise-hermes`` clones this repo so the
plugin directory is on ``sys.path``; importing the sibling package registers
Cruise. Pip installs use the ``hermes_agent.plugins`` entry point instead.
"""

from __future__ import annotations

import cruise_hermes as _cruise_hermes  # noqa: F401 — register_provider side effect
