# 🎓 Enterprise-Multimodal-Compliance-Intelligence-RAG-Pipeline

### *Transforming Unstructured Video & Audio Archives into Real-Time AI Intelligence*

---

## 🎨 Tech Stack & Badges

![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enterprise-multimodal-compliance-intelligence-rag-pipeline-sr.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

---

## 🌐 Overview

Educational platforms, corporate archives, and content creators generate thousands of hours of video content. However, finding precise information within video archives traditionally requires tedious timeline scrubbing.

This project delivers an **end-to-end Retrieval-Augmented Generation (RAG) platform** that ingests raw video/audio media, extracts timestamped text transcripts, builds high-dimensional vector representations, and serves an interactive Streamlit application. Users can ask natural-language questions and instantly receive grounded answers complete with **video references and second-level timestamp citations**.

---

## 🔥 Features

### 🧠 Core Analysis Engine
* **Timestamp-Level Citation Precision:** Maps every generated response directly to the exact video ID and second-by-second time window.
* **Semantic Vector Search:** Computes high-dimensional vector proximity using Cosine Similarity to capture conceptual meaning over literal keyword matching.
* **Zero-Hallucination Guardrails:** Prompt engineering constraints enforce strict context grounding to prevent off-topic or fabricated answers.
* **Resilient API Architecture:** Implements exponential backoff retry routines and dynamic model failovers to handle server spikes without crashing.

## 🎨 User Experience-
* **Interactive UI:** Clean Streamlit dashboard for real-time querying and instant generation.
* **Auditable Source Data:** Collapsible expanders reveal raw matching transcript chunks, similarity scores, and metadata.
* **Responsive Feedback:** Displays status indicators, clear error notifications, and warning dialogs for missing inputs.

---

## 📂 Project Structure-

```bash
RAG-based-AI-Teaching-Assistant/
├── .gitignore               # Shields API secrets (.env) & temporary caches
├── README.md                # Main system documentation
├── requirements.txt         # Project dependencies lockfile
├── .env                     # Local environment credentials (DO NOT COMMIT)
├── embeddings.joblib        # Serialized vector database & chunk metadata
├── prompt.txt               # Master prompt template for LLM groundings
├── app.py                   # Streamlit web application & vector search UI
├── 01_Video_To_mp3.py       # Pipeline Step 1: Video to MP3 Conversion
├── 02_mp3_To_json.py        # Pipeline Step 2: Audio Transcription & Timestamping
├── 03_Preprocessing_json.py # Pipeline Step 3: Text Cleaning & Chunk Formatting
├── 04_Process_Incoming.py   # Pipeline Step 4: Vector Embedding Generation
├── 05_Merge_chunks.py       # Pipeline Step 5: Vector Store Serialization
├── check_models.py          # Diagnostic script to verify Gemini API access
├── json/                    # Directory storing raw JSON transcript outputs
└── newjsons/                # Directory storing processed JSON transcript chunks
```
---

## ⚡ Quick Start
Automated Setup (PowerShell / Windows)

```bash
python -m venv venv
.\venv\Scripts\Activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Manual Setup

1. Clone the repository:

```bash
git clone [https://github.com/your-username/RAG-based-AI-Teaching-Assistant.git](https://github.com/your-username/RAG-based-AI-Teaching-Assistant.git)
cd RAG-based-AI-Teaching-Assistant
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your API keys:
Create a .env file in the root directory:

```bash
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

5. Launch the web application:

```bash
python -m streamlit run app.py
```
---

## 📖 Usage Guide & Workflow

1. Inquire: Enter your question into the Streamlit natural-language input field.

2. Retrieve: The pipeline vectorizes your query using gemini-embedding-001 and scans embeddings.joblib via cosine similarity.

3. Synthesize: Top matching transcript chunks are injected into prompt.txt and dispatched to gemini-3.6-flash.

Verify: Review the generated response alongside exact video references and timestamp citations. Expand source cards to inspect original transcripts.

---

## 💡 Example Questions to Try

* "What is an artificial neural network and in which lecture is it explained?"

* "Explain the difference between supervised and unsupervised learning."

* "Where is gradient descent discussed in the videos?"

Understanding the Result

* Grounded Answer: Generated text synthesized strictly from matched transcript segments.

* Video ID: The specific video file where the concept occurs.

* Timestamp Range: [Start Time - End Time] in seconds to locate the exact segment.

---

## 📤 Exporting Results

* Copying Text: Click the copy button on any generated response box to copy answers and citations directly.

* Exporting Data: Matched transcript tables can be exported as .csv or .json directly through Streamlit's native data display widgets.

---

## ⚙️ Configuration
Control app defaults via .env:

```bash
GEMINI_API_KEY="your_google_gemini_api_key"
TOP_K_RESULTS=5
DEFAULT_EMBED_MODEL="gemini-embedding-001"
DEFAULT_CHAT_MODEL="gemini-3.6-flash"
```

---

## 🤖 Model Information

1. Embedding Model: gemini-embedding-001 (Produces 768-dimensional dense vector embeddings).

2. Generative LLM: gemini-3.6-flash (Primary high-speed LLM model) with dynamic fallback to gemini-1.5-flash during peak traffic spikes.

---

## 🔍 References & Architecture

* Vector Search: scikit-learn Cosine Similarity matrix calculations over NumPy float32 vectors.

* Serialization: Joblib compressed binary data formats for rapid vector store deserialization.

---

## 🛠️ Development & Adding New Features
To run new video archives through the pipeline:

1. Place raw .mp4 or .mkv files into your working directory.

2. Execute processing scripts sequentially:

```bash
python 01_Video_To_mp3.py
python 02_mp3_To_json.py
python 03_Preprocessing_json.py
python 04_Process_Incoming.py
python 05_Merge_chunks.py
```

3. Restart app.py to reload the newly generated embeddings.joblib.

---

## 🐞 Troubleshooting & Debug Mode

* API Key Errors: Verify .env file formatting and ensure the key has active permissions in Google AI Studio.

* Missing Embeddings Error: Run python 05_Merge_chunks.py to generate embeddings.joblib.

* Diagnostic Check: Run python check_models.py in your terminal to inspect available models and verify connectivity:

```bash
python check_models.py
```
---

## 🎓 Educational Use & Perfect For

* Students: Ask natural-language questions against lecture archives and jump straight to relevant time markers.

* Researchers: Rapidly audit long audio/video recordings and symposium transcripts for exact citations.

* Content Creators: Make video catalogs searchable for viewers and subscribers.

---

## 🔮 Future Enhancements

[ ] Add interactive video player embedding directly inside Streamlit with jump-to-timestamp links.

[ ] Migrate embeddings.joblib to persistent vector databases (Qdrant/Pinecone) for multi-gigabyte scale.

[ ] Add automatic transcript PDF export functions.

## 📜 License
Distributed under the MIT License. See LICENSE for details.

---

## 🤝 Contributing
Contributions are welcome!

1. Fork the Project.

2. Create your Feature Branch (git checkout -b feature/NewFeature).

3. Commit your Changes (git commit -m 'Add NewFeature').

4. Push to the Branch (git push origin feature/NewFeature).

5. Open a Pull Request.

---

## 📬 Contact & Support

Project Developer: Sheetal Rajput

Issues: Open a GitHub Issue for technical questions or bug reports.

---

## 🙏 Acknowledgements

* Google Gemini API for fast embedding and generation endpoints.

* Streamlit for rapid UI deployment tools.

* Scikit-Learn for vectorized similarity calculations.

