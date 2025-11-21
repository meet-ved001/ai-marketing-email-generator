# app/agents/email_agent.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings

# Main LLM for generating emails
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.9,
    api_key=settings.openai_api_key
)

# Second LLM for scoring emails (can be same model)
scorer_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,     # deterministic scoring
    api_key=settings.openai_api_key
)

def run_email_graph(data: dict):
    """
    Generates a marketing email and ALSO scores it (0.0–1.0)
    using a second LLM call.
    """

    # === 1️⃣ Build prompt for email generation ===
    prompt_text = (
        f"Product Name: {data['product_name']}\n"
        f"Description: {data['product_description']}\n"
        f"Audience: {data['audience']}\n"
        f"Tone: {data['tone']}\n"
        f"Goal: {data['goal']}\n"
        f"Write {data.get('iterations',1)} marketing email(s).\n\n"
        "Include a clear subject line that starts with 'Subject:'."
    )

    messages = [
        SystemMessage(content="You are an AI that writes high-converting marketing emails."),
        HumanMessage(content=prompt_text)
    ]

    # === 2️⃣ First LLM call → Generate Email ===
    response = llm.invoke(messages)
    email_text = response.content.strip()
    clean_body = response.content.encode('utf-8').decode('unicode_escape')

    # Extract subject + body
    subject = f"Marketing Email for {data['product_name']}"
    body = clean_body

    if "Subject:" in email_text:
        try:
            parts = email_text.split("Subject:", 1)[1].split("\n", 1)
            subject = parts[0].strip()
            if len(parts) > 1:
                body = parts[1].strip()
        except:
            pass  # fallback to defaults

    # === 3️⃣ Second LLM call → Score the Email ===
    score_prompt = [
        SystemMessage(content="You are an expert marketing evaluator."),
        HumanMessage(
            content=(
                f"Score the following email on how persuasive it is for the goal '{data['goal']}'.\n"
                "Return ONLY a number between 0.0 and 1.0.\n\n"
                f"Email:\n{body}"
            )
        )
    ]

    score_response = scorer_llm.invoke(score_prompt)

    # Parse numeric score safely
    try:
        score_value = float(score_response.content.strip())
    except:
        score_value = 0.5  # fallback if parsing fails

    # === 4️⃣ Return structured output ===
    return {
        "subject": subject,
        "body": body,
        "score": score_value,
        
    }
