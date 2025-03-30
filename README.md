# QAChat_Prototype

## Description
This is the take-home case study/real world problem exercise finished by __Feichen Shen__.  
In this task, a Q/A chatbot prototype was built to address diverse questions related to a specific research paper. The work also clearly presented comprehensive evaluations/testing/KPI definition and detailed how clinical network embeddings can be incorporated.

## Overall Workflow

The overall workflow design followed a Retrieval Augmented Generation (RAG) architecture:  
1. Query submission
2. Ingest and parse knowledge data, construct a vector database
3. Semantic search
4. Return top K relevant results as context, and design prompt based on context
5. Post-process and response

<img src="imgs/workflow" alt="Chatbot Illustration" width="300"/>
