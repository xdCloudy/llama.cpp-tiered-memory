# KV-cache research

src/llama-kv-cache.* owns slot/cell semantics and backend tensors; recurrent and MSA memories have distinct structures. Existing K/V type options and backend placement are the first controls to measure. KV is mutable, unlike immutable model weights.

Investigate current K/V quantization, K/V asymmetry, architecture-specific sliding windows, hybrid/full-attention layers, sparse attention, and CPU/GPU placement. Cold tiering helps only when reads are sparse or old ranges are not touched each token. If decode reads the full cache each token, moving or compressing it may add a full decompression/copy cost. Report context, cache type, attention pattern, memory, TTFT, prompt/generation speed, and quality for lossy formats.
