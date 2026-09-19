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
every model provider. This repository will be the **[Hermes Agent](https://github.com/NousResearch/hermes-agent)
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

**Status:** repository bootstrapped; plugin not shipped yet. Track work in
[Issues](https://github.com/bytesbrains/cruise-hermes/issues).

---

## Intended install (once the plugin lands)

Hermes discovers third-party model providers from `$HERMES_HOME/plugins/` or
`hermes plugins install owner/repo` when `plugin.yaml` declares `kind: model-provider`.
Expected shape (subject to change while we build):

```sh
hermes plugins install bytesbrains/cruise-hermes
export CRUISE_API_KEY=cru_demo_…   # or cru_live_…
hermes model                       # pick Cruise / a Cruise model id
hermes doctor
```

Env vars will follow Hermes `ProviderProfile` convention (API key + optional base-URL override),
defaulting to production `https://cruise.bytesbrains.net/v1`.

### Try it before anyone issues you a live key

Point at the demo with a `cru_demo_` key:

| | |
| --- | --- |
| **API key** | `cru_demo_…` |
| **Base URL** | `https://cruise-demo.bytesbrains.net/v1` |

That host holds production’s model ids exactly, every price zero, and **no** provider credential
in the deployment. Answers are fabricated. It costs nothing to rehearse.

Name models as Cruise names them from `GET /v1/models` (e.g. `bb/agentic-coding`), not as the
upstream provider does.

---

## Works today without this package

Cruise’s data plane is OpenAI-compatible. If Hermes already lets you set an OpenAI-compatible
base URL and key (custom / OpenAI-shaped provider), you can point it at Cruise with two strings
and skip the plugin — same onboarding as any other OpenAI client:

```text
base URL:  https://cruise.bytesbrains.net/v1
API key:   cru_live_…
model:     a Cruise id from GET /v1/models
```

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
