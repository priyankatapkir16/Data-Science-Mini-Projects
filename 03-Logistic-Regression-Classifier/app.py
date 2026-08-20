from flask import Flask, render_template, request
import webbrowser
import threading
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

app = Flask(__name__)

# -----------------------------------------
# EXPANDED REALISTIC DATASET
# -----------------------------------------

# Dataset: [study_hours, sleep_hours, pass/fail]
# 1 = Pass, 0 = Fail

dataset = np.array([
    [1, 5, 0], [1, 6, 0], [1, 4, 0],
    [2, 4, 0], [2, 5, 0], [2, 7, 0],   # Low study → mostly fail

    [3, 5, 0], [3, 6, 1], [3, 7, 1],
    [4, 4, 0], [4, 5, 1], [4, 6, 1],   # Medium study → depends on sleep

    [5, 4, 0], [5, 5, 1], [5, 6, 1], [5, 7, 1],
    [6, 5, 1], [6, 6, 1], [6, 7, 1],   # Good study → mostly pass

    [7, 4, 1], [7, 5, 1], [7, 6, 1], [7, 8, 1],  # Strong pass

    # Additional realistic variations
    [3, 8, 1], [2, 8, 0], [4, 8, 1], [1, 8, 0],
    [6, 3, 0], [7, 3, 0], [8, 4, 1], [8, 6, 1]
])

X = dataset[:, :2]   # study, sleep
y = dataset[:, 2]    # label

# Train-Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------------------
# MODELS
# -----------------------------------------

log_model = LogisticRegression()
log_model.fit(X_train, y_train)

nb_model = GaussianNB()
nb_model.fit(X_train, y_train)


# -----------------------------------------
# ROUTE
# -----------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():
    result_lr = None
    result_nb = None
    study = ""
    sleep = ""

    if request.method == "POST":
        study = request.form.get("study")
        sleep = request.form.get("sleep")

        study = float(study)
        sleep = float(sleep)

        user_input = np.array([[study, sleep]])

        # Logistic Regression Prediction
        pred_lr = log_model.predict(user_input)[0]
        result_lr = "Pass" if pred_lr == 1 else "Fail"

        # Naive Bayes Prediction
        pred_nb = nb_model.predict(user_input)[0]
        result_nb = "Pass" if pred_nb == 1 else "Fail"

    return render_template(
        "index.html",
        result_lr=result_lr,
        result_nb=result_nb,
        study=study,
        sleep=sleep
    )


# -----------------------------------------
# AUTO OPEN IN MICROSOFT EDGE
# -----------------------------------------

def open_browser():
    webbrowser.get("windows-default").open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
