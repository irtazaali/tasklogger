# TaskLogger

A simple command-line tool for logging and querying tasks. Integration of Ollama to enable natural language queries of task data

## Features

- Log tasks with dates and time spent
- Query task history using natural language
- CSV-based storage for simplicity and portability

## Installation

No installation required. Just make sure the script is executable:

```bash
chmod +x tasklog.py
```

## Requirements

- Python 3.6+
- Ollama installed and running locally
- `requests` Python package

## Usage

### Adding a task

```bash
# Add a task for today with default 0.0 hours
./tasklog.py add "Implemented new feature"

# Add a task with a specific date
./tasklog.py add "Code review" --date 2025-05-05

# Add a task with hours spent
./tasklog.py add "Bug fixing" --hours 2.5

# Add a task with both date and hours
./tasklog.py add "Team meeting" --date 2025-05-06 --hours 1.5
```

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


## Data Storage

Tasks are stored in a CSV file named `tasklog.csv` in the current working directory with the following columns:

- `timestamp`: ISO timestamp when the task was logged
- `date`: Date of the task in YYYY-MM-DD format
- `task`: Description of the task
- `hours`: Hours spent on the task (decimal)




