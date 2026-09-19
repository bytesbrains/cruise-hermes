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
| **PyPI** | [`bytesbrains-cruise-hermes`](https://pypi.org/project/bytesbrains-cruise-hermes/) |
| **Host** | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) |
| **Production API** | `https://cruise.bytesbrains.net/v1` |
| **Demo API** | `https://cruise-demo.bytesbrains.net/v1` |

**Status:** model-provider plugin verified against the demo (**2026-09-19 UTC**). See
[Verified against demo](#verified-against-demo) below.

---

## Install

Requires [Hermes Agent](https://github.com/NousResearch/hermes-agent).

### Preferred — `hermes plugins install`

```sh
hermes plugins install bytesbrains/cruise-hermes
export CRUISE_API_KEY=cru_demo_…   # or cru_live_…
# optional — defaults to production:
# export CRUISE_BASE_URL=https://cruise.bytesbrains.net/v1
hermes model                       # pick BytesBrains Cruise / a Cruise model id
hermes doctor                      # probes Cruise GET /v1/models with your key
```

### Alternative — pip

Install into the **same Python environment** as Hermes, then opt in (pip plugins are
never loaded until listed under `plugins.enabled`):

```sh
pip install bytesbrains-cruise-hermes
```

```yaml
# ~/.hermes/config.yaml (or $HERMES_HOME/config.yaml)
plugins:
  enabled:
    - cruise
```

```sh
export CRUISE_API_KEY=cru_demo_…   # or cru_live_…
hermes doctor
hermes model
```

### Drop-in copy

Nested path Hermes also scans (copy the package directory, not only the shim):

```sh
mkdir -p "$HERMES_HOME/plugins/model-providers/cruise"
cp plugin.yaml __init__.py "$HERMES_HOME/plugins/model-providers/cruise/"
cp -R cruise_hermes "$HERMES_HOME/plugins/model-providers/cruise/"
```

| Env | Role |
| --- | --- |
| `CRUISE_API_KEY` | Project key (`cru_demo_…` / `cru_live_…`) |
| `CRUISE_BASE_URL` | Optional override; default `https://cruise.bytesbrains.net/v1` |

Put the key in the environment or `$HERMES_HOME/.env` — never in a committed `config.yaml`, never
in a settings sync that copies secrets to another machine.

### Try it before anyone issues you a live key

Point at the demo with a `cru_demo_` key from [bytesbrains.com/cruise](https://bytesbrains.com/cruise):

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

### Switch to production

Same install — change **only** the key and base URL:

```sh
export CRUISE_API_KEY=cru_live_…
export CRUISE_BASE_URL=https://cruise.bytesbrains.net/v1   # or unset to use the plugin default
hermes doctor
hermes model
```

For any Hermes host you do not fully control, ask for a `cru_live_` key issued with
`--rate-limit` / `--account-rate-limit` so a leaked key cannot spend unbounded.

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

## Model ids

**Name the model as Cruise names it**, from `GET /v1/models` with your key — not as the upstream
provider does. A hardcoded `gpt-4o` reaches Cruise as a model it does not route.

A `bb/…` id is a **lane**: Cruise picks a member per request. Prefer a lane for agent work
(`bb/agentic-coding`); pin a specific model id only when you need that vendor.

After install, `hermes model` lists BytesBrains Cruise and refreshes ids from the live catalogue
for the presented key. Offline seeds in the plugin (`fallback_models`) are a picker backup only —
never a frozen catalogue to ship against.

---

## When Cruise refuses

Cruise answers spending refusals with HTTP `429` and OpenAI’s `insufficient_quota` on purpose, so
stock OpenAI clients fail correctly. **Branch on `error.code`, never on HTTP status alone** —
several codes share `429` and mean different operator actions. Hermes surfaces the provider error
body; treat Cruise codes as themselves.

| Code | HTTP (typical) | Meaning | What to do |
| --- | --- | --- | --- |
| `budget_exhausted` | 429 | The **project** period cap is spent. Often carries `Retry-After`. | Wait for the period to reset, or ask the project owner to raise the cap. Retrying immediately will keep failing until then. |
| `wallet_exhausted` | 429 | The account **prepaid wallet** is empty. **No** useful `Retry-After` — waiting does not help. | Top up or get a credit grant. Do **not** retry in a loop. |
| `measurement_stale` | 429 | That model’s measurement aged out, so Cruise will not route it. | Call a lane (`bb/…`) or another id from `GET /v1/models` for your key. |
| `model_not_found` | 404 | No such model or lane, or nothing in the lane this key may reach. | Refresh ids from `GET /v1/models`. Do not invent upstream provider ids (`gpt-4o`, …). |
| `permission_error` | 403 | The key is valid but not scoped for that model. | Pick a model the key reaches, or ask for a wider key. |

**Period cap vs wallet empty:** both look like “out of quota” to a generic OpenAI client. Read
`error.code`: `budget_exhausted` is a **time-bound project limit**; `wallet_exhausted` is **no
prepaid balance left**. Confusing them leads to pointless retries or the wrong human escalation.

Auth failures (`Missing bearer token`, `Incorrect API key`) use `type: authentication_error` and
are not spending refusals — fix the key or env wiring first.

---

## Ground rules for this client

- **Holds a `cru_` key, never a provider credential.** Blast radius is one revocable, budget-capped
  key.
- **Key in the environment / `$HERMES_HOME/.env` / a secret store — never in a committed config.**
  Settings sync and git history are how keys leak without an event to notice them by.
- **Rate-limit keys** (`--rate-limit` / `--account-rate-limit`) for any Hermes host you do not
  control.
- **Traffic only to the configured Cruise base URL.** No telemetry, no second host.
- **Rehearse on the demo first.** `cruise-demo.bytesbrains.net` with a `cru_demo_` key costs
  nothing and holds no provider credential in the deployment.

See [SECURITY.md](SECURITY.md) for reporting.

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
