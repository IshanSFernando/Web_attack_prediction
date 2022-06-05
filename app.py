import numpy as np
from flask import Flask, request, render_template
from lockfile import LockFile
import pickle

import os

PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

model = pickle.load(open(r"finalized_model.pkl", "rb"))


@app.route("/")
def home():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'Nicol logo 1.png')
    lock = LockFile("visitors.txt")
    pred="enter your inputs"
    with lock:
        with open("visitors.txt", "r+") as f:
            fileContent = f.read()

            if fileContent == "":
                count = 1
            else:
                count = int(fileContent) + 1
            
            f.seek(0)
            f.write(str(count))
            f.truncate()
    lock = LockFile("predictions.txt")
    with lock:
        with open("predictions.txt", "r+") as g:
            

            count_1=g.read()
            g.seek(0)
            g.write(str(count_1))
            g.truncate()
    return render_template("in.html",
    prediction_text="{}".format(pred),
    visitor_count="number of visitors: {}".format(str(count)),
    number_of_predictions="Number of predictions: {}".format(str(count_1)),
    logo_=logo
    )




@app.route("/in.html")
def index():
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'Nicol logo 1.png')
    lock = LockFile("visitors.txt")
    pred="enter your inputs"
    with lock:
        with open("visitors.txt", "r+") as f:
            fileContent = f.read()

            if fileContent == "":
                count = 1
            else:
                count = int(fileContent) + 1
            
            f.seek(0)
            f.write(str(count))
            f.truncate()
    lock = LockFile("predictions.txt")
    with lock:
        with open("predictions.txt", "r+") as g:
            

            count_1=g.read()
            g.seek(0)
            g.write(str(count_1))
            g.truncate()
    return render_template("in.html",
    prediction_text="{}".format(pred),
    visitor_count="number of visitors: {}".format(str(count)),
    number_of_predictions="Number of predictions: {}".format(str(count_1)),
    logo_=logo
    )    

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
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'Nicol logo 1.png')
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = prediction[0]

    countries = ["Benign", "Brute Force -Web", "Brute Force -XSS", "SQL Injection"]

    lock = LockFile("predictions.txt")
    with lock:
        with open("predictions.txt", "r+") as g:
            fileContent = g.read()

            if fileContent == "":
                count_1 = 1
            else:
                count_1 = int(fileContent) + 1
            
            g.seek(0)
            g.write(str(count_1))
            g.truncate()
    lock = LockFile("visitors.txt")
    with lock:
        with open("visitors.txt", "r+") as f: 

            count=f.read()
            f.seek(0)
            f.write(str(count))
            f.truncate()

    return render_template(
        "in.html", 
        prediction_text="Likely attack: {}".format(countries[output]),
        visitor_count="number of visitors: {}".format(str(count)),
        number_of_predictions="Number of predictions: {}".format(str(count_1)),
        logo_=logo
    )


if __name__ == "__main__":
    app.run()