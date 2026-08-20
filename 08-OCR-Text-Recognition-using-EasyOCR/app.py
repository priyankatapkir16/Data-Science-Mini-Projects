from flask import Flask, render_template, request
import easyocr
import os
import threading
import webbrowser

app = Flask(__name__)

# Initialize easyocr Reader once (English language)
reader = easyocr.Reader(['en'])

@app.route("/", methods=["GET", "POST"])
def home():
    suggestion = None
    extracted_text = ""

    if request.method == "POST":
        file = request.files.get("image")
        if file:
            # Save temporary image
            img_path = "temp_img.png"
            file.save(img_path)

            # OCR extraction
            result = reader.readtext(img_path, detail=0)
            extracted_text = ' '.join(result)
            suggestion = f"Extracted Text: {extracted_text}"

            # Remove temporary file
            os.remove(img_path)

    return render_template("index.html", suggestion=suggestion)

# -----------------------------
# Auto-open Microsoft Edge
# -----------------------------
def open_browser():
    try:
        webbrowser.get("windows-edge").open("http://127.0.0.1:5000/")
    except:
        webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
