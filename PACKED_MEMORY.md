# Packed-memory concept

A packed representation is experimental storage for independently decodable blocks, not automatically a GGML tensor buffer. State how random reads map to tensor offsets and how consumers avoid materializing whole tensors. Candidate block sizes: 4 KiB, 16 KiB, 64 KiB, 256 KiB, 1 MiB, plus tensor/expert-specific sizes.

Evaluate LZ4, selected Zstd levels, bitshuffle/bit-plane transforms, quant-block repacking, and justified sparse formats. Prioritize random access, metadata, alignment, SIMD/GPU friendliness, and fallback. Begin with measurement and a standalone prototype. Inference integration requires an ADR, opt-in flag, correctness tests, and no disabled-path effect.
