import os
import pickle
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STORAGE_PATH = "storage"
DOCS_PATH = os.path.join(STORAGE_PATH, "docs")
INDEX_PATH = os.path.join(STORAGE_PATH, "index", "tfidf.pkl")


def extract_text_from_pdf(path: str) -> list[str]:
    """Pull out text from each page of a PDF file."""
    text_by_page = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text() or ""
            text_by_page.append(text.strip())
    return text_by_page


def build_index():
    """Rebuild TF-IDF index from all PDFs in storage/docs."""
    docs, metadata = [], []

    for filename in os.listdir(DOCS_PATH):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(DOCS_PATH, filename)
            pages = extract_text_from_pdf(path)
            for i, content in enumerate(pages):
                docs.append(content)
                metadata.append((filename, i + 1))  # (file, page number)

    if not docs:
        return None, None, None

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(docs)

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, "wb") as f:
        pickle.dump((vectorizer, matrix, metadata), f)

    return vectorizer, matrix, metadata


def load_index():
    """Load the saved TF-IDF index if it exists."""
    if not os.path.exists(INDEX_PATH):
        return None, None, None
    with open(INDEX_PATH, "rb") as f:
        return pickle.load(f)


def search(query: str, k: int = 3):
    """Return the top-k most relevant results for a query."""
    vectorizer, matrix, metadata = load_index()
    if not vectorizer:
        return []

    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, matrix).flatten()
    top_idx = scores.argsort()[::-1][:k]

    results = []
    for i in top_idx:
        results.append(
            {
                "score": round(float(scores[i]), 3),
                "doc_title": metadata[i][0],
                "page": metadata[i][1],
                "snippet": (matrix[i].__str__()[:200]),  # placeholder snippet
            }
        )
    return results
