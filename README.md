# GHOST 👻 — MVP (frontend-only demo)

A self-running private AI agent product (working title). This MVP is a
**frontend-only demo with honest labeling**. It does not claim any onchain
feature is live.

## What works (all local, $0, no server)

- **One Ghost persona**: friendly, witty, secret-keeping. Default name "Ghost".
  Short replies, playful tone.
- **Web chat**: replies are generated **locally in the browser** with simple
  rule-based/personality responses keyed to keywords, memory, and time of day.
  No external API calls, no API keys.
- **Memory in localStorage**: your name (if given), facts you ask Ghost to
  remember, secrets you mark as secrets, and conversation highlights persist
  across sessions on the same device. The UI states honestly:
  *"Memory lives in your browser for now — mainnet sealed memory pending."*
- **Morning message**: when you open the app on a new calendar day, Ghost has
  a message waiting, computed from stored memory + the date.
- **Shareable card**: any Ghost reply (or the morning message) has a
  "Make share card" button. The card renders the quote and offers PNG download
  and copy. **Redaction rule**: if a message contains anything you marked as
  a secret, Ghost refuses to card it and says why. Secrets are never repeated
  on cards.
- **Roadmap section**: "Roadmap: mainnet activation" lists Scheduler
  self-wake-ups, TEE sealed memory, and onchain LLM — all clearly labeled
  **PENDING** (pending the RITUAL airdrop claim).

## What is NOT live (and is never claimed to be)

- No wallet connection. No mainnet transactions. No TEE attestation.
- No onchain inference. No Scheduler wake-ups. No external API calls.

## Run locally / deploy

- Open `index.html` in a browser — that's the whole app.
- `worker.js` is the Cloudflare Worker bundle, generated from `index.html` by
  `build.py` (it embeds the page as a single static response, no bindings).
- Live demo: https://ghost.odemakindeezekiel5.workers.dev

## License

MIT — see `LICENSE`.
