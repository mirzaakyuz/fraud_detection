from flask import Flask, request
import pandas as pd
import pickle

app = Flask(__name__)

with open('features.pkl','rb') as m:
    features = pickle.load(m)

with open('rf_model.pkl','rb') as m:
    model = pickle.load(m)

@app.route('/')
# @app.route('/home') # iki farkli route atayabiliyoruz

def index():
    return 'Server is up and running!'
#
@app.route("/predict", methods=['GET','POST'])

def predict():

    #json_data = request.data
    json_data = request.get_json()

    if not all(k in json_data for k in ['Time','V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11',
                                        'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19', 'V20', 'V21', 'V22',
                                        'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']):
        return "Not enough data for the prediction!"

    df = pd.DataFrame.from_dict([json_data])
    #print(df)

    # df = pd.get_dummies(df).reindex(columns=features, fill_value=0)
    df = df.reindex(columns=features, fill_value=0)

    prediction = model.predict(df)

    #print(prediction)

    if prediction == 1:
        return f"The result is {str(prediction[0])}, the transaction is suspicious!"
    else:
        return f"The result is {str(prediction[0])}, the transaction is trustworthy."
app.run()
# app.run(port=5001)