# Memory tiers

Proposed conceptual tiers: HOT = VRAM, WARM = pinned host RAM, COLD = packed/compressed host RAM, VERY COLD = GGUF/NVMe or existing file mapping. These are hypotheses, not required policy. Pageable host RAM and OS page cache are separate resources.

Promotion/demotion may use LRU, LFU, weighted/decayed hotness, routing, or layer sequence. Bound caches; use hysteresis and in-flight ownership so pressure cannot cause thrash or use-after-free. Track hits, bytes moved, wait time, eviction value, and full-inference latency. Compare pinning against compression; warm pinned memory may be better than decoding compressed data.
