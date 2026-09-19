# AGENT.md — guidance for agents working in this repository

## What this is

Public **Hermes Agent** client for [BytesBrains Cruise](https://bytesbrains.com/cruise): a
model-provider plugin (`kind: model-provider`) that registers Cruise so `hermes model`,
`hermes doctor`, and sessions route through the gateway.

Cruise holds provider keys, project budgets, and the cost ledger. This repo only ships the Hermes
side: present a `cru_` key to a Cruise base URL and project Cruise’s catalogue into Hermes models.

## Commands

Two install paths ship the same provider:

- **PyPI:** [`bytesbrains-cruise-hermes`](https://pypi.org/project/bytesbrains-cruise-hermes/)
  (`pip install bytesbrains-cruise-hermes` + `plugins.enabled: [cruise]`)
- **Git:** `hermes plugins install bytesbrains/cruise-hermes` clones this repo into
  `$HERMES_HOME/plugins/cruise-hermes/` (`plugin.yaml` + root `__init__.py` shim +
  `cruise_hermes/` package)

Both register via the `hermes_agent.plugins` / model-provider discovery path
(`cruise` → `cruise_hermes`).

```sh
# Throwaway Hermes home — does not touch ~/.hermes
export HERMES_HOME=$HOME/.hermes/cache/scratch/cruise-hermes-test
mkdir -p "$HERMES_HOME/plugins/model-providers/cruise"
cp plugin.yaml __init__.py "$HERMES_HOME/plugins/model-providers/cruise/"
cp -R cruise_hermes "$HERMES_HOME/plugins/model-providers/cruise/"
export CRUISE_API_KEY=cru_demo_…   # real demo key
export CRUISE_BASE_URL=https://cruise-demo.bytesbrains.net/v1
hermes doctor
hermes model
```

```sh
# Local wheel (optional) — or install the published package
python -m pip install build
python -m build
pip install dist/bytesbrains_cruise_hermes-*.whl
# published: pip install bytesbrains-cruise-hermes
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
  `fallback_models` in `cruise_hermes/__init__.py` is an offline seed only; do not grow it
  into a frozen catalogue.
- Branch Cruise refusals on `error.code` (`budget_exhausted`, `wallet_exhausted`,
  `measurement_stale`, …), not on HTTP status alone.
- Keep `plugin.yaml` and a root `__init__.py` shim at the **repo root** (required for
  `hermes plugins install`). Put the real profile in `cruise_hermes/`. Do not nest under
  `plugins/model-providers/` in this repo — that path is only for drop-in copies under
  `$HERMES_HOME`.
- Keep `[project].version` in `pyproject.toml` aligned with `plugin.yaml` `version` and
  with `v*` tags used by `.github/workflows/publish-pypi.yml`.
- Open changes as pull requests against `main`. Do not force-push or delete `main`.
- Match sister Cruise clients ([openclaw-cruise](https://github.com/bytesbrains/openclaw-cruise),
  [cruise-n8n](https://github.com/bytesbrains/cruise-n8n)) for security and key-handling tone;
  Hermes-specific layout follows NousResearch’s model-provider plugin contract.

## Layout

| Path | Role |
| --- | --- |
| `plugin.yaml` | Manifest (`kind: model-provider`) for `hermes plugins install` |
| `__init__.py` | Thin shim — imports `cruise_hermes` for git/drop-in installs |
| `cruise_hermes/` | Package: `register_provider(ProviderProfile(...))` + pip entry point |
| `pyproject.toml` | PyPI package [`bytesbrains-cruise-hermes`](https://pypi.org/project/bytesbrains-cruise-hermes/) + entry point `cruise` |
| `README.md` | Product pitch, install, demo rehearsal |
| `SECURITY.md` | Private vulnerability disclosure |
| `AGENT.md` | This file — agent conventions |
| `.github/workflows/wrokin-hunter.yml` | Advisory security hunter (does not block merges) |
| `.github/workflows/publish-pypi.yml` | Publish wheel/sdist on `v*` tags (Trusted Publisher) |
| `LICENSE` | BytesBrains proprietary client license |

## Open work

See GitHub issues: register Hermes in Cruise docs (#4).
