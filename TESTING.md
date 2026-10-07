# Testing strategy

Profiler validation covers GGUF metadata/payload bounds, quant types, deterministic codec round trips, partial blocks, truncated input, and report stability. Runtime prototypes additionally cover alignment, eviction/promotion, concurrent reads, checksums, fallback, and async lifetime.

Use existing GGML/llama test infrastructure where possible. CUDA results are checked against CPU/reference output for supported formats. Lossless transforms reproduce bytes; lossy paths need explicit quality/perplexity analysis. Avoid large model downloads and timing thresholds in CI. Benchmarks are separate from correctness CI.
