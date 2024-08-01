import spacy
from spacy.language import Language
from spacy.tokens import Doc

MODEL_NAME = "model"
model: Language | None = None


def _model_path():
    return f"var/models/{MODEL_NAME}"


def _get_model():
    global model
    if model is None:
        model = spacy.load(_model_path())
    return model


ResumeRecord = dict[str, list[str]]


def _doc_to_record(doc: Doc) -> ResumeRecord:
    ents = [(ent.label_, ent.text) for ent in doc.ents]
    insights: ResumeRecord = {}
    for label, ent in ents:
        if label not in insights:
            insights[label] = []
        insights[label].append(ent)
    return insights


def parse_resume(text: str) -> ResumeRecord:
    doc = _get_model()(text)
    insights = _doc_to_record(doc)
    return insights
