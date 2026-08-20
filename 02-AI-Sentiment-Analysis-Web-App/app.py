from flask import Flask, render_template, request
from nltk.sentiment import SentimentIntensityAnalyzer
from afinn import Afinn
import threading
import webbrowser
import nltk

# Download VADER lexicon (run once separately if needed)
# nltk.download('vader_lexicon')

app = Flask(__name__)

# Initialize analyzers
vader_analyzer = SentimentIntensityAnalyzer()
afinn_analyzer = Afinn()

# Rule-based word lists
positive_words = ['good', 'happy', 'great', 'fantastic', 'excellent', 'love', 'like']
negative_words = ['bad', 'sad', 'terrible', 'hate', 'awful', 'worst', 'dislike']

def rule_based_sentiment(text):
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return 'Positive'
    elif neg_count > pos_count:
        return 'Negative'
    else:
        return 'Neutral'

@app.route("/", methods=["GET", "POST"])
def home():
    sentiment_results = {}
    if request.method == "POST":
        text = request.form.get("input_text")
        
        # VADER analysis
        vader_score = vader_analyzer.polarity_scores(text)['compound']
        vader_sentiment = 'Neutral'
        if vader_score >= 0.05:
            vader_sentiment = 'Positive'
        elif vader_score <= -0.05:
            vader_sentiment = 'Negative'
        
        # AFINN analysis
        afinn_score = afinn_analyzer.score(text)
        afinn_sentiment = 'Neutral'
        if afinn_score > 0:
            afinn_sentiment = 'Positive'
        elif afinn_score < 0:
            afinn_sentiment = 'Negative'
        
        # Rule-based analysis
        rule_sentiment = rule_based_sentiment(text)
        
        sentiment_results = {
            "text": text,
            "vader_sentiment": vader_sentiment,
            "vader_score": vader_score,
            "afinn_sentiment": afinn_sentiment,
            "afinn_score": afinn_score,
            "rule_sentiment": rule_sentiment
        }
    
    return render_template("index.html", results=sentiment_results)

# Function to open browser after Flask starts
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Start browser in a separate thread after 1.5 seconds
    threading.Timer(1.5, open_browser).start()
    # Run Flask without the reloader to prevent double start
    app.run(debug=False, use_reloader=False)
