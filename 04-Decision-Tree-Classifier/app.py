from flask import Flask, render_template, request
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

import webbrowser
import threading

app = Flask(__name__)

# -------------------------
# DATASET
# -------------------------
# Features: Weight (grams), Color (0=Red,1=Orange,2=Yellow), Diameter (cm)
# Target: 0=Apple, 1=Orange, 2=Banana
X = np.array([
    [150, 0, 7], [160, 0, 7.5], [155, 0, 6.8],   # Apple
    [180, 1, 7.2], [190, 1, 7.8], [185, 1, 7.5], # Orange
    [120, 2, 15], [130, 2, 14.5], [125, 2, 15.2], # Banana
    [110, 2, 14], [135, 2, 16], [140, 2, 15.5]   # More banana examples
])
y = np.array([0,0,0,1,1,1,2,2,2,2,2,2])

# Train Decision Tree
dt_model = DecisionTreeClassifier(criterion="entropy", random_state=42)
dt_model.fit(X, y)

# Visualize Tree
def visualize_tree(model):
    from sklearn import tree
    plt.figure(figsize=(12,6))
    tree.plot_tree(model,
                   feature_names=["Weight","Color","Diameter"],
                   class_names=["Apple","Orange","Banana"],
                   filled=True, rounded=True)
    plt.savefig("static/tree.png")
    plt.close()

visualize_tree(dt_model)

# -------------------------
# ROUTE
# -------------------------
@app.route("/", methods=["GET","POST"])
def home():
    result = None
    weight = ""
    color = ""
    diameter = ""

    if request.method == "POST":
        weight = float(request.form.get("weight"))
        color = int(request.form.get("color"))
        diameter = float(request.form.get("diameter"))

        user_input = np.array([[weight, color, diameter]])
        pred = dt_model.predict(user_input)[0]

        if pred == 0:
            result = "Apple "
        elif pred == 1:
            result = "Orange "
        else:
            result = "Banana "

    return render_template("index.html",
                           result=result,
                           weight=weight,
                           color=color,
                           diameter=diameter)

# -------------------------
# AUTO OPEN IN BROWSER
# -------------------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__=="__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
