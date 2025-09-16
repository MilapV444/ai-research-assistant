🧠 AI Research Assistant




Live Demo: 🚀 Try it here

An AI-powered research assistant that helps users search the web, analyze documents, and get context-aware answers. Built with LangChain, LangGraph, and deployed on Streamlit Cloud.

✨ Features

🔍 Web Search Agent – fetches real-time info using DuckDuckGo API.

📄 Document Q&A – upload PDFs or text files and query them intelligently.

🧠 Contextual Memory – remembers past interactions for smoother conversations.

⚡ LangGraph Workflow – structured state management for multi-step reasoning.

🌐 Streamlit Interface – clean and interactive UI for end users.

🏗️ Architecture
<code>ai_research_assistant/
│── support_agent/          # Core agent logic
│   ├── state.py            # Defines agent state
│   ├── memory.py           # Conversation memory
│   ├── tools.py            # Web search + doc Q&A tools
│   ├── graph.py            # LangGraph workflow
│   └── __init__.py
│
│── main.py                 # CLI entrypoint
│── app.py                  # Streamlit web app
│── requirements.txt        # Project dependencies
│── README.md               # Project documentation
│── .gitignore              # Ignore sensitive files
│── LICENSE                 # MIT License
</code>


⚙️ Setup
1. Clone the repo
<code>git clone https://github.com/your-username/ai-research-assistant.git
cd ai-research-assistant
</code>


2. Create virtual environment
<code>python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
</code>


3. Install dependencies
<code>pip install -r requirements.txt
</code>


4. Add your API key

Create a .env file in the project root:

OPENAI_API_KEY="your_api_key_here"

▶️ Run the App
CLI mode
<code>
python main.py
</code>

Streamlit app
<code>
streamlit run app.py
</code>

📸 Demo Screenshot



📚 Usage Examples

Example 1 – Web Search

User: What is the latest research on quantum computing?  
AI: Found 3 recent papers and summarized their findings...  


Example 2 – Document Q&A

User: Uploads a PDF research paper  
User: What does this paper say about reinforcement learning?  
AI: The paper highlights that RL improves sample efficiency...  

📜 License

This project is licensed under the MIT License – see the LICENSE
 file for details.
