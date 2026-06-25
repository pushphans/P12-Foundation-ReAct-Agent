# 🤖 Foundation ReAct Agent

A production-ready **ReAct (Reasoning + Acting)** AI agent built with **LangGraph** and exposed via a **FastAPI** REST endpoint. The agent autonomously reasons over user queries, selects appropriate tools, and returns structured responses — demonstrating the foundational agentic loop pattern used in real-world GenAI systems.

---

## 📌 What Is This?

This project implements the **ReAct pattern** from scratch using LangGraph's `StateGraph`. The agent follows a Thought → Action → Observation loop:

1. **Reason** — The LLM (GPT-4o-mini) receives the user query and decides whether to call a tool or respond directly.
2. **Act** — If a tool is needed, `ToolNode` executes it and returns the result as an observation.
3. **Repeat or Respond** — The agent iterates until it has enough context to generate a final answer.

The entire workflow is wired into a **FastAPI endpoint** (`POST /agent`), making it easy to integrate with any frontend or backend service.

---

## 🗂️ Project Structure

```
P12-Foundation-ReAct-Agent/
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── api/
│   │   └── router.py          # POST /agent endpoint
│   ├── agent/
│   │   ├── graph.py           # LangGraph StateGraph (ReAct loop)
│   │   └── tools.py           # Tool definitions (get_weather, get_flight_price)
│   ├── core/
│   │   └── config.py          # Pydantic settings (env vars)
│   └── models/
│       └── agent.py           # AgentRequest / AgentResponse schemas
├── requirements.txt
├── pyproject.toml
├── .python-version            # Python 3.12
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | GPT-4o-mini via LangChain `init_chat_model` |
| API Server | FastAPI + Uvicorn |
| Settings Management | Pydantic Settings v2 |
| Package Manager | `uv` (lock file included) |
| Python Version | 3.12 |

---

## 🧠 Agent Architecture

```
User Query (POST /agent)
        │
        ▼
  ┌─────────────┐
  │  react_node  │  ← LLM with bound tools
  └──────┬──────┘
         │
   tools_condition
    ┌────┴────┐
    │         │
    ▼         ▼
tool_node    END
    │
    └──► react_node  (loop back until done)
```

The graph uses `tools_condition` from LangGraph's prebuilt module to route between calling a tool and ending the conversation. The state is a simple `TypedDict` with an `Annotated[list[AnyMessage], add_messages]` field — messages accumulate across the loop automatically.

---

## 🛠️ Available Tools

### `get_weather(location: str) → str`
Returns current weather for a given city.

```
Jammu    → "35°C and Sunny"
Delhi    → "40°C and Hot"
Srinagar → "22°C and Pleasant"
```

### `get_flight_price(source: str, destination: str) → str`
Returns cheapest flight price between two cities.

```
Jammu → Srinagar → "₹3500 via Air India Express"
```

> Both tools are registered in `tools_list` and bound to the LLM via `.bind_tools()` and passed to `ToolNode`.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- `uv` package manager (recommended) or `pip`
- OpenAI API key

### 1. Clone the Repository

```bash
git clone https://github.com/pushphans/P12-Foundation-ReAct-Agent.git
cd P12-Foundation-ReAct-Agent
```

### 2. Set Up Environment

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## 📡 API Reference

### `POST /agent`

Runs the ReAct agent with the provided query.

**Request Body**

```json
{
  "query": "What is the weather in Jammu?"
}
```

**Response**

```json
{
  "response": "The current weather in Jammu is 35°C and Sunny."
}
```

**Example with `curl`**

```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the cheapest flight from Jammu to Srinagar?"}'
```

**Interactive Docs**

FastAPI's built-in Swagger UI is available at `http://localhost:8000/docs`.

---

## 🔑 Key Concepts Demonstrated

- **ReAct Pattern** — Interleaved reasoning and tool-calling loop without any manual orchestration logic.
- **LangGraph StateGraph** — Declarative graph with conditional edges (`tools_condition`) for dynamic routing.
- **LangChain Tool Decorator** — `@tool` for converting plain Python functions into LLM-callable tools.
- **ToolNode** — Prebuilt LangGraph node that handles tool dispatch and observation injection automatically.
- **Pydantic v2 Settings** — Type-safe environment variable loading via `pydantic-settings`.
- **FastAPI + Async** — Fully async endpoint using `await workflow.ainvoke(...)`.

---

## 🔧 Extending the Agent

### Add a New Tool

```python
# app/agent/tools.py

@tool
def get_hotel_price(city: str, check_in: str, check_out: str) -> str:
    """Get the cheapest hotel price in a city for given dates."""
    # Your logic here
    return f"Hotel in {city}: ₹2000/night"

# Add to tools_list
tools_list = [get_weather, get_flight_price, get_hotel_price]
```

The tool is automatically available to the LLM — no changes needed in `graph.py`.

### Swap the LLM

```python
# app/agent/graph.py

llm = init_chat_model(
    "claude-3-5-sonnet-20241022",
    model_provider="anthropic",
    api_key=settings.ANTHROPIC_API_KEY
)
```

---

## 📦 Dependencies

```
langchain
langchain-openai
langchain-core
langgraph
fastapi
uvicorn
pydantic-settings
geopy
```

---

## 🗺️ Roadmap

- [ ] Replace mock tool implementations with real API integrations (OpenWeatherMap, Skyscanner)
- [ ] Add conversation memory / multi-turn support
- [ ] Add LangSmith tracing for observability
- [ ] Dockerize the service
- [ ] Add streaming response support via Server-Sent Events

---

## 👨‍💻 Author

**Pushp Hans**
AI Engineer | LangGraph · FastAPI · Flutter

- GitHub: [@pushphans](https://github.com/pushphans)

---

## 📄 License

This project is open source. Feel free to fork, modify, and build on it.
