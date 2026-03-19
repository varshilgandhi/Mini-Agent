# Mini Agent Orchestrator

## Architecture
- Planner: Mock LLM converts user input into steps
- Orchestrator: Executes steps sequentially
- Tools: cancel_order and send_email (async)

## Features
- Async execution
- Failure handling (20% failure simulation)
- Simple agent workflow

## How to Run
pip install fastapi uvicorn  
uvicorn main:app --reload

## Example Request
POST /agent
{
  "query": "Cancel my order 9921 and send email"
}