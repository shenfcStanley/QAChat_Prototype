## Assumptions

The following assumptions were made in this take-home use case study:
1. **Query Topics Selection:** In order to cover a diverse set of queries (diverse user base) to evaluate the chatbot's performance, I defined query topics as __Basic Questions__, __Clinical Questions__, __Scientific Questions__, and __Ambiguous or Others__ questions.
2. **Domain Expertise Assumed:** In this prototype, I viewed myself as the domain expert to manually evaluate chatbot responses for all categories (for accuracy scoring). In the real-world scenario, it would be better invite domain experts from different background for human-level annotation.
3. **Zephyr-7B for Query/Data Augmentation:** Zephyr-7B was used as a third-party LLM to generate a representative set of diverse queries with few-shot prompting. The initial examples was designed by myself to simulate real-world users (clinicians, researchers, general audience).
4. **ChatGPT-4o as Scorer:** ChatGPT-4o was used as a third-party LLM to simulate human-like evaluation scores where appropriate.
