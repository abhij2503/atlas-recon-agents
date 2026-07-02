from bs4 import BeautifulSoup
import requests

def run():	
	with open("targets/bert_modelcard.html", encoding="utf-8") as f:
		raw = f.read()
	soup = BeautifulSoup(raw, "html.parser")   # make the soup
	text = soup.get_text()
	first = text.find("Limitations and bias")
	start = text.find("Limitations and bias", first + 1)
	bias_text = text[start : start + 1500]

	prompt = f"Here is the documented limitations-and-bias section from a public AI model's page: {bias_text}. In one sentence, why would a publicly admitted weakness like this matter to an attacker doing reconnaissance?"

	answer = requests.post("http://localhost:11434/api/generate",json={"model": "llama3.1:8B", "prompt": prompt, "stream": False})
	return {
    "evidence": bias_text[:300],     # first 300 chars, enough to show the proof
    "finding": answer.json()["response"]
	}

	