import re


def parse_agent_output(raw: str) -> dict:
    """Parse the supervisor agent's text output into structured fields."""
    result = {
        "decision": "UNKNOWN",
        "score": "N/A",
        "summary": "",
        "skill_fit": "",
        "experience_fit": "",
        "salary_fit": "",
    }
    if not raw:
        return result

    m = re.search(r"DECISION\s*:\s*([A-Z]+)", raw, re.IGNORECASE)
    if m:
        result["decision"] = m.group(1).upper()

    m = re.search(r"SCORE\s*:\s*(\d+)\s*/\s*100", raw, re.IGNORECASE)
    if m:
        result["score"] = m.group(1)

    sections = {
        "summary":        r"Summary\s*:(.*?)(?=Skill fit\s*:|Experience fit\s*:|Salary fit\s*:|$)",
        "skill_fit":      r"Skill fit\s*:(.*?)(?=Experience fit\s*:|Salary fit\s*:|$)",
        "experience_fit": r"Experience fit\s*:(.*?)(?=Salary fit\s*:|$)",
        "salary_fit":     r"Salary fit\s*:(.*?)$",
    }
    for key, pat in sections.items():
        m = re.search(pat, raw, re.IGNORECASE | re.DOTALL)
        if m:
            result[key] = m.group(1).strip()

    return result
