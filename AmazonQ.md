# TaskLogger Ollama Integration

## Overview

This document describes the integration of Ollama with the TaskLogger tool to enable natural language queries of task data.

## Implementation Details

The TaskLogger tool now uses Ollama, a local LLM server, to process natural language queries about task data. This implementation:

1. Connects to a locally running Ollama server at `http://localhost:11434/api/generate`
2. Formats task data and user questions into a prompt for the LLM
3. Processes the response and displays it to the user

## Requirements

- Python 3.6+
- Ollama installed and running locally
- `requests` Python package

## Usage

### Starting Ollama

Before using the natural language query feature, make sure Ollama is running:

```bash
ollama serve
```

### Querying Tasks

```bash
# Query tasks using the default model (llama3)
./tasklog.py query "How many hours did I spend on meetings last week?"

# Query tasks using a specific model
./tasklog.py query "Show me all tasks from yesterday" --model mistral
```

## Available Models

The default model is `llama3`, but you can use any model that you have pulled to your Ollama installation:

```bash
# List available models
ollama list

# Pull a new model
ollama pull mistral
```

## Customization

You can modify the prompt template in the `query_tasks_with_ollama` function to improve the quality of responses for your specific use case.

## Troubleshooting

If you encounter errors:

1. Ensure Ollama is running with `ollama serve`
2. Check that you have the requested model installed with `ollama list`
3. Verify network connectivity to the Ollama API endpoint
