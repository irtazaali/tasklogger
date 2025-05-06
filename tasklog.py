#!/usr/bin/env python3
"""
tasklog - A command-line tool for logging and querying tasks.

This tool allows users to log tasks with dates and hours spent, and to query
the task log using natural language via Ollama.
"""

import argparse
import csv
import datetime
import json
import os
import sys
import requests
from typing import Dict, List, Optional, Any

# Constants
CSV_FILE = "tasklog.csv"
CSV_HEADERS = ["timestamp", "date", "task", "hours"]
OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

def setup_argparse() -> argparse.ArgumentParser:
    """Set up and return the argument parser for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Log and query tasks from the command line."
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task to the log")
    add_parser.add_argument("task", help="Description of the task")
    add_parser.add_argument(
        "--date", 
        help="Date of the task in YYYY-MM-DD format (defaults to today)",
        default=datetime.date.today().isoformat()
    )
    add_parser.add_argument(
        "--hours", 
        type=float, 
        help="Hours spent on the task (defaults to 0.0)",
        default=0.0
    )
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query tasks using natural language")
    query_parser.add_argument("question", help="Natural language question about tasks")
    query_parser.add_argument(
        "--model",
        help=f"Ollama model to use (defaults to {DEFAULT_MODEL})",
        default=DEFAULT_MODEL
    )
    
    return parser

def validate_args(args: argparse.Namespace) -> bool:
    """Validate command-line arguments."""
    if args.command == "add":
        # Validate date format
        try:
            datetime.date.fromisoformat(args.date)
        except ValueError:
            print(f"Error: Invalid date format. Please use YYYY-MM-DD format.")
            return False
        
        # Validate hours
        if args.hours < 0:
            print("Error: Hours must be a non-negative number.")
            return False
    
    return True

def ensure_csv_exists() -> None:
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(CSV_HEADERS)

def add_task(task: str, date: str, hours: float) -> None:
    """Add a new task to the CSV file."""
    ensure_csv_exists()
    
    timestamp = datetime.datetime.now().isoformat()
    
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, date, task, hours])
    
    print(f"Task added: '{task}' on {date} ({hours} hours)")

def read_tasks() -> List[Dict[str, Any]]:
    """Read all tasks from the CSV file and return as a list of dictionaries."""
    ensure_csv_exists()
    
    tasks = []
    with open(CSV_FILE, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert hours to float
            row['hours'] = float(row['hours'])
            tasks.append(row)
    
    return tasks

def query_tasks_with_ollama(question: str, tasks: List[Dict[str, Any]], model: str) -> str:
    """
    Query tasks using Ollama's language model.
    
    Args:
        question: The natural language question about tasks
        tasks: List of task dictionaries
        model: The Ollama model to use
        
    Returns:
        The response from Ollama
    """
    # Format tasks data as a string
    tasks_data = "Task data:\n"
    for i, task in enumerate(tasks, 1):
        tasks_data += f"{i}. Date: {task['date']}, Hours: {task['hours']}, Task: {task['task']}\n"
    
    # Create the prompt for Ollama
    prompt = f"""
You are a helpful assistant analyzing task log data. Please answer the following question based on the task data provided.

{tasks_data}

Question: {question}

Please provide a clear and concise answer based only on the task data provided.
"""
    
    # Prepare the request payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        # Make the API request to Ollama
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the response
        result = response.json()
        return result.get("response", "No response received from Ollama.")
    
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama. Make sure Ollama is running (ollama serve)."
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {str(e)}"
    except json.JSONDecodeError:
        return "Error: Received invalid response from Ollama."

def query_tasks(question: str, model: str = DEFAULT_MODEL) -> None:
    """
    Query tasks using natural language via Ollama.
    
    Args:
        question: The natural language question about tasks
        model: The Ollama model to use
    """
    tasks = read_tasks()
    
    if not tasks:
        print("No tasks found in the log.")
        return
    
    print(f"Querying tasks using Ollama model '{model}'...")
    print(f"Question: {question}\n")
    
    # Get response from Ollama
    response = query_tasks_with_ollama(question, tasks, model)
    
    # Print the response
    print("\nOllama Response:")
    print(response)

def main() -> None:
    """Main entry point for the tasklog tool."""
    parser = setup_argparse()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if not validate_args(args):
        sys.exit(1)
    
    if args.command == "add":
        add_task(args.task, args.date, args.hours)
    elif args.command == "query":
        query_tasks(args.question, args.model)

if __name__ == "__main__":
    main()
