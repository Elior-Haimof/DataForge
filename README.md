# ⚒️ DataForge: Human-in-the-Loop AI Data Preprocessing

📄 **[Read the Full Academic Research Paper (PDF)](./DataForge_Academic_Paper.pdf)** ⚙️ **[View Detailed Environment Configuration Guide (TXT)](./SETUP_GUIDE.txt)**

Data preprocessing remains a massive bottleneck in data science. Traditional "black-box" cleaning tools rely on rigid statistical heuristics, often blindly deleting valid contextual data (e.g., flagging a luxury penthouse as an anomaly because its price exceeds the neighborhood mean). 

**DataForge** is a "negotiated data cleaning" application that solves this. By integrating Meta's Llama 3, the system detects anomalies and generates natural language explanations for its flags. Instead of forcing automated deletions, it provides the user with the context needed to make informed decisions to accept, reject, or manually refine changes.

[DataForge Demo](https://github.com/user-attachments/assets/8f51135a-4fab-4652-9c4b-94a91dc1e396)

### 📈 Business Impact & Study Results
We validated DataForge through a controlled within-subjects study using injected "data-mines" (valid outliers). Shifting from a black-box model to an explainable AI (XAI) interface yielded significant improvements in trust calibration:
* **Reduced False Acceptance Rate:** Dropped from 40.0% to 6.7% (-33.3%).
* **Increased Correct Rejection Rate:** Improved from 46.7% to 86.7% (+40.0%).
* **Overall Decision Accuracy:** Increased to 77.3%.

### 🛠️ System Architecture & Tech Stack
* **Frontend & State Management:** Python, Streamlit (Custom CSS, Session State tracking).
* **AI/LLM Engine:** Meta Llama 3.1 via Ollama API (Few-Shot Prompting).
* **Anomaly Detection:** Rule-based statistical modeling (Z-scores, multivariate heuristics).
* **Explainable AI (XAI):** Pre-computed reasoning engine generating contextual justifications for statistical flags.

### 💻 Quick Start
For full comprehensive steps on setting up your local environment, database parameters, and dependencies, please refer directly to the native **[SETUP_GUIDE.txt](./SETUP_GUIDE.txt)** file.

1. Ensure Ollama is running locally with `ollama pull llama3.1`.
2. Activate your local environment and install requirements: `pip install -r requirements.txt`.
3. Launch the application root: `streamlit run app.py`.
