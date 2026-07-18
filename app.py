import gradio as gr

from policy_service import ask


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

            with gr.Group():
                gr.Markdown("## 🤖 Agent Pipeline")
                gr.Markdown("""
🟢 **Safety Agent**

⬇️

🟢 **Router Agent**

⬇️

🟢 **Retriever Agent**

⬇️

🟢 **Generator Agent**

⬇️

🟢 **Verifier Agent**
""")

        # Right Column
        with gr.Column(scale=1):

            with gr.Group(elem_id="response-card"):

                gr.Markdown("## 🤖 AI Response")

                output = gr.Markdown(
                    container=True
                )

            flag = gr.Button(
                "🚩 Flag Response",
                variant="secondary"
            )

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