### Install Ollama (Local LLM Runtime)

Download and install Ollama:

[https://ollama.com/download](https://ollama.com/download)

Pull a model (choose one):

```bash
ollama pull mistral
```


---

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

Open the browser at:

```
http://localhost:8501
```

---

## Using the App

1. Upload a **valid PDF file**
2. Wait for indexing to complete
3. Ask questions about the document
4. Ask follow-up questions (memory is preserved)

---

## Sample PDFs for Testing


Recommended:

* Transformer Paper
  [https://arxiv.org/pdf/1706.03762.pdf](https://arxiv.org/pdf/1706.03762.pdf)
* Stanford CS229 Notes
  [https://cs229.stanford.edu/notes2020fall/CS229_Lecture_Notes.pdf](https://cs229.stanford.edu/notes2020fall/CS229_Lecture_Notes.pdf)

---
