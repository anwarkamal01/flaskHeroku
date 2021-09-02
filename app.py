from model.IrisPrediction import IrisPrediction
from flask import Flask,jsonify,request,g,render_template,abort,make_response,redirect
from model.User import User
from validation.Validator import *
from flask_cors import CORS
#Load the iris datasets using sklearn : Note you can also d/l from UCI and read using pd.read_csv
import numpy as np
import pandas as pd
import sklearn  #For Classical ML
#from sklearn import datasets
import pickle
from sklearn import datasets

app=Flask(__name__)
CORS(app)

#code the routes
@app.route('/login', methods=['POST'])
def loginUser():
    try:
        email=request.form['email']
        pwd=request.form['pwd']
        output=User.loginUser({"email":email,"password":pwd})
        #print(output)
        if output["jwt"]=="":
            return render_template("login.html",message="Invalid Login Credentials!")
       
        else:
            predictions=IrisPrediction.getPredictions(output['userName'])
            print(predictions)
            resp = make_response(render_template("iris2.html",msg="Hello people!",pred=predictions))
            resp.set_cookie('jwt', output["jwt"])
            resp.set_cookie('userName',output['userName'])
            resp.set_cookie('userid',str(output['userid']))
            return resp
    except Exception as err:
        print(err)
        return render_template("login.html",message="Error!")


@app.route('/register', methods=['POST'])
def registerUser():
    try:
        userName=request.form['userName']
        email=request.form['email']
        password=request.form['password']
        confirmPassword=request.form['confirmPassword']

        if password != confirmPassword:
            return render_template("register.html",message="Passwords do not match!")

        User.insertUser(userName,email,"member",password)
        
        return render_template("register.html",message="Account created successfully!")


    except Exception as err:
        print(err)
        return render_template("register.html",message="Error!")


@app.route('/iris2.html') #define the api route
@login_required
def getPredictions():
    try:
        #Insert new prediction
        userName=request.cookies.get("userName")
        userid=request.cookies.get("userid")
        sepalLength=float(request.args.get('sepalLength'))
        sepalWidth=float(request.args.get('sepalWidth'))
        petalLength=float(request.args.get('petalLength'))
        petalWidth=float(request.args.get('petalWidth'))
        iris = datasets.load_iris()
        loaded_model = pickle.load(open("iris_logistic_regression.pkl","rb"))
        #Test out the model using some prediction
        s1=np.array([sepalLength, sepalWidth, petalLength, petalWidth])
        y_prob = loaded_model.predict_proba(s1.reshape(1,-1))
        #prediction
        prediction=iris.target_names[np.argmax(y_prob)]
        #prediction probability
        probability=np.max(y_prob)
        print(prediction)
        IrisPrediction.insertPrediction(userid,sepalLength,sepalWidth,petalLength,petalWidth,prediction)    
        predictions=IrisPrediction.getPredictions(userName)
        return render_template("iris2.html",pred=predictions,prediction=prediction,prob=probability)
    except Exception as err:
        print(err)
        return render_template("iris2.html")


@app.route('/delete') #define the api route
@login_required
def delete():
    try:
        userName=request.cookies.get("userName")
        prediction_id=int(request.args.get("id"))
        IrisPrediction.deletePrediction(prediction_id)
        predictions=IrisPrediction.getPredictions(userName)
        return render_template("iris2.html",pred=predictions)
    except Exception as err:
        print(err)
        return render_template("iris2.html")



@app.route('/logout') #define the api route
def logout():
    resp = make_response(redirect("login.html"))
    resp.delete_cookie('jwt')
    
    return resp

@app.route('/<string:url>')
def staticPage(url):
    print("static page",url)
    try:
        return render_template(url)
    except Exception as err:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
 

if __name__ == '__main__':
    app.run(debug=True)
