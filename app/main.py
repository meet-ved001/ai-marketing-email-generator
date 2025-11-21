# app/main.py
from fastapi import FastAPI, HTTPException
from app.schemas import EmailRequest, EmailResponse, AgentStep
from app.agents.email_agent import run_email_graph
from app.db import init_db, SessionLocal, EmailGeneration
from app.config import settings
from contextlib import asynccontextmanager


# ✅ Use lifespan for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()  # initialize DB
    yield
    # Shutdown logic (optional)
    print("App shutting down...")

app = FastAPI(title="AI Marketing Email Agent", lifespan=lifespan)
@app.post("/generate-subject-lines")
def generate_subject_lines(req: EmailRequest):
    """
    Generates multiple catchy subject lines for A/B testing.
    """
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate

    try:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9, openai_api_key=settings.openai_api_key)
        prompt = ChatPromptTemplate.from_template(
            "Generate 5 catchy, short, and engaging email subject lines for a marketing email about {product_name}. "
            "Description: {product_description}. "
            "Audience: {audience}. Tone: {tone}. Goal: {goal}. "
            "Output them as a JSON list of strings."
        )

        chain = prompt | llm
        result = chain.invoke({
            "product_name": req.product_name,
            "product_description": req.product_description,
            "audience": req.audience,
            "tone": req.tone,
            "goal": req.goal
        })

        import json
        subjects = []
        try:
            subjects = json.loads(result.content)
        except:
            subjects = [line.strip("-• ") for line in result.content.split("\n") if line.strip()]

        return {"subject_lines": subjects[:5]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-email", response_model=EmailResponse)
def generate_email(req: EmailRequest):
    # Convert structured request to dict
    payload = req.dict()
    try:
        # Pass full dictionary to run_email_graph
        result = run_email_graph(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Persist result in SQLite
    db = SessionLocal()
    item = EmailGeneration(
        product_name=req.product_name,
        audience=req.audience,
        tone=req.tone,
        subject=result.get("subject", ""),
        body=result.get("body", ""),
        score=result.get("score", 0.0)
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()

    # Map steps for response
    steps = []
    for s in result.get("steps", []):
        steps.append(AgentStep(name=s.get("name", ""), output=str(s.get("output", ""))))

    return EmailResponse(
        subject=result.get("subject", ""),
        body=result.get("body", ""),
        score=result.get("score", 0.0),
        steps=steps
    )

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
