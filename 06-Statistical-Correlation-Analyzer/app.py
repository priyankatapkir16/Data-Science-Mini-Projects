from flask import Flask, render_template, request
import webbrowser
import threading
import numpy as np
from scipy.stats import pearsonr, spearmanr

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    pearson_result = None
    spearman_result = None
    data1 = ""
    data2 = ""

    if request.method == "POST":
        data1 = request.form.get("data1")
        data2 = request.form.get("data2")

        # Convert input string -> list of floats
        try:
            list1 = np.array([float(x.strip()) for x in data1.split(",") if x.strip() != ""])
            list2 = np.array([float(x.strip()) for x in data2.split(",") if x.strip() != ""])

            # Validation
            if len(list1) == 0 or len(list2) == 0:
                pearson_result = "Error: Inputs cannot be empty!"
                spearman_result = None

            elif len(list1) != len(list2):
                pearson_result = "Error: Both datasets must have equal length!"
                spearman_result = None

            elif len(list1) < 2:
                pearson_result = "Error: At least 2 values are required!"
                spearman_result = None

            else:
                # Calculate Pearson & Spearman
                pearson_corr, _ = pearsonr(list1, list2)
                spearman_corr, _ = spearmanr(list1, list2)

                pearson_result = round(float(pearson_corr), 4)
                spearman_result = round(float(spearman_corr), 4)

        except:
            pearson_result = "Invalid input! Use only numbers separated by commas."
            spearman_result = None

    # Pass values to template
    return render_template(
        "index.html",
        pearson=pearson_result,
        spearman=spearman_result,
        data1=data1,
        data2=data2
    )


# Auto-open browser (Edge/Default browser)
def open_browser():
    webbrowser.get("windows-default").open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
