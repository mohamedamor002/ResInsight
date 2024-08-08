from flask import Flask, request, render_template
from turbo_flask import Turbo
import parsing_model
import pdf_extraction

app = Flask(__name__)
turbo = Turbo(app)


@app.get("/")
def index():
    return render_template("index.html")


UNPROCESSABLE_ENTITY = 422


def form_error(template: str, **context):
    return render_template(template, **context), UNPROCESSABLE_ENTITY


@app.post("/upload")
def upload_file():

    upload_error: str | None = None

    if "file" not in request.files:
        upload_error = "No file part."
        return form_error("index.html", upload_error=upload_error)

    file = request.files["file"]
    if file.filename == "":
        upload_error = "No uploaded file."
        return form_error("index.html", upload_error=upload_error)

    if file.content_type != "application/pdf":
        upload_error = "File must be a PDF."
        return form_error("index.html", upload_error=upload_error)

    text = pdf_extraction.pdf_to_text(file)
    insights = parsing_model.parse_resume(text)
    if turbo.can_stream():
        return turbo.stream(
            (
                turbo.update(
                    render_template("insights.html", insights=insights), "insights"
                ),
                turbo.update("", "error"),
            )
        )
    return render_template("index.html", insights=insights)


if __name__ == "__main__":
    app.run()
