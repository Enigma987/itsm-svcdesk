<!-- ai-generated: 90% - Codex documented the provenance of the instructor-supplied investigation transcript. -->
# Investigator transcript provenance

`transcript.md` is an unchanged copy of `Laboratory 4/Recordings/lab4-rec-3/transcript-recorded.md`, supplied by the instructor. It records the course agent loop using `qwen3:4b-instruct` through the read-only Prometheus tools.

HANDOUT.md explicitly permits a live-path student to use any supplied recording's transcript and test its hypotheses against the student's own live snapshot. This is the approved transcript route. The recorded investigation happened on a different run and date; the scorecard must evaluate the quoted claims against our actual incident data and explain any disagreement. No new model execution or MCP session is claimed for this copied transcript.

The on-call operations, page, ticket, flag changes and service recovery are captured separately as actual API responses in `incident/operations.jsonl`. The final incident clocks come from `itsmlab incident 4`.

## Independent second investigator

The second scorecard uses a fresh-context Codex sub-agent against a separately served copy of our saved snapshot. It received only the symptom and UTC window. Its actual calls went through the unmodified course `prom_mcp.py` server with `mcp==2.2.0`, using `scripts/lab4_mcp_client.py` as a CLI adapter. The local `.venv` environment is ignored by Git.

`second/transcript.md` preserves the prompt, actual tool responses and final answer. `second/tool-events.jsonl` is the tool-call log, and `second/hypotheses.json` preserves the investigator's own candidate claims. The parent independently translated those claims into the filtering comparisons in `ai-rca-eval-2.json`; actual scorecard returns are in `second/query-results.json`. The exact inherited API model identifier was not exposed, and the provenance says so.

`COMPARISON.md` compares the two investigations while distinguishing contradicted candidate hypotheses from confident final claims.
