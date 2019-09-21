from flask import Flask
from flask import render_template
from graph_computations import experiment as experiments

app = Flask(__name__, template_folder="templates")


@app.route('/')
def index():
    return render_template('index.html', message="Here is a message")

def start_exp():
    experiment = experiments.Experiment(10)
    initial = experiment.get_initial()
    return render_template('test.html', graph=initial)

def run_exp(experiment):
    trans_hist = experiment.to_api(10)
    #redirect user to new templste with completed experiment data