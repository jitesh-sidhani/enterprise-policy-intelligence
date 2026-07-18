from agents.generator import get_llm


SYSTEM_PROMPT = """
You are an Enterprise Router Agent.

Your ONLY responsibility is to classify the user's question.

Choose EXACTLY ONE category from:

HR
Finance
IT
AI Governance
General Policy

Classification Rules:

HR:
- Leave
- Attendance
- Dress code
- Holidays
- Working hours
- Employees
- Office rules
- Maternity
- Sick leave

Finance:
- Travel reimbursement
- Expenses
- Claims
- Salary
- Allowances
- Payroll

IT:
- Password reset
- Email
- Laptop
- VPN
- Computer
- Software access

AI Governance:
- ChatGPT
- LLM
- AI usage
- Copilot
- AI ethics
- AI security

General Policy:
- Anything related to company policies that doesn't fit above.

Return ONLY the category name.

No explanation.
No punctuation.
No markdown.
"""


def route_question(question: str):

    llm = get_llm()

    prompt = f"""
{SYSTEM_PROMPT}

User Question:

{question}
"""

    response = llm.invoke(prompt)

    return response.content.strip()