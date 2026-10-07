# CPU research notes

CPU inference is a supported target. Current CPU backend code has quantized traits, repacking, threaded kernels, and architecture variants. A secondary decoder must not compete with hot matrix operations for cache bandwidth without showing a net gain.

Profile AVX2, AVX-512, ARM NEON, and generic fallback where available; vary block size, workers, NUMA, and fused/staged decode. Report codec throughput separately from prompt/generation throughput. Check packed round trips and quantized tensor correctness against canonical bytes.
