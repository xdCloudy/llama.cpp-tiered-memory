# Risks and mitigations

- Poor secondary compressibility: profile first; stop or target favorable tensor classes.
- Decode cost exceeds transfer savings: measure end-to-end; retain fallback.
- Peak memory grows because packed and decoded copies coexist: track live bytes and avoid whole-tensor materialization.
- Paging/pinning harms host: cap locked-memory budgets and measure system pressure.
- Thrash and tail latency: bounded caches, hysteresis, trace replay, and tail metrics.
- Async lifetime/corruption bugs: bounds checks, checksums, ownership, synchronization tests, fallback.
- Upstream churn: narrow patches, isolated branches, documented sync.
- Platform skew: test Windows/Linux separately; keep core portable.
- Misleading results: compare upstream and disabled fork; report variance and negative outcomes.
- Lossy quality regression: explicit opt-in and quality/perplexity criteria.
