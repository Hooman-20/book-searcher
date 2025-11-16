import os
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
import shutil
from indexer import build_index, search

STORAGE_PATH = "storage"
DOCS_PATH = os.path.join(STORAGE_PATH, "docs")

os.makedirs(DOCS_PATH, exist_ok=True)

app = FastAPI(title="Book Searcher", description="Search inside PDFs with TF-IDF")




@app.get("/")
def root():
    return {"message": "Welcome to Book Searcher! Go to /docs to try the API."}



@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a PDF file and reindex documents."""
    if not file.filename.endswith(".pdf"):
        return JSONResponse(content={"error": "Only PDF files are supported"}, status_code=400)

    file_path = os.path.join(DOCS_PATH, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    build_index()
    return {"ok": True, "message": f"Indexed {file.filename}"}


@app.get("/search")
def search_docs(q: str = Query(..., description="Search query"), k: int = 3):
    """Search the indexed PDFs for relevant pages."""
    results = search(q, k)
    return {"query": q, "results": results}
