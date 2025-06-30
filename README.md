Current Contest Landpage: https://kaleidoscopic-chimera-5f72ff.netlify.app/

# CTF Map Template

A template for creating LLM Agent CTF contest maps.

## Overview

This template provides a standardized structure for contributors to create CTF contest "maps" where LLM agents compete to find hidden flags.

## Quick Start

1. **Clone this template**
2. **Create your map** in the `example_map/` directory
3. **Test your flags** using the provided agent example
4. **Submit your map** for the contest

## Structure

- `example_map/` - Complete example map implementation
- `docs/` - Documentation for map creators
- `utils/` - Validation and testing utilities

## Requirements

```bash
pip install -r requirements.txt
```

## Testing Your Map

```bash
# Quick test of the example map
python3 test_example.py

# Manual testing:
# 1. Start the server
cd example_map/frontend
python3 server.py

# 2. Test with agent (in another terminal)
cd example_map
python3 agent_example.py

# 3. Validate your map
python3 utils/validate_map.py example_map/
```

## Contributing

See `docs/creating_maps.md` for detailed instructions on creating your own maps. 
