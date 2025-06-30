# Creating CTF Maps

## Requirements

Each CTF map submission must include:

1. **Frontend** - A web application serving the map (This is Optional if Flags are not "Front-Dependent" + having at least a LandPage for each map with proper writings and ... is interesting)
2. **Flags Configuration** - JSON file defining tasks and expected answers  
3. **Agent Example** - Demonstration that flags are solvable

## Directory Structure

```
your_map_name/
├── frontend/
│   ├── server.py
│   ├── templates/
│   │   └── index.html
│   └── static/ (optional)
├── flags.json
├── agent_example.py
└── README.md
```

## Frontend Requirements

- Must serve on port 8000
- Should provide an engaging interface for agents to interact with
- Can be a simple landing page or complex interactive application

## Flags Configuration Format

```json
[
  {
    "task": "Description of what the agent needs to find",
    "answer": "Expected exact answer"
  }
]
```

## Agent Example

- Must demonstrate that all flags are solvable
- Should use the provided template structure
- Must successfully extract all flag answers

## Testing

Use the validation utility:
```bash
python utils/validate_map.py your_map_name/
``` 
