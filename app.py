import gradio as gr

from agents.generator import get_llm
from agents.retriever import retrieve_context
from agents.router import route_question
from agents.safety import safety_check
from agents.verifier import verify_answer

def ask(question):

    # -----------------------------
    # 1. Safety Agent
    # -----------------------------
    safe, reason = safety_check(question)

    if not safe:
        return f"❌ {reason}"

    # -----------------------------
    # 2. Router Agent
    # -----------------------------
    department = route_question(question)

    # -----------------------------
    # 3. Retriever Agent
    # -----------------------------
    context = retrieve_context(question)

    # print("\n================ CONTEXT ================\n")
    # print(context)
    # print("\n==========================================\n")

    # -----------------------------
    # 4. Generator Agent
    # -----------------------------
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

    # print(prompt)

    response = llm.invoke(prompt)

    # print(response.content)

    answer = response.content.strip()

# -----------------------------
# 5. Verifier Agent
# -----------------------------
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


# -----------------------------
# Final Response
# -----------------------------

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


css = """
/* Hide Gradio footer */
footer {
    display: none !important;
}

/* Improve textarea readability */
textarea {
    font-size: 17px !important;
    line-height: 1.6 !important;
}

/* Better markdown readability */
.markdown {
    line-height: 1.7;
}

/* Slightly rounded buttons */
button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

#question-card,
#response-card {

    border-radius: 16px;

    border: 1px solid #3b3b45;

    padding: 18px;

    background: #23232b;
}
"""





with gr.Blocks(
    title="Enterprise Policy Intelligence",
    css=css
) as demo:

    gr.HTML("""
<div style="text-align:center; padding:25px;">

<h1 style="font-size:46px; margin-bottom:10px;">
🏢 Enterprise Policy Intelligence
</h1>

<p style="font-size:20px; color:#9CA3AF;">
Multi-Agent Enterprise Policy Intelligence Platform
</p>

<p style="font-size:16px; color:#7A7A7A;">
Powered by RAG • LangChain • Groq • FAISS
</p>

</div>
""")

    with gr.Row(equal_height=True):

        # Left Column
        with gr.Column(scale=1):

            with gr.Group(elem_id="question-card"):

                gr.Markdown("## 📝 Ask Policy Question")

                question = gr.Textbox(
                    placeholder="Example: How many annual leave days do permanent managers receive?",
                    lines=3,
                    show_label=False
                )

                with gr.Row():
                    clear = gr.Button("Clear", variant="secondary")
                    submit = gr.Button("Submit", variant="primary")

            
            with gr.Group(elem_id="pipeline-card"):
                gr.Markdown("## 🤖 Agent Pipeline")
                gr.Markdown("""
🟢 **Safety Agent**
- Checks if the question is safe and policy-related.

⬇️

🟢 **Router Agent**
- Classifies the question into the correct department.

⬇️

🟢 **Retriever Agent**
- Retrieves relevant policy context using semantic search.

⬇️

🟢 **Generator Agent**
- Generates an answer only from the retrieved context.

⬇️

🟢 **Verifier Agent**
- Verifies the answer against the retrieved policy.
""")


        # Right Column
        with gr.Column(scale=1):

            with gr.Group(elem_id="question-card"):

                gr.Markdown("## 🤖 AI Response")

                output = gr.Markdown(
                    container=True
                )

            flag = gr.Button(
                "🚩 Flag Response",
                variant="secondary"
            )

    # Event handlers
    submit.click(
        fn=ask,
        inputs=question,
        outputs=output
    )

    question.submit(
        fn=ask,
        inputs=question,
        outputs=output
    )

    clear.click(
        lambda: ("", ""),
        outputs=[question, output]
    )

demo.launch()