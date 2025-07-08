# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware 
from backend.graph import create_graph
from backend.agents import roadmap_node, tutorial_node, exercise_node, review_node

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = create_graph()

@app.post("/tutor")
async def tutor_flow(req: Request):
    body = await req.json()
    topic = body.get("query")
    level = body.get("level", "beginner")  # default level if not provided
    user_id = body.get("user_id")
    code = body.get("code")

    if not topic or not user_id:
        return {"error": "Missing topic or user ID."}

    input_state = {
        "topic": topic,
        "level": level,
        "user_id": user_id,
        "code": code
    }

    try:
        output = graph.invoke(input_state)

        # Combine all outputs for frontend
        reply_parts = []
        for key in ["roadmap", "tutorial", "exercise", "review"]:
            if key in output and output[key]:
                reply_parts.append(f"### {key.capitalize()}:\n{output[key]}")

        return {
            "reply": "\n\n---\n\n".join(reply_parts),
            "raw": output
        }

    except Exception as e:
        return {"error": f"Graph error: {str(e)}"}
