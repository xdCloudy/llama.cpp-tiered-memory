# EXP-002: MoE expert locality

## Question
Do realistic prompt and generation traces show useful per-layer expert frequency skew, temporal locality, or predictable transitions?

## Hypothesis
Some workloads may reuse a small fraction of experts, but routing can vary by prompt, token, layer, and batch. Aggregate frequency may not predict the next expert.

## Implementation
Planned trace-only instrumentation or graph callback capture, using existing llama_moe_cache as reference. Record routing counts, transitions, reuse distance, copy bytes, and cache behavior without changing routes or outputs.

## Status
Planned. Define privacy-safe prompt fixtures and trace format before collecting. Report workload/model details and separate prompt from decode. No locality result is established.
