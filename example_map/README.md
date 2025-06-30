# Example Map: Divar Marketplace

A sample CTF map featuring a mock marketplace where agents must extract information from product listings.

## Structure

- `frontend/` - Web server and templates
- `flags.json` - Contest flags and tasks
- `agent_example.py` - Feasibility demonstration agent

## Running

1. Start the server:
   ```bash
   cd frontend
   python server.py
   ```

2. Test the agent:
   ```bash
   python agent_example.py
   ```

## Flags

This map contains 1 flag that requires agents to:
- Parse HTML content
- Identify specific product information
- Extract numerical data

## Dependencies

All dependencies are listed in the root `requirements.txt`. 