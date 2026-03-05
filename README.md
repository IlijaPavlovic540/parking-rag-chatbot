# parking-rag-chatbot - Stage 1


## Overview

This project implements the **first stage** of an intelligent chatbot system for managing parking space reservations.
The chatbot uses **RAG** to answer user questions about the parking facility and to collect reservaation information from users.

The system integrates a ** vector database ( Weaviate)** for sematic search, **LangChain** for RAG orchestration, and **OpenAI embeddings** for semantic similarity.

This stage focuses on building the ** core RAG architecture, interactive chatbot behavior, guardrails, and evaluation of system performance**.


---

# Architecture

The system is composed of several main components:

### 1. Knowledge Base ( static data )
Static parkign information is stored as Markdown files in: data/static_kb/

Examples:
- parking location
- prices
- rules
- working hours
- reservation prceoss

These documents are split into chunks and stored as embeddings in a **Weaviate vector database**.

---

### 2. Vector database ( Weviate )

The vector database stores:

- document chunks
- embeddings generated using OpenaAI models
- metadata such as document source

This ennables **semantic retrieval** of relevant information for users queries.

---

### 3. Retrieval-Augmented Generation (RAG)

When a user asks a question:

1. The question is embedded using OpenaAI embeddings.
2. The system retrieves the **top-K relevant chunks** from Weaviate.
3. The retrieved context is inserted into a prompt.
4. The LLM generates an answer using that context.

This improves accuracy and reduces hallucinaitons.

---

### 4. Chatbot Interaction (CLI)

For stage 1, the chatbot runs as a **command - line interface (CLI)**

User can:
- ask questions about the parkign system
- start a reservation
- provide reservation details


---

### 5. Guardrails ( Data protection )

To prevent sensitive data exposuere, the system implements thwo guardrail mechanisms.

### Policy Filtering

The chatbot blocks requests attemtpting to extract internal system data such as:

-- syste prompts
-- database dups
-- API keys
-- full reservation lists

### PIII Detection and redaction

Sensitive information is detected using **MIcrosfo Presidio**

Detected entities include:
- person names
- phone numbers
- email addresses
- locations
- vehicle license plates

These values are automatically **anoymized before output**


# Installation

### 1. Clone the repository

git clone <rep-url>
cd parking-chatbot

### 2. Create virtual env

python -m venv .venv

Activate it:
Windows: .venv\Scripts\activate
Linux / Mac: source.venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt

---

# Environment Configuration

Create a .env file int the project root:

WEAVIATE_URL=your weavite url
WEAVIATE_API_KEY = your weavite key
PG_HOST= localhost
PG_PORT = 5432
PG_DB = postgress db name
PG_USER = postgress db user
PG_PASSWORD = postgress db password
OPENAI_API_KEY= your openai api key

---

# Data Ingestion

Before running the chatbot, the knowledge base must be ingested into the vector databse.

python app/rag/ingest_lc.py

This will:
1. Load documnets from the 'data/static_kb'
2. Split them into chunks
3. Generate embeddings
4. Store them in Weaviate

---

# Runnint the Chatbot

Start the CLI chatbot:

python app/chat_cli.py


# Evaluation

The system is evaluated using two types of metrics:

## Retrieval Accuracy

Metrics:
- Recall@k
- Precision@k

Run evaluation:

python app/evaluation/retrieval_eval.py

## Performance Testing
Latency tests measure reposnse perofmrance

python app/evaluation/latency_test.py

Measured values include:
- Retrieval latency
- End to end resposne time

Results are documented in:

reports/stage1_evaluaiton.md

---

# Testing

Unit tests are implemnted using **pytest**.

Run tests: pytest -q

Test cover:

- guardrails polocy filtering
- PII redaction
- reservation validaiotn
- evaluation metric calculations

---

# Continue Integration CI

Github actions automatically runs tests on:

- push
- pull request

CI workflow:

.hithub/workflows/ci.yml
