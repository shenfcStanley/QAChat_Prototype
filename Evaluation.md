## Evaluation Overview

This evaluation assesses the chatbot’s ability to generate clinically accurate, grounded answers from a HER2 breast cancer paper, using Clinical-Knowledge-Embeddings as the default selected strategy and Mistral-7B as the open source LLM.

**Assumption:** Based on initial testing, Clinical-Knowledge-Embeddings provided the most clinically relevant retrieval results. Thus, evaluation was scoped to this embedding configuration for all 16 queries.

#### Query Augmentation
`Zephyr-7B-Beta` was utilized as a third-party language model for query/data augmentation. 16 queries was generated.

#### LLM-based Scoring and Human-level Scoring
`ChatGPT-4o` was used for automated result scoring. Prompts for query augmentation and auto scoring is under `tests\prompts`. I serve as the domain expert to conduct human-level scoring.


## Test Set
A total of 16 queries were used, balanced across user types. Half of the queries were generated directly, and the other half were semantically augmented to simulate varied user phrasing. Please go to [comprehensive test results](tests/testresults/eval_results.csv) for accessing the comprehensive test results.

| Category          | Example                                    |
|-------------------|--------------------------------------------|
| Basic-Original   | "What is HER2?"                            |
| Basic-Original   | "Is HER2 a gene or a protein?"                            |
| Clinical-Original  | "What treatment options are mentioned for HER2-positive patients?" |
| Clinical-Origiinal  | "How does HER2 amplification affect survival rates?" |
| Scientific-Origiinal  | "How many patients were included in the HER2 study?" |
| Scientific-Origiinal  | "What statistical methods were used to evaluate HER2’s effect on outcomes?" |
| Others-Original | "Who discovered HER2?" |
| Others-Original | "Is HER2 mentioned in the conclusion?" |
| Basic-Augmented   | "What is HER2 and how is it related to breast cancer?"                            |
| Basic-Augmented   | "Can you explain what HER2 amplification means in the context of breast cancer?"                            |
| Clinical-Augmented  | "Which drugs are recommended for HER2-positive breast cancer patients, and at what dosage?" |
| Clinical-Augmented  | "What is the overall survival rate for HER2-positive breast cancer patients after treatment?" |
| Scientific-Augmented  | "How many patients with metastatic breast cancer were included in the HER2 study, and how were they recruited?" |
| Scientific-Augmented  | "Were any adverse events reported during the HER2 study, and how were they managed?" |
| Others-Augmented | "Were any alternative therapies to HER2-targeted treatment tested in the study, and if so, how effective were they?" |
| Others-Augmented | "Did the study mention any potential long-term side effects of HER2-targeted treatment, and how were they monitored?" |


#### Business Metrics
- Mean response time (sec): 50.47 
- Mean LLM-based score (1-5): 4.25
- Mean Human-level score (1-5): 4.19
- Acceptable Answer Rate (Human Score ≥ 4): 81.2%
- Acceptable Answer Rate (LLM ≥ 4): 87.5%

### Human vs. LLM Score Correlation

To estimate the reliability of using LLM for automatic scoring, Pearson correlation was calculated between human-labeled and LLM-based scores.

- **Correlation**: 0.82

This suggests that LLM-based scoring can be used as a reasonable proxy for expert review in future iterations.


### 🚀 Next Steps and Future Evaluation Plans

- Extend evaluation to include all three embedding models in a side-by-side comparison.
- Increase query volume and include multi-hop reasoning questions.
- Incorporate real-world user feedback and satisfaction tracking (e.g., thumbs up/down in UI).
- Perform expert adjudication of borderline cases and add qualitative annotations.
