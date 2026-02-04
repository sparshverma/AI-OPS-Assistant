# AI Operations Assistant 🤖

A multi-agent AI system capable of planning, executing, and verifying tasks using GitHub and Weather APIs. This project demonstrates a **Planner-Executor-Verifier** architecture where LLM agents collaborate to solve user requests.

## 🏗 Architecture

The system follows a three-stage pipeline:

1.  **Planner Agent 🧠**: Analyzes the natural language request and generates a structured JSON execution plan.
2.  **Executor Agent 🛠️**: Parses the plan and executes specific tools (GitHub, Weather) to gather data.
3.  **Verifier Agent ✅**: Synthesizes the execution results into a final, user-friendly natural language response.

### Available Tools
*   `github_tool`: Fetches repository stars, descriptions, and metadata.
*   `weather_tool`: Fetches real-time weather data for any city.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.8 or higher
*   OpenAI API Key
*   OpenWeatherMap API Key
*   GitHub Personal Access Token

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/sparshverma/AI-OPS-Assistant.git
    cd AI-OPS-Assistant
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**
    Create a `.env` file in the root directory (copy from `.env.example`) and add your credentials:
    ```ini
    OPENAI_API_KEY=your_openai_key_here
    OPENWEATHER_API_KEY=your_weather_key_here
    GITHUB_TOKEN=your_github_token_here
    ```

---

## 💻 Usage

### Web Interface (Recommended)
Launch the modern web interface to interact with the assistant.

```bash
python run_web.py
```
*   The application will automatically attempt to open your browser.
*   Access manually at: `http://localhost:8081`

### Command Line Interface
For quick testing or headless environments:

```bash
python main.py
```

---

## 📂 Project Structure

```
├── agents/             # Agent logic (Planner, Executor, Verifier)
├── llm/                # LLM client configuration
├── tools/              # Tool implementations (GitHub, Weather)
├── web_interface/      # FastAPI app and static assets
├── main.py             # CLI entry point
├── run_web.py          # Web entry point
└── requirements.txt    # Project dependencies
```

## 🛠 Features & Capabilities

*   **Natural Language Processing**: Understands complex intents like "Check react stars and weather in Menlo Park".
*   **Robust Error Handling**: Agents gracefully handle tool failures or API errors.
*   **Web Dashboard**: Clean, responsive UI for interacting with the agents.
*   **Extensible**: Easily add new tools to `tools/` and register them in `agents/executor.py`.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

---

**Disclaimer**: This is a demonstration project for agentic workflows. Ensure you manage your API keys securely.




