import os
import json
import re
from pathlib import Path
from typing import List, Tuple
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from PIL import Image
from qreader import QReader
import base64
import imghdr

_ST_MODEL = None


def _get_embedding_model():
    global _ST_MODEL
    if _ST_MODEL is None:
        _ST_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _ST_MODEL


def decode_qr(reference: str) -> Tuple[str, str]:
    """
    Decode a QR code from an image file and save any image content found.
    
    Args:
        reference: Path to the QR code image file
    
    Returns:
        Tuple of (decoded text, path to saved image if image content was found, else None)
    """
    qr_path = Path(__file__).parent / "QR-code.png"
    if not qr_path.exists():
        raise FileNotFoundError(f"QR code image not found at {qr_path}")
    
    # Read the image using PIL
    image = Image.open(str(qr_path))
    
    # Initialize QReader
    qreader = QReader()
    
    # Decode QR code
    qr_data = qreader.decode(image)
    if qr_data is None:
        raise ValueError("No QR code found in the image")
    
    # Try to decode as base64 and check if it's an image
    try:
        # Remove data URL prefix if present
        if qr_data.startswith('data:image'):
            base64_data = qr_data.split(',')[1]
        else:
            base64_data = qr_data
            
        image_data = base64.b64decode(base64_data)
        image_type = imghdr.what(None, image_data)
        
        if image_type:
            # It's an image, save it
            output_path = qr_path.parent / f"qr_content.{image_type}"
            with open(output_path, 'wb') as f:
                f.write(image_data)
            return qr_data, str(output_path)
    except Exception:
        # Not base64 or not an image, just return the text
        pass
    
    return qr_data, None


def download_review() -> str:
    review_path = Path(__file__).parent / "frontend" / "dummy_review.txt"
    return review_path.read_text(encoding="utf-8")


def embed_text(text: str) -> List[float]:
    """Embed text using OpenAI's text-embedding-3-small model and return the first 5 dimensions."""
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    response = client.embeddings.create(model="text-embedding-3-small", input=[text])
    embedding = response.data[0].embedding
    return embedding[:5]


def cosine_similarity(vector1: List[float], vector2: List[float]) -> float:
    v1 = np.asarray(vector1, dtype=float)
    v2 = np.asarray(vector2, dtype=float)
    if v1.ndim != 1 or v2.ndim != 1:
        raise ValueError("Vectors must be one-dimensional")
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    if denom == 0:
        raise ValueError("Cosine similarity undefined for zero-length vector")
    return float(np.dot(v1, v2) / denom)


def load_task_data(json_path: Path):
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_html(html_path: Path) -> str:
    return html_path.read_text(encoding="utf-8")


def get_digits(text: str):
    match = re.search(r"(\d{4})", text)
    return match.group(1) if match else None


if __name__ == "__main__":
    base_dir = Path(__file__).parent
    json_path = base_dir / "public.json"
    html_path = base_dir / "frontend" / "templates" / "index.html"

    tasks = load_task_data(json_path)
    html_content = load_html(html_path)

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    success = True

    for entry in tasks:
        task_text = entry.get("task", "")
        expected_answer = str(entry.get("answer", "")).strip()

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert escape-room solver. "
                    "Read the provided HTML and the task. "
                    "You have access to a bunch of tools to help you solve the task. Your job is to read the "
                    "HTML file that contains 4 problems. Each problem answer is one digit. Solve each problem to "
                    "get access to the 4-digit answer. Return only the four-digit answer and nothing else. "
                    "The first problem(lo`) is the red one; you need to process an image for it and choose from 4 "
                    "options that which one is the right answer and return the option number(only 1 or 2 or 3 or 4). In the second problem(lock 2) you see a txt file; "
                    "download it and find the answer in that. In the third problem(lock 3) you are given a QR code that "
                    "you have to scan and find the digit in its content. In the fourth problem(lock 4) you are given a question and an embedding. figure it to how to crack its code and find its digit. at the end do not return anything rather than the 4-digits number that is created by putting each lock's digit in order"
                ),
            },
            {
                "role": "user",
                "content": f"Task:\n{task_text}\n\nHTML Content Starts:\n{html_content}\n\nHTML Content Ends.",
            },
        ]

        tools_spec = [
            {
                "type": "function",
                "function": {
                    "name": "decode_qr",
                    "description": "Return the text embedded in the QR code rendered in index.html.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "reference": {
                                "type": "string",
                                "description": "An identifier for the QR code."
                            }
                        },
                        "required": ["reference"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "download_review",
                    "description": "Download and return the full review text used in the blue task.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "embed_text",
                    "description": "Embed the supplied text with text-embedding-3-small and return the first five dimensions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "The text to embed."
                            }
                        },
                        "required": ["text"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "embed_words",
                    "description": "Embed each supplied word with text-embedding-3-small and return the first five dimensions per word.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "words": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of words to embed."
                            }
                        },
                        "required": ["words"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "cosine_similarity",
                    "description": "Return the cosine similarity between two numeric vectors of equal length.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "vector1": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "First vector."
                            },
                            "vector2": {
                                "type": "array",
                                "items": {"type": "number"},
                                "description": "Second vector."
                            }
                        },
                        "required": ["vector1", "vector2"],
                    },
                },
            },
        ]

        while True:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools_spec,
            )

            msg = response.choices[0].message
            messages.append(msg)

            if getattr(msg, "tool_calls", None):
                for call in msg.tool_calls:
                    fn_name = call.function.name
                    args = json.loads(call.function.arguments or "{}")
                    result = globals()[fn_name](**args)
                    messages.append(
                        {
                            "role": "tool",
                            "name": fn_name,
                            "tool_call_id": call.id,
                            "content": json.dumps(result),
                        }
                    )
                continue

            llm_answer_raw = msg.content or ""
            break

        llm_digits = get_digits(llm_answer_raw)

        if llm_digits == expected_answer:
            print(f"✅ Task solved. Expected = LLM answer = {llm_digits}")
        else:
            print(f"❌ Task failed. Expected {expected_answer}, but LLM returned '{llm_answer_raw}'.")

        if llm_digits and len(llm_digits) == 4:
            for c, d in zip(["Red", "Blue", "Green", "Purple"], llm_digits):
                print(f"{c}: {d}")
        if expected_answer and len(expected_answer) == 4:
            for c, d in zip(["Red", "Blue", "Green", "Purple"], expected_answer):
                print(f"Expected {c}: {d}")

        if llm_digits != expected_answer:
            success = False
