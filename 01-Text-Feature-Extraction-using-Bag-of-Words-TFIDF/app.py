from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import webbrowser
import threading
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    bow_output = None
    tfidf_output = None
    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("input_text", "").strip()

        if input_text:
            # Bag of Words
            cv = CountVectorizer()
            bow_vector = cv.fit_transform([input_text]).toarray()
            bow_output = bow_vector.tolist()

            # TF-IDF
            tfidf = TfidfVectorizer()
            tfidf_vector = tfidf.fit_transform([input_text]).toarray()
            tfidf_output = tfidf_vector.tolist()

    return render_template("index.html", bow=bow_output, tfidf=tfidf_output, input_text=input_text)


# Function to open browser automatically
def open_browser():
    url = "http://127.0.0.1:5000"
    try:
        # Try default browser first
        webbrowser.open(url)
    except:
        print(f"Please open your browser and go to {url}")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
