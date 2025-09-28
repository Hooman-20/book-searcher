# Book Searcher

Book Searcher is a lightweight tool that makes it easy to **search inside large PDF textbooks**.  
It uses **TF-IDF and cosine similarity** to find the most relevant passages, returning snippets and page numbers instantly.  

---

##  Features
- Upload PDF(s) and automatically index them by page  
- Keyword search with **ranked results**  
- Returns snippets with page references for quick context  
- REST API with **FastAPI + Swagger UI**  
- Saves the index so searches persist after restart  

---

##  Tech Stack
- **Python 3.10+**  
- FastAPI – backend framework  
- Uvicorn – server  
- scikit-learn – TF-IDF vectorization  
- PyPDF2 – PDF text extraction  
- NumPy – math utilities  

---

##  Project Structure
```
book-searcher/
book-searcher/
│── app.py          # API (upload + search)
│── indexer.py      # PDF parsing + TF-IDF indexing
│── requirements.txt
│── README.md
│── storage/
│    ├── docs/      # uploaded PDFs
│    └── index/     # saved index files
```

---

## Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/Hooman-20/book-searcher.git
cd book-searcher
```
2. Install dependencies
```
python -m venv .venv
.venv\Scripts\activate   # Windows
# or: source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```
3. Run the server
```uvicorn app:app --host 0.0.0.0 --port 8000 --reload


Open http://localhost:8000/docs
 to test in Swagger UI.
```

 Example Usage

Upload a PDF
```
curl -F "file=@Algorithms.pdf" http://localhost:8000/upload
```

Response:
```
{"ok": true, "message": "Indexed Algorithms.pdf"}
```

Search inside the PDF
```
curl "http://localhost:8000/search?q=dynamic%20programming&k=3"
```

Response:
```
{
  "query": "dynamic programming",
  "results": [
    {
      "score": 0.38,
      "doc_title": "Algorithms.pdf",
      "page": 42,
      "snippet": "Dynamic programming is a method for solving complex problems..."
    }
  ]
}
```
