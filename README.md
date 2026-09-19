<p align="center">
  <img src="https://bytesbrains.com/brand/cruise-logo-480.png" alt="BytesBrains Cruise" width="280" />
</p>

<h1 align="center">BytesBrains Cruise for Hermes Agent</h1>

<p align="center">
  Every model your Cruise key can reach — as a Hermes model-provider plugin —<br />
  with budgets, per-project keys, and one cost ledger that stay on the gateway.
</p>

<p align="center">
  <a href="https://bytesbrains.com/cruise"><img src="https://img.shields.io/badge/Product-bytesbrains.com%2Fcruise-111111" alt="Product" /></a>
  <a href="https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin"><img src="https://img.shields.io/badge/Hermes-model%20provider%20plugin-555" alt="Hermes docs" /></a>
  <a href="https://github.com/NousResearch/hermes-agent"><img src="https://img.shields.io/badge/Host-NousResearch%2Fhermes--agent-111111" alt="Hermes Agent" /></a>
</p>

---

## What this is

[BytesBrains Cruise](https://bytesbrains.com/cruise) is one OpenAI-compatible endpoint in front of
every model provider. This repository is the **[Hermes Agent](https://github.com/NousResearch/hermes-agent)
client**: a model-provider plugin (`kind: model-provider`) that registers Cruise so `hermes model`,
`hermes doctor`, and sessions route through the gateway.

Your keys, budgets and ledger stay on the gateway. Hermes only holds a `cru_` key and talks to
the base URL you configure.

| | |
| --- | --- |
| **Product** | [bytesbrains.com/cruise](https://bytesbrains.com/cruise) |
| **Source** | [bytesbrains/cruise-hermes](https://github.com/bytesbrains/cruise-hermes) |
| **Host** | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) |
| **Production API** | `https://cruise.bytesbrains.net/v1` |
| **Demo API** | `https://cruise-demo.bytesbrains.net/v1` |

**Status:** model-provider plugin verified against the demo (**2026-09-19 UTC**). See
[Verified against demo](#verified-against-demo) below.

---

## Install

Requires [Hermes Agent](https://github.com/NousResearch/hermes-agent). Prefer the Git install so
`plugin.yaml` lands under `$HERMES_HOME/plugins/`:

```sh
hermes plugins install bytesbrains/cruise-hermes
export CRUISE_API_KEY=cru_demo_…   # or cru_live_…
# optional — defaults to production:
# export CRUISE_BASE_URL=https://cruise.bytesbrains.net/v1
hermes model                       # pick BytesBrains Cruise / a Cruise model id
hermes doctor                      # probes Cruise GET /v1/models with your key
```

Drop-in alternative (same two files, nested path Hermes also scans):

```sh
mkdir -p "$HERMES_HOME/plugins/model-providers/cruise"
cp plugin.yaml __init__.py "$HERMES_HOME/plugins/model-providers/cruise/"
```

| Env | Role |
| --- | --- |
| `CRUISE_API_KEY` | Project key (`cru_demo_…` / `cru_live_…`) |
| `CRUISE_BASE_URL` | Optional override; default `https://cruise.bytesbrains.net/v1` |

### Try it before anyone issues you a live key

Point at the demo with a `cru_demo_` key:

| | |
| --- | --- |
| **API key** | `cru_demo_…` |
| **Base URL** | `https://cruise-demo.bytesbrains.net/v1` |

```sh
export CRUISE_API_KEY=cru_demo_…
export CRUISE_BASE_URL=https://cruise-demo.bytesbrains.net/v1
hermes doctor
hermes model
hermes -z "hello" --provider cruise -m bb/agentic-coding
```

That host holds production’s model ids exactly, every price zero, and **no** provider credential
in the deployment. Answers are fabricated. It costs nothing to rehearse.

Name models as Cruise names them from `GET /v1/models` (e.g. `bb/agentic-coding`), not as the
upstream provider does.

### Verified against demo

**2026-09-19 UTC** — throwaway `HERMES_HOME`, Hermes Agent **v0.21.3**, plugin copied to
`$HERMES_HOME/plugins/cruise-hermes/` (flat install layout), env:

```text
CRUISE_API_KEY=cru_demo_…          # never committed
CRUISE_BASE_URL=https://cruise-demo.bytesbrains.net/v1
```

| Check | Result |
| --- | --- |
| `hermes doctor` | `✓ BytesBrains Cruise` (connectivity / `/models` probe) |
| Live catalogue | `ProviderProfile.fetch_models` ids **equal** `GET /v1/models` (63 ids, incl. `bb/agentic-coding`) |
| Short session | `hermes -z … --provider cruise -m bb/agentic-coding` completed (demo fabricates the body) |
| Plugin-free fallback | `POST /v1/chat/completions` with the same base URL + key returned HTTP 200 |

---

## Works today without this package

Cruise’s data plane is OpenAI-compatible. If Hermes already lets you set an OpenAI-compatible
base URL and key (custom / OpenAI-shaped provider), you can point it at Cruise with two strings
and skip the plugin — same onboarding as any other OpenAI client:

```text
base URL:  https://cruise.bytesbrains.net/v1          # or cruise-demo… for rehearsal
API key:   cru_live_…                                 # or cru_demo_… on the demo host
model:     a Cruise id from GET /v1/models
```

Verified on the demo host on **2026-09-19 UTC** via `POST /v1/chat/completions` (no Hermes plugin).

The plugin’s job is the Hermes-native path: appear in `hermes model`, wire `hermes doctor`,
fetch the live catalogue for your key, and keep setup from becoming a hand-edited config file.

---

## Sister clients

| Host | Repo |
| --- | --- |
| OpenClaw | [bytesbrains/openclaw-cruise](https://github.com/bytesbrains/openclaw-cruise) |
| n8n | [bytesbrains/cruise-n8n](https://github.com/bytesbrains/cruise-n8n) |
| VS Code | [bytesbrains/cruise-vscode](https://github.com/bytesbrains/cruise-vscode) |
| Cursor | [bytesbrains/cruise-cursor-plugin](https://github.com/bytesbrains/cruise-cursor-plugin) |
| Claude Code | [bytesbrains/cruise-claude-plugin](https://github.com/bytesbrains/cruise-claude-plugin) |

---

## License

See [LICENSE](LICENSE).
