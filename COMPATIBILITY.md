# Compatibility contract

Follow upstream GGUF parsing, GGML tensor types, graph behavior, and backend contracts. Packed formats, if introduced, are explicit experimental storage with independent metadata; they do not silently change existing GGUF quantization. Models remain loadable through the standard path when an experimental file, codec, backend, or option is unavailable.

Default build and invocation preserve upstream behavior. Experimental options and formats are opt-in and versioned. Corrupt or unavailable experimental data must fail safely or use the documented fallback. Keep public API changes out of early milestones. Record upstream conflicts, backend gaps, model coverage, and fallback behavior here.
