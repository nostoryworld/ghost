# GHOST on Ritual Public Mainnet — integration notes

> Status: RESEARCH ONLY. Nothing in this file is deployed. The GHOST MVP is a
> frontend-only demo; this document records what the official Ritual docs say
> is available on mainnet so the real onchain activation can be built later.
> Verified from https://docs.ritualfoundation.org on 26 Oct 2026 (read-only).
> System-contract addresses below come from the docs and MUST be confirmed
> with `eth_getCode` before any deployment — the docs themselves warn that
> addresses are deployment-specific.

## Connection facts (confirmed)

- Chain ID: **784**
- Native currency: RITUAL, 18 decimals
- RPC: https://rpc.ritualfoundation.org
- Explorer: https://explorer.ritualfoundation.org
- Docs: https://docs.ritualfoundation.org

## Scheduler — documented LIVE, with limits

- System contract: `0x4E0abeE2233D73E66382b45244F7459B34E1490E`
- A contract schedules its own future calls via `schedule(...)`; wakeups arrive
  through `onScheduledExecution(uint256 executionIndex, bytes calldata data)`,
  which must check `msg.sender == address(SCHEDULER)`. No off-chain keeper.
- Limits that shape GHOST:
  - Contracts only — EOAs cannot call `schedule()`.
  - Per-schedule span capped at 10,000 blocks (~25–33 min at 150–200 ms blocks).
  - Indefinite running requires **re-scheduling on every wakeup** (the docs'
    Sovereign Agent Loop pattern: one-shot schedule, then `_scheduleNext()`).
  - Cost: non-refundable residency fee of `1e13` wei (0.00001 RITUAL) per block
    until expiry, plus per-execution funding from the sponsor's RitualWallet.

## Onchain LLM — documented LIVE

- Precompile: LLM at `0x0802` (text model in docs:
  `deepseek-ai/DeepSeek-V4-Flash-0731`).
- Model registry: ModelPricingRegistry
  `0xd190Aa03c401ef5CEcE00927b522974c0f330b97` (`getAllModels()` is
  authoritative).
- No API keys for registry models. Docs example: ~250 fresh input + 150 output
  tokens ≈ 0.00059 RITUAL. Failed LLM calls still charge a fixed 0.01 RITUAL.
- Constraints: one async precompile call per transaction; `convoHistory` is
  required on every LLM call; short-running async budget up to ~500 blocks.

## TEE private compute — PARTIAL (architecture documented, live fleet not evidenced)

- Attestation registry: TEEServiceRegistry
  `0xf4495DC72143D44A93AB0ecE4d6D63a216b27839`.
- DKMS key derivation: precompile `0x081B` (0.01 RITUAL per derivation;
  private key never leaves the enclave). Requires an executor advertising
  `DKMS=6` — otherwise the call reverts.
- Agent layers: Sovereign Agent `0x080C`, Persistent Agent `0x0820`
  (heartbeat every 2,000 blocks, min runtime balance 0.1 RITUAL).
- Honest gaps:
  - No live executor list or count appears in the docs; the number of
    independent TEE providers live on mainnet is unverified.
  - "Private memory" is DKMS-encrypted external storage (GCS/Pinata/IPFS via
    StorageRef), not purely onchain, and not free.
  - Persistent-agent revival is capped at 3 attempts with a 10,000-block
    cooldown; writes after the last checkpoint can be lost.
  - LLM outputs are plaintext by default; encrypted output needs a 65-byte
    `0x04`-prefixed key + `piiEnabled=true` + non-empty `encryptedSecrets` —
    missing any one silently disables PII protection.

## Not live / superseded — do not build on these

- No browsable model marketplace (only the on-chain rate card).
- Infernet is explicitly replaced by native precompiles ("No Infernet").
- No faucet in the docs. Funding = native RITUAL for gas + RitualWallet escrow
  (`0xF04076756d8129Baec46Dc0F1c526Baec490C393`) for compute.

## Open checks before ANY spend or deploy

1. `eth_getCode` on every system-contract address above (chain 784).
2. Confirm a live DKMS-capable TEE executor reachable on mainnet.
3. Confirm a RITUAL acquisition route and fiat price (the airdrop claim page
   was not published as of 26 Oct 2026; treat any unofficial claim URL as
   unverified).
4. Re-price one full wakeup cycle (Scheduler residency + LLM call + DKMS)
   before promising any subscription price.

## How the MVP maps to this (later, not now)

- Morning message (localStorage today) → Scheduler self-wakeup + LLM call.
- Browser memory (localStorage today) → DKMS-encrypted StorageRef memory.
- Shareable card (canvas today) → onchain-attested Ghost moments.
- Until the checks above pass, all three stay labeled PENDING in the UI.
