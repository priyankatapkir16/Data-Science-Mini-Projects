from flask import Flask, render_template, request
import webbrowser
import threading

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    suggestion = None
    habit_input = ""

    if request.method == "POST":
        habit_input = request.form.get("habit").lower()

        # Simple rule-based recommendations
        if "study" in habit_input:
            suggestion = "Try the Pomodoro Technique: 25 minutes study + 5 minutes break."
        elif "sleep" in habit_input:
            suggestion = "Maintain a fixed sleep schedule and avoid screens 30 minutes before bed."
        elif "exercise" in habit_input or "workout" in habit_input:
            suggestion = "Start with a 15-minute daily routine. Consistency beats intensity!"
        elif "stress" in habit_input:
            suggestion = "Practice deep breathing for 5 minutes or take a short walk."
        elif "lazy" in habit_input or "motivation" in habit_input:
            suggestion = "Break big tasks into tiny steps. Start with 2 minutes only."
        else:
            suggestion = "Try maintaining a simple daily journal to track your habits."

    return render_template("index.html", habit_input=habit_input, suggestion=suggestion)


# -----------------------------
# Auto-open Microsoft Edge
# -----------------------------
def open_browser():
    try:
        # Opens Microsoft Edge explicitly
        webbrowser.get("windows-edge").open("http://127.0.0.1:5000/")
    except:
        # If the above fails, use default browser fallback
        webbrowser.open("http://127.0.0.1:5000/")


if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
