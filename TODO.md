# Project TODO & Ideas

Date: 2025-10-30

## Next Up (High-impact)
- [ ] Fix remaining failing tests (history duplicates; dynamic_rag async plugin)
- [ ] Add SSE cancellation (request.is_disconnected, propagate cancel to LLM/Qdrant)
- [ ] Unify message ID policy (avoid double insert; clear UPSERT rules)
- [ ] Minimal SSE integration test and DI smoke test

## RAG & Knowledge
- [ ] File uploads (PDF/MD/TXT): extract → chunk → embed → Qdrant(UserDocs)
- [ ] Reindex endpoint and delete flow (soft-delete + vector cleanup)
- [ ] Prompt: inject "USER DOCS CONTEXT" before history when relevant

## Tools System
- [ ] Tool registry + interface (name, schema, run)
- [ ] Safe invocation (whitelist, limits, validation)
- [ ] Example tools: getWeather, getTime, searchDocs
- [ ] ChatAgent integration for tool_call roundtrip

## Prompting
- [ ] Tune combined SYSTEM prompt sections and wording
- [ ] Idioms filtering/dedup + size guard
- [ ] Add small per-user profile block if available

## Observability
- [ ] Request-id/trace for streaming logs
- [ ] Standardize log levels; trim noisy info logs

## Dev Experience
- [ ] pytest-asyncio (asyncio_mode=auto) instead of manual fallback
- [ ] Make pre-commit with check_syntax + basic lint
- [ ] Short operational handbook (LM Studio profiles, SSE tips)

## ML / Fine-tuning (Roadmap)
- [ ] Collect high-quality chat transcripts for SFT
- [ ] Synthetic RAG QA generation for domain docs
- [ ] Eval harness (BLEU/ROUGE + retrieval quality, latency)
- [ ] Experiment tracker (wandb or simple CSV)

## Documentation
- [ ] ADR: One SYSTEM prompt (why) and LM Studio alternation (how)
- [ ] Update screenshots/diagrams after uploads/tools

## Ideas (Backlog)
- [ ] Conversation summarization and memory windows
- [ ] Cost-aware RAG (confidence threshold, fallback)
- [ ] Multi-turn tool planning (lightweight planner)

---
Authoring: Shared by team (add initials in parentheses when helpful)
