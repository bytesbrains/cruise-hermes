# AGENT.md — guidance for agents working in this repository

## What this is

Public **Hermes Agent** client for [BytesBrains Cruise](https://bytesbrains.com/cruise): a
model-provider plugin (`kind: model-provider`) that registers Cruise so `hermes model`,
`hermes doctor`, and sessions route through the gateway.

Cruise holds provider keys, project budgets, and the cost ledger. This repo only ships the Hermes
side: present a `cru_` key to a Cruise base URL and project Cruise’s catalogue into Hermes models.

**Status:** repository bootstrapped; plugin not shipped yet. Track work in GitHub Issues.

## Commands

There is no package or test entry point yet. Until the plugin lands:

- Read [README.md](README.md) for intended install shape and demo-host rehearsal.
- Do not invent a `package.json`, Makefile, or CI job unless the change explicitly scaffolds the
  plugin (see issue #1).

When the plugin exists, document install / build / test commands here and keep them in sync with
the README.

## Conventions a change must honour

- **Never commit a Cruise key** (`cru_live_…`, `cru_demo_…`, `cru_test_…`, `cru_svc_…`) or any
  provider credential. Keys live in the environment or a secret manager.
- **No telemetry, no second host.** Traffic only to the configured Cruise base URL.
- Keep the tree **public-safe**. Do not paste internal gateway design, private trackers, or
  unpublished roadmap. Public product behaviour (base URL, key shapes, `/v1/models`, refusal
  codes) is fine.
- Model ids are **Cruise ids** from `GET /v1/models` for the presented key — never invent
  upstream provider ids. Prefer lanes (`bb/…`) over pinned models unless a pin is required.
- Branch Cruise refusals on `error.code` (`budget_exhausted`, `wallet_exhausted`,
  `measurement_stale`, …), not on HTTP status alone.
- Open changes as pull requests against `main`. Do not force-push or delete `main`.
- Match sister Cruise clients ([openclaw-cruise](https://github.com/bytesbrains/openclaw-cruise),
  [cruise-n8n](https://github.com/bytesbrains/cruise-n8n)) for security and key-handling tone;
  Hermes-specific plugin layout follows NousResearch’s model-provider plugin contract.

## Layout

| Path | Role |
| --- | --- |
| `README.md` | Product pitch, intended install, demo rehearsal |
| `SECURITY.md` | Private vulnerability disclosure |
| `AGENT.md` | This file — agent conventions |
| `.github/workflows/wrokin-hunter.yml` | Advisory security hunter (does not block merges) |
| `LICENSE` | BytesBrains proprietary client license |

Plugin sources (`plugin.yaml`, provider code, tests) are not in-tree yet — see issue #1.

## Open work

See GitHub issues: scaffold the plugin (#1), verify against the demo (#2), document install/env
(#3), register Hermes in Cruise docs (#4).
