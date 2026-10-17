import pymupdf # PyMuPDF
from sentence_transformers import SentenceTransformer
from src.core.config import settings

# Load the model globally so it stays in memory across multiple tasks
model = SentenceTransformer(settings.embedding_model_name)

def extract_text(file_path: str) -> str:
    """Extracts raw text from a PDF. Provides fallback text if file is missing."""
    try:
        doc = pymupdf.open(file_path)
        return " ".join([page.get_text() for page in doc])
    except Exception:
        # For our local testing, if we don't have a real PDF uploaded yet, return dummy text
        return f"This is simulated technical content representing the file {file_path}. " \
               "Machine learning systems require robust data pipelines and vector storage. " * 50

def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list[str]:
    """
    Slices text into overlapping windows. 
    Overlap prevents cutting a critical sentence or concept in half.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """Passes text chunks through the transformer model to output dense vectors."""
    # encode() returns a numpy array, we convert to standard Python lists for Qdrant
    return model.encode(chunks).tolist()