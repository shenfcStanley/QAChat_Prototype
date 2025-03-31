## Assumptions

The following assumptions were made in this take-home use case study:
1. **Single PDF Scope:** In this prototype, the chatbot is designed to reference a single research paper (HER2 study) rather than a multi-document corpus.
2. **Query Topics Selection:** In order to cover a diverse set of queries (diverse user base) to evaluate the chatbot's performance, I defined query topics as __Basic Questions__, __Clinical Questions__, __Scientific Questions__, and __Ambiguous or Others__ questions.
3. **Domain Expertise Assumed:** In this prototype, I viewed myself as the domain expert to manually evaluate chatbot responses for all categories (for accuracy scoring). In the real-world scenario, it would be better invite domain experts from different background for human-level annotation.
4. **Zephyr-7B for Query/Data Augmentation:** Zephyr-7B was used as a third-party LLM to generate a representative set of diverse queries with few-shot prompting. The initial examples was designed by myself to simulate real-world users (clinicians, researchers, general audience).
5. **ChatGPT-4o as Scorer:** ChatGPT-4o was used as a third-party LLM to simulate human-like evaluation scores where appropriate.
6. **Clinical-Knowledge-Embeddings Selected for Tests:** Although I used three models to generate the initial embeddings, here I assume the Clinical-Knowledge-Embeddings yield the optimal performance overall based on the initial check, and showcase the evaluation on **all 16 queries** using this model to assess response accuracy, quality, evidence grounding, and response time
