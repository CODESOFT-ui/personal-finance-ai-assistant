# Assignment 4 — RAG Agent Report

**Student:** Joseph
**Project:** Personal Finance RAG Agent (adapted from `RAG_AI_Agent`)

## Assigned use case

A guarded, evaluated Retrieval-Augmented Generation assistant for **personal finance / financial literacy**. Users ask money questions; the agent retrieves from a small finance knowledge base, runs three parallel specialists (budgeting, investing, account-security), and returns a cited answer — wrapped in input/execution/output guardrails and automatic evaluation.

## Documents used

Four **original** PDFs I generated (`data/build_pdfs.py`, so no copyright issues), one per finance sub-topic:

1. `01_budgeting_and_saving.pdf` — 50/30/20 rule, emergency funds, zero-based budgeting, sinking funds, inflation.
2. `02_investing_basics.pdf` — compound interest, diversification, index funds, risk/return, dollar-cost averaging, retirement accounts.
3. `03_banking_and_credit.pdf` — savings vs current accounts, credit cards, credit scores, loan interest, digital payments, deposit insurance.
4. `04_fraud_and_account_security.pdf` — phishing, 2FA, passwords, card skimming, identity theft, investment scams.

Ingestion result: **4 PDFs → 12 chunks** (chunk_size 800).

## What I changed (prompts & settings)

**Domain adaptation (prompts):**
- Renamed the three specialists health/gym/fitness → **budgeting / investing / safety**, and rewrote each specialist prompt for its finance angle.
- Rewrote the **NLP input guard** rules: UNSAFE now means get-rich-quick/insider-trading/fraud requests or anything off-topic for personal finance; SAFE = budgeting, investing, banking, fraud-safety questions.
- Rewrote the **guardrail agent** and **NLP output guard** checks for finance (no "guaranteed returns", no posing as a licensed adviser, recommend a professional for big decisions) instead of medical rules.
- Rewrote all 10 demo scenarios for finance — including a **card-number redaction** demo, which is especially relevant in this domain.

**Embeddings:** switched from local HuggingFace MiniLM to **OpenAI `text-embedding-3-small`** (removes the PyTorch dependency entirely).

**Two tuned settings (as required):**

| Setting | Default | Tuned to | Why / impact |
|---|---|---|---|
| `CHUNK_SIZE` / `CHUNK_OVERLAP` (chunking) | 1000 / 200 | **800 / 150** | The finance PDFs are short and topic-dense; smaller chunks keep each vector focused on one concept, so retrieved chunks are less "mixed-topic." With 4 short PDFs this yields 12 clean chunks. |
| `TOP_K` (retrieval) | 4 | **5** | Each PDF page is one source; retrieving 5 chunks gives the three specialists enough cross-topic context (e.g. an emergency-fund question also surfaces a relevant investing chunk) without flooding the prompt. |

**Different judge model (as required):** generator = `gpt-4o-mini`, **LLM-as-judge = `gpt-4.1-mini`**. The judge is intentionally a different model so it is not grading its own output.

## 3 test questions & outputs

**Q1 — "How should I build an emergency fund and how big should it be?"** (verified run)
- Routed: regex guard PASS → NLP guard PASS (recognised as a budgeting question) → retrieved 5 chunks → 3 specialists → planner chose **detailed** → answer grounded in `01_budgeting_and_saving.pdf` with citations.
- Answer (excerpt): *"aim to save three to six months' worth of essential expenses … kept in an easily accessible savings account … start with one month … use zero-based budgeting."*
- Guardrail agent: **APPROVED**. Output guards: PASS.
- **LLM judge (`gpt-4.1-mini`): claim precision 100%, hallucinations 0, relevancy 1.00**, grounding 20% (the judge counts how many of the 5 retrieved chunks directly support the answer — only the budgeting chunks did, which is correct).

**Q2 — "What's the best workout routine to build muscle?"** (off-topic) → **BLOCKED by the NLP input guard**: *"The query is completely off-topic and unrelated to personal finance."* Demonstrates the domain guard works.

**Q3 — standalone metrics demo (`examples/run_evaluation.py`)** → exercises every search & answer metric:
`MRR 1.0 · MAP 0.70 · Precision 0.40 · Recall 1.0 · F1 0.57 · NDCG 0.89 · ROUGE-1 0.53 · ROUGE-2 0.25 · ROUGE-L 0.53 · Fuzzy 58/68 · Semantic 0.38`.

**Tests:** `33/33 passing` (`pytest`), covering ingestion, the agent graph (now finance-named), `main`, and the full `rag_evaluator` metrics package.

## What worked well / what didn't

- **Worked:** the guardrail + RAG + evaluation pipeline ran end-to-end on the new domain with only prompt/data changes — the graph structure didn't need redesigning. The NLP guard correctly distinguishes finance from off-topic. Citations point at the exact source PDF/page. Swapping to OpenAI embeddings made the project lightweight (no multi-GB PyTorch download).
- **Didn't / limitations:** with only 4 short PDFs, retrieval `recall` is easy but `precision` is modest (TOP_K=5 over 12 chunks pulls some loosely-related chunks) — the judge's grounding score reflects this. A larger, deeper corpus and a reranking step would be the next improvement. The standalone `examples/run_evaluation.py` must be run with `pip install -e .` (or PYTHONPATH set) so the package resolves.

## How to reproduce
```powershell
pip install -r requirements.txt
copy .env.example .env            # add OPENAI_API_KEY
python ingestion.py               # 4 PDFs -> 12 chunks
python guardrails_rag_graph.py    # ask a question, or type 'demo'
pip install -e . ; python examples/run_evaluation.py   # metrics demo
pytest -q                         # 33 tests
```
