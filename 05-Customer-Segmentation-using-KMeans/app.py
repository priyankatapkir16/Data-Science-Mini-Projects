from flask import Flask, render_template, request
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import threading, webbrowser

app = Flask(__name__)

# Synthetic 2D dataset: weight (kg) vs height (cm)
np.random.seed(42)
cluster1 = np.random.normal(loc=[30, 100], scale=[5,10], size=(10,2))   # Small animals
cluster2 = np.random.normal(loc=[70, 150], scale=[5,10], size=(10,2))   # Medium animals
cluster3 = np.random.normal(loc=[120, 200], scale=[10,15], size=(10,2)) # Large animals

X = np.vstack((cluster1, cluster2, cluster3))

# -------------------------
# ROUTE
# -------------------------
@app.route("/", methods=["GET","POST"])
def home():
    k = 3
    result_msg = None

    if request.method == "POST":
        k = int(request.form.get("k_clusters",3))
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(X)
        centers = kmeans.cluster_centers_

        # Plot clusters
        plt.figure(figsize=(8,6))
        colors = ['#6C63FF','#FF6584','#FFC107','#00BCD4','#4CAF50']
        for i in range(k):
            plt.scatter(X[labels==i,0], X[labels==i,1], s=100, c=colors[i%len(colors)], label=f'Cluster {i+1}')
        plt.scatter(centers[:,0], centers[:,1], s=200, c='black', marker='X', label='Centroids')
        plt.xlabel("Weight (kg)")
        plt.ylabel("Height (cm)")
        plt.title(f"K-Means Clustering (k={k})")
        plt.legend()
        plt.savefig("static/cluster.png")
        plt.close()

        result_msg = f"Clustering done with k = {k}"

    return render_template("index.html", k=k, result_msg=result_msg)

# -------------------------
# AUTO OPEN BROWSER
# -------------------------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__=="__main__":
    threading.Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False, use_reloader=False)

