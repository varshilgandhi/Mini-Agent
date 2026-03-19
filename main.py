from fastapi import FastAPI
import asyncio
import random

app = FastAPI()

#PLANNER (Mock LLM)
def planner(user_input: str):
    steps = []

    if "cancel" in user_input.lower():
        order_id = "9921"  # hardcoded for demo
        steps.append({
            "action": "cancel_order",
            "order_id": order_id
        })

    if "email" in user_input.lower():
        steps.append({
            "action": "send_email",
            "email": "user@example.com",
            "message": "Your order has been cancelled."
        })

    return steps


#TOOLS 
async def cancel_order(order_id: str):
    await asyncio.sleep(1)

    # simulate 20% failure
    if random.random() < 0.2:
        return {"success": False, "error": "Cancellation failed"}

    return {"success": True}


async def send_email(email: str, message: str):
    await asyncio.sleep(1)
    return {"success": True}


#ORCHESTRATOR 
async def execute_plan(plan):
    for step in plan:
        print(f"Executing: {step}")

        if step["action"] == "cancel_order":
            result = await cancel_order(step["order_id"])

            if not result["success"]:
                return {
                    "status": "failed",
                    "reason": result["error"]
                }

        elif step["action"] == "send_email":
            await send_email(step["email"], step["message"])

    return {"status": "success"}


#API
@app.post("/agent")
async def agent(request: dict):
    user_input = request.get("query", "")

    plan = planner(user_input)
    result = await execute_plan(plan)

    return {
        "plan": plan,
        "result": result
    }