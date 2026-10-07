# Design principles

This is a set of experiments, not one universal compressor. Each candidate declares data class (immutable weights, expert slice, KV region, workspace), mutability, lifetime, access granularity, consumer backend, and allowed loss. Those facts determine whether it belongs in packed storage, pinned host RAM, VRAM, an ordinary backend buffer, or nowhere.

A useful prototype needs independently decodable blocks, versioned indexing, alignment metadata, corruption detection, bounded memory, concurrent-read semantics, explicit ownership, async completion rules, and fallback. The block format should permit CPU SIMD and GPU decoding comparisons without coupling every experiment to one codec. Default inference remains on normal upstream allocations unless explicitly enabled.

Avoid premature API design. First profile already-quantized GGUF payloads and current loading. Prefer a standalone tool for offline profiling; introduce an inference interface only when measurements justify decode and management costs. Lossy transforms require explicit naming, metadata, opt-in behavior, and quality measurements.
