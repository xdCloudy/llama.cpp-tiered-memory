# QA and acceptance

Before an experiment is usable, verify build coverage, deterministic fallback, bounds handling, cleanup, error paths, and docs. Review allocations and async lifetimes, not only output correctness. Exercise Windows/Linux where supported; keep unavailable APIs optional.

Performance QA uses upstream, feature-disabled fork, and feature-enabled fork. Record repeated measurements and preserve failures. Negative or inconclusive outcomes are acceptable; missing evidence is not. For each milestone, link issues, commits, build/test logs, workload manifests, and reports.
