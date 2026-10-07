# Decision log

Architecture decisions live as numbered ADRs in docs/decisions/. Each record includes context, options, decision, consequences, status, and evidence. Superseded records remain with a link to the replacement.

## Current decisions
- ADR-000: independent llama.cpp-specific research fork inspired by compressed-memory principles, not a literal Meta CRAM port. See docs/decisions/ADR-000-project-scope.md.
- No runtime data path is selected. M0/M1 evidence will determine whether a packed store or profiler-only result is justified.
