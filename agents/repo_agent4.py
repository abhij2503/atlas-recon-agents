from bs4 import BeautifulSoup
import requests

def run():
	with open("targets/bert_modelcard.html", encoding="utf-8") as f:
		soup = BeautifulSoup(f.read(), "html.parser")
	demo_list = []
	for link in soup.find_all("a"):
		href = str(link.get("href"))
		# keep real demos/spaces, skip the bare menu button
		if ("exbert/?model=" in href or "/spaces/" in href) and href not in demo_list:
			demo_list.append(href)
	demos_text = ", ".join(demo_list)
	prompt = f"A public AI model has these live demo and Space endpoints where anyone can interact with it: {demos_text}. In one sentence, why do live, reachable demo endpoints help an attacker (think probing model behavior without needing to download anything)?"
	answer = requests.post("http://localhost:11434/api/generate",json={"model": "llama3.1:8B", "prompt": prompt, "stream": False})
	return {
    "evidence": demo_list,
    "finding": answer.json()["response"]
	}