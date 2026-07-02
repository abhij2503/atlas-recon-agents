from bs4 import BeautifulSoup
import requests

def run():
	with open("targets/bert_files.html", encoding="utf-8") as f:
		raw = f.read()
	soup = BeautifulSoup(raw, "html.parser")   # make the soup
	file_list = []
	for link in soup.find_all("a"):            # loop over links, not letters
		word = link.get_text().strip()         # the clean text of this link
		if word.endswith((".json", ".txt", ".bin", ".safetensors", ".h5", ".msgpack", ".onnx")) and not word.startswith("Update"):
			file_list.append(word)
	files_text = ", ".join(file_list)
	prompt = f"Here are the downloadable files from a public AI model: {files_text}. In one sentence, why would these matter to an attacker?"

	answer = requests.post("http://localhost:11434/api/generate", json={"model": "llama3.1:8B", "prompt": prompt, "stream": False})
	return {
    "evidence": file_list,
    "finding": answer.json()["response"]
	}
	