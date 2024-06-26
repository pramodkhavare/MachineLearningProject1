from flask import Flask ,request 
import os ,sys
import pip 
import json 
from flask import render_template ,abort ,send_file






from Housing.src.logger import logging
from Housing.src.exception import HousingException
from Housing.src.pipeline.prediction_pipeline import HousingData ,Prediction
from Housing.src.pipeline.training_pipeline import Pipeline
from Housing.src.constant import CONFIG_DIR
from Housing.src.logger import get_log_dataframe
from Housing.src.config.configuration import HousingConfiguration
from Housing.src.utils.utils import write_yaml ,read_yaml

ROOT_DIR =os.getcwd()
LOG_FOLDER_NAME = 'Housing_logs'
PIPELINE_FOLDER_NAME = 'Housing\src'
SAVED_MODEL_DIR  ='saved_models'
PROCESSOR_DIR = 'D:\Data Science\MachineLearning\Project\MachineLearningProject1\\artifact\\transformed_data_dir'
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR ,CONFIG_DIR ,'model.yaml')
LOG_DIR = os.path.join(ROOT_DIR ,LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR ,PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR ,SAVED_MODEL_DIR)

HOUSING_DATA_KEY = "housing_data"
MEDIAN_HOUSING_VALUE_KEY = "median_house_value"

app = Flask(__name__)   #app is Flask object


@app.route('/artifact' ,defaults = {'req_path': 'artifact'})
@app.route('/artifatc/<path:req_path>')
def render_artifacts_dir(req_path):
    os.makedirs('artifact' ,exist_ok=True)
    print(f"req_path: {req_path}") 
    abs_path = os.path.join(req_path)
    print(f"Abs_path :{abs_path}")

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)
    
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path ,'r' ,encoding='utf-8') as file:
                content = ''
                for line in file.readline():
                    content = f"{content}{line}"
                return content 
        return send_file(abs_path)  

    files = {os.path.join(abs_path ,file_name): file_name for file_name in os.listdir(abs_path) if 
             "artifact" in os.path.join(abs_path ,file_name)} 

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


    



@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=HousingConfiguration())
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)



@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        HOUSING_DATA_KEY: None,
        MEDIAN_HOUSING_VALUE_KEY: None
    }

    if request.method == 'POST':
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        housing_median_age = float(request.form['housing_median_age'])
        total_rooms = float(request.form['total_rooms'])
        total_bedrooms = float(request.form['total_bedrooms'])
        population = float(request.form['population'])
        households = float(request.form['households'])
        median_income = float(request.form['median_income'])
        ocean_proximity = request.form['ocean_proximity']

        housing_data = HousingData(lattitude=latitude,
                                   longitude=longitude,
                                   house_median_age=housing_median_age,
                                   total_rooms=total_rooms,
                                   total_bedrooms=total_bedrooms,
                                   population=population,
                                   households=households,
                                   median_income=median_income,
                                   ocean_proximity=ocean_proximity,
                                   )
        housing_df = housing_data.get_data_as_dataframe()
        housing_predictor = Prediction(model_dir=MODEL_DIR ,preprocessor_dir =PROCESSOR_DIR)
        median_housing_value = housing_predictor.prediction(features=housing_df)

        context = {
            HOUSING_DATA_KEY: housing_data.get_data_as_dataframe(),
            MEDIAN_HOUSING_VALUE_KEY: median_housing_value,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)



@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml(yaml_file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__=="__main__":
    app.run(debug=True,port=8501)