import spacy
from spacy.language import Language
from spacy.tokens import Doc
import sys

MODEL_NAME = "model"
model: Language | None = None


def _model_path():
    return f"var/models/{MODEL_NAME}"


def _get_model():
    global model
    if model is None:
        model = spacy.load(_model_path())
    return model


def _model_labels():
    return [label for label in _get_model().pipe_labels["ner"] if label != "UNKNOWN"]


type ResumeRecord = dict[str, list[str]]


def _doc_to_record(doc: Doc) -> ResumeRecord:
    ents = [(ent.label_, ent.text) for ent in doc.ents]
    labels = _model_labels()
    insights: ResumeRecord = {label: [] for label in labels}
    for label, ent in ents:
        if label not in labels:
            print(f"Unknown label: {label}", file=sys.stderr)
            continue
        insights[label].append(ent)
    return insights


def parse_resume(text: str) -> ResumeRecord:
    doc = _get_model()(text)
    insights = _doc_to_record(doc)
    return insights
