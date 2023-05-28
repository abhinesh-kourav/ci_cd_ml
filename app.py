from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the pickled pipelines
with open('ci_pipeline.pkl', 'rb') as file:
    ci_pipeline = pickle.load(file)

with open('cd_pipeline.pkl', 'rb') as file:
    cd_pipeline = pickle.load(file)


@app.route('/')
def index():
    return render_template('prediction_form.html')


@app.route('/predict', methods=['POST'])
def predict():
    rock_classification = request.form['rock_classification']
    mean_grain_size = float(request.form['mean_grain_size'])
    plagioclase_feldspar = float(request.form['plagioclase_feldspar'])
    alkali_feldspar = float(request.form['alkali_feldspar'])
    quartz = float(request.form['quartz'])
    calcite = float(request.form['calcite'])
    clay = float(request.form['clay'])
    mica = float(request.form['mica'])
    amphibole = float(request.form['amphibole'])
    density = float(request.form['density'])
    porosity = float(request.form['porosity'])
    e = float(request.form['e'])
    v = float(request.form['v'])

    # Create a DataFrame with the input values
    input_data = pd.DataFrame({
        'Mean Grain Size (mm)': [mean_grain_size],
        'Rock Classification': [rock_classification],
        'Plagioclase feldspar (%)': [plagioclase_feldspar],
        'Alkali feldspar (%)': [alkali_feldspar],
        'Quartz (%)': [quartz],
        'Calcite (%)': [calcite],
        'Clay (%)': [clay],
        'Mica (%)': [mica],
        'Amphibole (%)': [amphibole],
        'Density (g/cm3)': [density],
        'Porosity (%)': [porosity],
        'E (GPa)': [e],
        'v': [v]
    })

    #print(input_data)
    ci_prediction = round(ci_pipeline.predict(input_data)[0],2)
    cd_prediction = round(cd_pipeline.predict(input_data)[0],2)

    return render_template('prediction_result.html', ci_prediction=ci_prediction, cd_prediction=cd_prediction)

if __name__ == '__main__':
    app.run(debug=True)