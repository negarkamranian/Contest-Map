# Example Map: Divar Marketplace

A sample CTF map featuring a mock marketplace where agents must extract information from product listings.

## Structure

- `frontend/` - Web server and templates
- `flags.json` - Contest flags and tasks
- `agent_example.py` - Feasibility demonstration agent
- `test_setup.py` - Automated test script

## Quick Test

Run the automated test to verify everything works:

```bash
python3 test_setup.py
```

## Manual Setup

### Prerequisites

1. Install dependencies (from project root):
   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key (choose one method):
   
   **Method A: Environment variable**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   **Method B: Create .env file**
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

### Running

1. Start the server:
   ```bash
   cd frontend
   python3 server.py
   ```
   Server will be available at: http://localhost:8000

2. Test the agent (in another terminal):
   ```bash
   cd example_map
   export OPENAI_API_KEY="your-api-key-here"
   python3 agent_example.py
   ```

## Task Description

The map contains **1 flag** that requires agents to:
- Parse HTML content from the marketplace
- Identify the first laptop listing
- Extract the numerical price value

**Expected behavior**: The agent should find the first laptop (ASUS VivoBook 15) and return its price: `35000000`

## Technical Details

- **Server**: FastAPI with Jinja2 templates
- **Agent**: Uses OpenAI GPT-4o-mini with Pydantic structured output
- **Task**: Price extraction from Persian/Farsi marketplace HTML
- **Validation**: Automatic comparison with expected answer

## Dependencies

All dependencies are listed in the root `requirements.txt`. 