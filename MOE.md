# Mixture-of-experts research

Current graph construction selects experts and can query llama_moe_cache for host-resident expert weights. The cache tracks/copies expert groups and reports hits/misses. This is the baseline; begin with trace-only routing measurements.

Record per-layer expert frequency, transitions, reuse distance, batch dependence, route-to-transfer latency, bytes copied, promotions, evictions, and hit rate. Compare LRU, LFU, decay-weighted, router-informed prediction, per-layer/global budgets, and fixed/adaptive capacity. Candidate tiers are VRAM hot, pinned-RAM warm, packed-RAM cold, and file-backed fallback; concurrent requests and in-flight copies must remain safe.

Measure prompt and generation separately on realistic prompts and seeds. Router signals help only if available early enough and if prediction beats wasted bytes/cache pollution. Report tail latency and thrashing as well as aggregate hit rate.
