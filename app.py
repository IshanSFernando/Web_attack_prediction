import numpy as np
from flask import Flask, request, render_template
import pickle

import os

PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

model = pickle.load(open(r"finalized_model.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")    

@app.route("/about.html")
def about():
    full_filename_1 = os.path.join(app.config['UPLOAD_FOLDER'], 'more.PNG')
    full_filename_2 = os.path.join(app.config['UPLOAD_FOLDER'], 'SVM_report.PNG')
    full_filename_3 = os.path.join(app.config['UPLOAD_FOLDER'], 'KNN.PNG')
    full_filename_4 = os.path.join(app.config['UPLOAD_FOLDER'], 'Capture.PNG')
    full_filename_5 = os.path.join(app.config['UPLOAD_FOLDER'], 'principal.PNG')
    full_filename_6 = os.path.join(app.config['UPLOAD_FOLDER'], 'Kmeans.PNG')
    full_filename_7 = os.path.join(app.config['UPLOAD_FOLDER'], 'elbow_method.PNG')
    full_filename_8 = os.path.join(app.config['UPLOAD_FOLDER'], 'After_elbow.PNG')
    full_filename_9 = os.path.join(app.config['UPLOAD_FOLDER'], 'semi.PNG')
    return render_template("about.html",image_1 = full_filename_1,image_2 = full_filename_2,image_3 = full_filename_3,image_4 = full_filename_4,image_5 = full_filename_5,image_6 = full_filename_6,image_7 = full_filename_7,image_8 = full_filename_8,image_9 = full_filename_9)

@app.route("/predict", methods=["POST"])
def predict():

    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = prediction[0]

    countries = ["Benign", "Brute Force -Web", "Brute Force -XSS", "SQL Injection"]

    return render_template(
        "index.html", prediction_text="Likely attack: {}".format(countries[output])
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)