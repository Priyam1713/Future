# Future permanent development instructions

## 80/20 delivery rule — user directive, 2026-11-02

Prioritize approximately 80% of practical functionality with the most efficient 20% of effort. This supersedes earlier requirements for exhaustive completion before advancing. The percentages are prioritization guidance, not a measured coverage claim.

- Work on one technique at a time in the exact inventory ID order. Preserve the 60-technique taxonomy, 54 retained techniques, six excluded IDs (25, 27, 41, 42, 47, 48), resource rankings and variations. Exclusions remain excluded unless the user changes them.
- Build the core engine and highest-value variations; research and extract the most useful source-supported rules. Defer expensive edge cases, obscure variations and exhaustive research to P1/P2 refinement.
- Never trade away core numerical accuracy, independent verification, source provenance, licensing compliance or passing functionality for speed.
- Keep deterministic calculations independent of LLM interpretation. Separate direct, compositional and unsupported interpretations; isolate conflicting traditions and explicitly name conventions.
- Freeze a supported / experimental / unsupported configuration matrix. Incomplete experimental functionality does not block a stable core release and must not be advertised as supported certification.
- Define concrete acceptance criteria, run the complete regression suite and CLI smoke tests, record limits and prioritized backlog, then mark **Core v1 Ready** when those criteria pass. This does not mean exhaustive or empirically validated.
- Commit and push each meaningful verified pass; update PROGRESS.md concisely. Commit the current technique's closure before beginning the next technique's resource/variation audit. Do not implement the next technique before closure.
- Preserve local/offline reproducibility, immutable versioned rules, rights restrictions and existing interfaces. Avoid new frameworks, premature UI and unrelated infrastructure.

The original inventory is preserved in resources/ and knowledge/inventory.json. Release scope and acceptance records are in knowledge/; history is in PROGRESS.md. Read the current records before resuming; do not treat historical progress entries as current blockers when superseded by this directive.
