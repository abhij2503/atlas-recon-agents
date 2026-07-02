import requests

def write_report(findings):

    # --- 1. Gather all four findings into one text block for the AI ---
    all_findings_text = ""
    for name, data in findings.items():
        all_findings_text += f"{data['atlas_id']} {data['atlas_name']}: {data['finding']}\n\n"

    # --- 2. Ask the AI for an executive summary of the whole picture ---
    prompt = f"You are a security analyst. Here are four reconnaissance findings about a public AI model, each mapped to a MITRE ATLAS technique:\n\n{all_findings_text}\nWrite a short executive summary (3-4 sentences) of the overall attack surface these findings reveal."

    answer = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.1:8B", "prompt": prompt, "stream": False}
    )
    summary = answer.json()["response"]
    
    score_prompt = f"Based on these reconnaissance findings about a public AI model:\n\n{all_findings_text}\nGive ONLY a single attack surface score from 0 to 10 (where 10 is most exposed), followed by one sentence of justification. Format: 'Score: X/10 - justification'."
    score_answer = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.1:8B", "prompt": score_prompt, "stream": False}
        )
    attack_score = score_answer.json()["response"]

    # --- 3. Build the markdown report text ---
    report = "# ATLAS Reconnaissance Intelligence Report\n\n"
    report += "**Target:** google-bert/bert-base-uncased\n\n"
    report += "## Executive Summary\n\n"
    report += summary + "\n\n"
    report += "## Attack Surface Score\n\n"
    report += attack_score + "\n\n"
    report += "## Most Critical Finding\n\n"
    report += "The single most critical finding is **[AML.T0004] Search Application Repositories** — the downloadable model files. Unlike the other findings, which only allow external observation, the complete weights (model.safetensors, pytorch_model.bin), architecture (config.json), and tokenizer are downloadable, giving an attacker a full offline copy of the model for unlimited white-box analysis and adversarial-example development.\n\n"
    report += "## Findings by ATLAS Technique\n\n"

    for name, data in findings.items():
        report += f"### [{data['atlas_id']}] {data['atlas_name']}\n\n"
        report += f"**Concrete evidence found:** {data['evidence']}\n\n"
        report += data["finding"] + "\n\n"

    # --- 4. Save it to a file ---
    with open("output/atlas_recon_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("Report written to output/atlas_recon_report.md")