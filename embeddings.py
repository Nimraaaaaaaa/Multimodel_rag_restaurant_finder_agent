from sentence_transformers import SentenceTransformer
import torch
from PIL import Image
import numpy as np

# Load CLIP model from sentence-transformers
clip_model = SentenceTransformer("clip-ViT-B-32")
text_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_image_embedding(image):
    # image = PIL image
    image_np = np.array(image)
    
    # SentenceTransformer handles image → embedding internally
    emb = clip_model.encode([image_np])
    return emb[0]

def get_text_embedding(text):
    return text_model.encode([text])[0]
