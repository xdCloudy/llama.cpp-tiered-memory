# ADR-000: project scope and research boundary

- Status: accepted
- Date: 2026-10-07

## Context
The fork investigates whether semantic knowledge in llama.cpp can improve compact storage, tiering, and movement for inference. Meta CRAM motivates compressed-memory bandwidth but is a hardware design.

## Decision
Treat this as an independent llama.cpp-specific research implementation inspired by CRAM-style principles. Keep experiments opt-in, benchmark-driven, and isolated from default upstream behavior. Do not create generic user-space ZRAM or imply a literal port.

## Consequences
The project may reject compression in favor of avoiding copies, better pinning, mmap behavior, or cache locality. Every claim needs upstream and fork-disabled controls. New runtime abstractions require evidence and a separate ADR.
