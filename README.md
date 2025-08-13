# ✈️ WanderMind AI – AI-Powered Travel Itinerary Designer

WanderMind AI is an interactive **Streamlit** application that uses **LangGraph** multi-agent workflows and **AWS Bedrock** LLMs to design personalized travel itineraries based on destinations, budget, dates, and interests.

---

## 🚀 Features
- **Multi-Agent Workflow** with LangGraph  
- **AWS Bedrock Models** for research, budget optimization, and itinerary composition  
- **Interactive Streamlit UI**  
- **Downloadable Itinerary** in plain text  
- **Customizable** destinations, dates, budget, and interests  

---

## 🛠 Tech Stack
- **Python 3.10+**  
- **Streamlit** – Web UI  
- **LangGraph** – Agent-to-Agent protocol  
- **AWS Bedrock** – LLM hosting  
- **Boto3** – AWS SDK for Python  
- **Dotenv** – Environment variable loading  

---

## 📂 Project Structure
```
itineraryPlanner/
│-- app.py              # Main Streamlit app
│-- requirements.txt    # Dependencies
│-- .env                # AWS credentials & region
│-- test_app.py              # Unit tests
│-- README.md           # Documentation
│-- .gitignore          # Ignored files
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/aishu136/wandermind-ai.git
cd wandermind-ai
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .venv
```

### 3️⃣ Activate the virtual environment

**Windows**
```bash
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

### 4️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 5️⃣ Configure AWS credentials  
Create a `.env` file in the root directory:
```ini
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```
> Make sure your AWS account has Bedrock access and is allowed to use the chosen models.

---

## ▶️ Running the Application
```bash
streamlit run app.py
```
Then open the URL provided in the terminal (usually [http://localhost:8501](http://localhost:8501)).

---

## 🧪 Running Tests
```bash
pytest test_app.py
```

---

## 📌 Example Usage
1. Enter destinations:  
   ```
   Paris, Rome
   ```
2. Enter travel dates:  
   ```
   2025-09-10 to 2025-09-17
   ```
3. Set budget:  
   ```
   2000
   ```
4. Add interests:  
   ```
   history, art, food
   ```
5. Click **Generate Itinerary** and download your plan.

---

## ⚠️ Common Issues
- **`AccessDeniedException`**  
  Your AWS account doesn't have access to the selected Bedrock model.  
  Enable the model in **AWS Console → Bedrock → Model Access**.

- **`ModuleNotFoundError`**  
  Install missing dependencies:
  ```bash
  pip install -r requirements.txt
  ```

- **`NameError: BedrockChat`**  
  Ensure you are using the correct import for Bedrock models.

---

## 📜 License
This project is licensed under the **MIT License**.
