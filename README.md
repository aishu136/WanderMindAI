# ✈️ WanderMind AI – AI-Powered Travel Itinerary Designer

WanderMind AI is an interactive **Streamlit** application that uses **LangGraph** multi-agent workflows and **AWS Bedrock** LLMs to design personalized travel itineraries based on destinations, budget, dates, and interests.

## 🚀 Features
- **Multi-Agent Workflow** with LangGraph
- **AWS Bedrock Models** for research, budget optimization, and itinerary composition
- **Interactive Streamlit UI**
- **Downloadable Itinerary** in plain text
- **Customizable** destinations, dates, budget, and interests

## 🛠 Tech Stack
- **Python 3.10+**
- **Streamlit** – Web UI
- **LangGraph** – Agent-to-Agent protocol
- **AWS Bedrock** – LLM hosting
- **Boto3** – AWS SDK for Python
- **Dotenv** – Environment variable loading

## 📂 Project Structure
itineraryPlanner/
│-- app.py # Main Streamlit app
│-- requirements.txt # Dependencies
│-- .env # AWS credentials & region

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/wandermind-ai.git
cd wandermind-ai
Create a virtual environment

bash
Copy
Edit
python -m venv .venv
Activate the virtual environment

Windows

bash
Copy
Edit
.venv\Scripts\activate
macOS/Linux

bash
Copy
Edit
source .venv/bin/activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Configure AWS credentials in a .env file:

ini
Copy
Edit
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
Make sure your AWS account has Bedrock access and is allowed to use the chosen models.

▶️ Running the Application
bash
Copy
Edit
streamlit run app.py
Open the URL provided in the terminal (usually http://localhost:8501).

🧪 Running Tests
bash
Copy
Edit
pytest
📌 Example Usage
Enter destinations: Paris, Rome

Enter travel dates: 2025-09-10 to 2025-09-17

Set budget: 2000

Add interests: history, art, food

Click Generate Itinerary and download your plan.

⚠️ Common Issues
AccessDeniedException: Your AWS account doesn't have access to the selected Bedrock model. Enable the model in the AWS Console → Bedrock → Model Access.

ModuleNotFoundError: Install missing dependencies with pip install -r requirements.txt.

NameError: BedrockChat: Ensure you are using the correct import for Bedrock.

📜 License
This project is licensed under the MIT License.


│-- README.md # Project documentation
