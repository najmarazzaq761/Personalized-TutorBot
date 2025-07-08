from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq  # type: ignore
import os

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192",
    temperature=0.3
)

def roadmap_node(input):
    topic = input["topic"]
    level = input["level"]
    prompt = PromptTemplate.from_template("""
    Create an 8-week roadmap for learning {topic} at a {level} level.
    Include weekly topics and a short milestone project.
    Output in markdown table format.
    """)
    return {"roadmap": llm.invoke(prompt.format(topic=topic, level=level)).content}

def tutorial_node(input):
    topic = input["topic"]
    level = input["level"]
    prompt = PromptTemplate.from_template("""
    Generate a detailed tutorial for {topic} at a {level} level.
    Include:
    - Explanation
    - 2–3 simple code examples
    - Real-world analogy
    Format in markdown.
    """)
    return {"tutorial": llm.invoke(prompt.format(topic=topic, level=level)).content}

def exercise_node(input):
    topic = input["topic"]
    prompt = PromptTemplate.from_template("""
    Generate:
    - 1 coding challenge
    - 2 multiple choice quiz questions for topic: {topic}
    Format response in markdown with clear sections.
    """)
    return {"exercise": llm.invoke(prompt.format(topic=topic)).content}

def review_node(input):
    code = input.get("code")
    topic = input.get("topic")

    if not code or not topic:
        return {"review": "❗ Missing code or topic for review."}

    prompt = PromptTemplate.from_template("""
You are a code reviewer. Analyze the following code related to {topic}:

{code}

Return feedback in markdown:
- ✅ Correctness check
- 🧠 Style suggestions
- 🚀 Optimization tips
""")

    return {"review": llm.invoke(prompt.format(topic=topic, code=code)).content}
