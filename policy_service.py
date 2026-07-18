from agents.generator import get_llm
from agents.retriever import retrieve_context
from agents.router import route_question
from agents.safety import safety_check
from agents.verifier import verify_answer


def ask(question):

    print("=" * 60)
    print("QUESTION:", question)

    safe, reason = safety_check(question)

    if not safe:
        return f"❌ {reason}"

    department = route_question(question)

    context = retrieve_context(question)

    llm = get_llm()

    prompt = f"""
You are an Enterprise Policy Assistant.

The Router Agent classified this question as:

Department: {department}

Your job is to answer ONLY using the retrieved policy context.

Rules:

- Never use outside knowledge.
- Never guess.
- Never invent company policies.
- If the retrieved context does not contain enough information,
  reply exactly:

"I couldn't find this information in the uploaded policy."

Retrieved Context:
{context}

User Question:
{question}
"""

    response = llm.invoke(prompt)

    answer = response.content.strip()

    verification = verify_answer(
        question=question,
        context=context,
        answer=answer
    )

    if verification.verified:
        final_answer = answer
    else:
        final_answer = f"""
⚠️ Verification Failed

Generated Answer:
{answer}

Reason:
{verification.reason}
"""

    return f"""
### 🏢 Department
**{department}**

---

### {"✅ Verified" if verification.verified else "❌ Verification Failed"}

**Reason:** {verification.reason}

---

### 💬 Answer

{final_answer}
"""