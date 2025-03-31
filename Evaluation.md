### 🧪 Evaluation Overview

This evaluation assesses the chatbot’s ability to generate clinically accurate, grounded answers from a HER2 breast cancer paper, using Clinical-Knowledge-Embeddings as the default selected strategy and Mistral-7B as the open source LLM.

**Assumption:** Based on initial testing, Clinical-Knowledge-Embeddings provided the most clinically relevant retrieval results. Thus, evaluation was scoped to this embedding configuration for all 16 queries.

#### Query Augmentation
`Zephyr-7B-Beta` was utilized as a third-party language model for query/data augmentation.

#### LLM-based Scoring and Human-level Scoring
`ChatGPT-4o` was used for automated result scoring. Prompts for query augmentation and auto scoring is under `tests\prompts`. I serve as the domain expert to conduct human-level scoring.


#### Business Metrics
- Mean response time (sec): 50.47 
- Mean LLM-based score (1-5): 4.25
- Mean Human-level score (1-5): 4.19
- Correlation between LLM scorer and human scorer: 0.91
- Acceptable Answer Rate (Human Score ≥ 4): 81.2%
- Acceptable Answer Rate (LLM ≥ 4): 87.5%


