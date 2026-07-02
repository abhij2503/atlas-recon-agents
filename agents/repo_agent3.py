from bs4 import BeautifulSoup
import requests

def run():
	with open("targets/bert_modelcard.html", encoding="utf-8") as f:
		raw = f.read()
	soup = BeautifulSoup(raw, "html.parser")   # make the soup
	text = soup.get_text()
	start = text.find("google-bert")
	owner_text = text[start : start + 80]
	prompt = f"A public AI model is published by this owner/organization: {owner_text}. In one sentence, why does knowing who publishes and maintains a model help an attacker (think impersonation, phishing, or supply-chain targeting)?"
	answer = requests.post("http://localhost:11434/api/generate",json={"model": "llama3.1:8B", "prompt": prompt, "stream": False}
	)
	return {
    "evidence": owner_text,
    "finding": answer.json()["response"]
	}
