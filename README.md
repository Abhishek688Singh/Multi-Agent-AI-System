# Multi-Agent AI Research System

An open-source research workspace that turns a topic into a sourced research draft and critique. The Streamlit interface exposes a four-stage AI workflow for searching, reading, writing, and reviewing research.

> **Important:** Generated content is a starting point for research. Verify sources, claims, and citations before using the output academically or professionally.

## Features

- Search the web for recent information about a research topic.
- Select and scrape a relevant source for detailed content.
- Generate a structured research paper.
- Review the draft with an AI critic.
- Inspect progress, source material, the draft, and critique in a Streamlit UI.

## Architecture

The application is organized as a sequential four-stage pipeline:

```text
Streamlit UI (app.py)
        |
        v
Research pipeline (src/pipeline/pipeline.py)
        |
        +--> Search agent  --> LangSearch web-search API
        |
        +--> Reader agent  --> Web page fetching and text extraction
        |
        +--> Writer chain  --> Structured research-paper draft
        |
        +--> Critic chain  --> Draft quality review
```

### Main components

- `app.py` - Streamlit application, session state, progress reporting, and results display.
- `src/pipeline/pipeline.py` - Orchestrates the four workflow stages and returns the research result.
- `src/agents/agents.py` - Configures the Gemini model, search and reader agents, writer chain, and critic chain.
- `src/tools/tools.py` - Provides the LangSearch integration and webpage scraping tool.

## Technologies

- **Python 3.12+**
- **Streamlit** for the web interface
- **LangChain** and **LangGraph** for agents and chains
- **Google Gemini** through `langchain-google-genai`
- **LangSearch API** for web search
- **Requests**, **BeautifulSoup**, and **Trafilatura/readability** for web content extraction
- **python-dotenv** for local environment configuration
- **uv** for dependency and environment management

## Prerequisites

Install the following before starting:

1. Python 3.12 or newer
2. A Google Gemini API key
3. A LangSearch API key
4. Git

## Installation

### Option 1: uv (recommended)

Clone the repository and create the project environment:

```bash
git clone https://github.com/Abhishek688Singh/Multi-Agent-AI-System.git
cd Multi-Agent-AI-System
uv sync
```

### Option 2: pip and virtualenv

```bash
git clone https://github.com/Abhishek688Singh/Multi-Agent-AI-System.git
cd Multi-Agent-AI-System

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key
LANG_SEARCH_API_KEY=your_langsearch_api_key
```

Never commit `.env` or expose API keys in source code. The application loads these values with `python-dotenv`.

## Running the application

With uv:

```bash
uv run streamlit run app.py
```

With an activated virtual environment:

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Using the application

1. Enter a focused research topic.
2. Select **Start research**.
3. Follow the four stages in the progress panel.
4. Review the generated paper, source material, and critic feedback.
5. Edit or download the draft for further verification and revision.

## Project layout

```text
.
├── app.py
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── agents/
│   │   └── agents.py
│   ├── pipeline/
│   │   └── pipeline.py
│   └── tools/
│       └── tools.py
└── README.md
```

## Development

Run a syntax check before opening a pull request:

```bash
python3 -m py_compile app.py src/agents/agents.py src/pipeline/pipeline.py src/tools/tools.py
```

When contributing, keep changes focused, update documentation for user-facing behavior, and avoid committing credentials or generated artifacts.

## Contributing

Contributions are welcome:

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Open a pull request with a clear description of the problem and solution.

For larger changes, open an issue first to discuss the proposed direction.

## License

No license file is currently included in this repository. Add an OSI-approved license before distributing the project for reuse.