from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# small demo: load a sentence transformer and compare to a "persuasive" prototype vector
_model = SentenceTransformer("all-MiniLM-L6-v2")
# create a "prototype" embedding for persuasive copy (you could expand this)
_persuasive_examples = [
    "Limited time offer! Sign up now to get lifetime savings.",
    "Don't miss out — join today for exclusive benefits.",
    "Act now to receive 50% off your first month."
]
_proto_vec = None
def _init_proto():
    global _proto_vec
    _proto_vec = _model.encode(_persuasive_examples).mean(axis=0)

def score_email(body: str) -> float:
    global _proto_vec
    if _proto_vec is None:
        _init_proto()
    vec = _model.encode([body])[0]
    sim = cosine_similarity([vec], [_proto_vec])[0][0]
    # normalize sim (roughly) into 0-1
    score = float((sim + 1) / 2)
    return round(score, 3)
