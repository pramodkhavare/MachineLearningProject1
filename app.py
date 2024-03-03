from flask import Flask ,request 
import os ,sys
from Housing.src.logger import logging
from Housing.src.exception import HousingException
app = Flask(__name__)   #app is Flask object


@app.route("/" ,methods= ['GET' , 'POST'])
def index():
    try:
        return "CICD Pipeline has been estabilished" 

    except Exception as e:
        raise HousingException(error_message= e ,error_detail= sys)
    


if __name__ == "__main__":
    app.run(debug=True)