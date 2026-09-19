# AGENT.md — guidance for agents working in this repository

## What this is

Public **Hermes Agent** client for [BytesBrains Cruise](https://bytesbrains.com/cruise): a
model-provider plugin (`kind: model-provider`) that registers Cruise so `hermes model`,
`hermes doctor`, and sessions route through the gateway.

Cruise holds provider keys, project budgets, and the cost ledger. This repo only ships the Hermes
side: present a `cru_` key to a Cruise base URL and project Cruise’s catalogue into Hermes models.

## Commands

There is no package build. The plugin is two files at the repo root (`plugin.yaml`,
`__init__.py`) so `hermes plugins install bytesbrains/cruise-hermes` clones a discoverable
layout into `$HERMES_HOME/plugins/cruise-hermes/`.

```sh
# Throwaway Hermes home — does not touch ~/.hermes
export HERMES_HOME=$HOME/.hermes/cache/scratch/cruise-hermes-test
mkdir -p "$HERMES_HOME/plugins/model-providers/cruise"
cp plugin.yaml __init__.py "$HERMES_HOME/plugins/model-providers/cruise/"
export CRUISE_API_KEY=cru_demo_…   # real demo key
export CRUISE_BASE_URL=https://cruise-demo.bytesbrains.net/v1
hermes doctor
hermes model
```

## Conventions a change must honour

- **Never commit a Cruise key** (`cru_live_…`, `cru_demo_…`, `cru_test_…`, `cru_svc_…`) or any
  provider credential. Keys live in the environment or a secret manager.
- **No telemetry, no second host.** Traffic only to the configured Cruise base URL.
- Keep the tree **public-safe**. Do not paste internal gateway design, private trackers, or
  unpublished roadmap. Public product behaviour (base URL, key shapes, `/v1/models`, refusal
  codes) is fine.
- Model ids are **Cruise ids** from `GET /v1/models` for the presented key — never invent
  upstream provider ids. Prefer lanes (`bb/…`) over pinned models unless a pin is required.
  `fallback_models` in `__init__.py` is an offline seed only; do not grow it into a frozen
  catalogue.
- Branch Cruise refusals on `error.code` (`budget_exhausted`, `wallet_exhausted`,
  `measurement_stale`, …), not on HTTP status alone.
- Keep `plugin.yaml` and `__init__.py` at the **repo root** (required for
  `hermes plugins install`). Do not nest them under `plugins/model-providers/` in this repo —
  that path is only for drop-in copies under `$HERMES_HOME`.
- Open changes as pull requests against `main`. Do not force-push or delete `main`.
- Match sister Cruise clients ([openclaw-cruise](https://github.com/bytesbrains/openclaw-cruise),
  [cruise-n8n](https://github.com/bytesbrains/cruise-n8n)) for security and key-handling tone;
  Hermes-specific layout follows NousResearch’s model-provider plugin contract.

## Layout

| Path | Role |
| --- | --- |
| `plugin.yaml` | Manifest (`kind: model-provider`) for `hermes plugins install` |
| `__init__.py` | `register_provider(ProviderProfile(...))` for Cruise |
| `README.md` | Product pitch, install, demo rehearsal |
| `SECURITY.md` | Private vulnerability disclosure |
| `AGENT.md` | This file — agent conventions |
| `.github/workflows/wrokin-hunter.yml` | Advisory security hunter (does not block merges) |
| `LICENSE` | BytesBrains proprietary client license |

## Open work

See GitHub issues: verify against the demo (#2), document install/env polish (#3), register
Hermes in Cruise docs (#4).
