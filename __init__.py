"""BytesBrains Cruise — Hermes model-provider plugin.

Registers Cruise as an OpenAI-compatible chat-completions backend. Hermes holds
only a ``cru_`` project key; provider credentials, budgets, and the cost ledger
stay on the gateway. Live model ids come from ``GET /v1/models`` for the
presented key — ``fallback_models`` is an offline seed only.

Install, env, model ids, refusals, and demo → production switch: see README.md
(ships with ``hermes plugins install bytesbrains/cruise-hermes``).
"""

from __future__ import annotations

from providers import register_provider
from providers.base import ProviderProfile

# Offline seeds for the picker when the live catalogue is unreachable.
# Prefer lanes; never invent upstream provider ids (gpt-4o, …).
_FALLBACK_MODELS = (
    "bb/agentic-coding",
    "bb/chat-assistant",
    "bb/code-review",
    "bb/summarization",
    "bb/extraction",
    "bb/translation",
    "bb/deep-reasoning",
    "bb/code-completion",
)

cruise = ProviderProfile(
    name="cruise",
    aliases=("bytesbrains-cruise", "bb-cruise"),
    display_name="BytesBrains Cruise",
    description="Cruise — OpenAI-compatible gateway with budgets and a cost ledger",
    signup_url="https://bytesbrains.com/cruise",
    env_vars=("CRUISE_API_KEY", "CRUISE_BASE_URL"),
    base_url="https://cruise.bytesbrains.net/v1",
    api_mode="chat_completions",
    auth_type="api_key",
    # Cheap lane for compression / summarization; live resolve may replace this.
    default_aux_model="bb/summarization",
    fallback_models=_FALLBACK_MODELS,
)

register_provider(cruise)
