from flask import Flask ,request 

app = Flask(__name__)   #app is Flask object


@app.route("/" ,methods= ['GET' , 'POST'])
def index():
    return "CICD Pipeline has been estabilished"



if __name__ == "__main__":
    app.run(debug=True)