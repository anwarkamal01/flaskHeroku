from flask import Flask,jsonify,render_template,request
from model.User import User
from validation.Validator import *
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

#GET all users
@app.route('/users',methods=['GET'])
#@login_required
#@admin_required
def getUsers():
    try:
        #print(g.role)
        users=User.getUsers()

        output={"Users":users}
        return jsonify(output),200
    except Exception as err:
        print(err)
        output={"Message":"Error occurred."}
        return jsonify(output),500

#Get 1 User based on userid supplied
@app.route('/users/<int:userid>',methods=['GET'])
#@login_required
#@require_isAdminOrSelf
def getOneUser(userid):

    try:
        users=User.getUserByUserid(userid) 
        print("INT function called")
        if len(users)>0:
            output={"Users":users}
            return jsonify(output),200
        else:
            output={"Users":""}
            return jsonify(output),404
    except Exception as err:
        print(err)
        output={"Message":"Error occurred."}
        return jsonify(output),500

#Get 1 User based on userid supplied
@app.route('/users/<string:userid>',methods=['GET'])
def getOneStringUser(userid):

    try:
        users=User.getUserByUserid(int(userid)) 
        print("String function called")
        if len(users)>0:
            output={"Users":users}
            return jsonify(output),200
        else:
            output={"Users":""}
            return jsonify(output),404
    except Exception as err:
        print(err)
        output={"Message":"Error occurred."}
        return jsonify(output),500

#POST 1 new user - Insert
@app.route('/users',methods=['POST'])
def insertUser():

    try:
        #extract the incoming request data from user
        userData=request.json#request.form.to_dict() ->if using html forms
        print(userData)
        print("****************************just before calling database insert1")
        #userid=userData['userid']
        username=userData['userName']
        email=userData['email']
        role=userData['role']
        password=userData['password']

        #call the model to insert
        print("****************************just before calling database insert2")
        count=User.insertUser(username,email,role,password)

        output={"Rows Inserted":count}      
        return jsonify(output),201
    except Exception as err:
        print(err)
        output={"Message":"Error occurred."}
        return jsonify(output),500


@app.route('/users/<int:userid>', methods=['PUT'])
def updateUser(userid):
    jsonBody=request.json
    print(jsonBody);
   
    count=User.updateUser(userid,jsonBody['email'],jsonBody['password'])
    
    if(count==1):        
        return '{"message": "User with id '+str(userid)+ ' has been successfully updated!"}',200
    else:
        return '{"message": "User with id '+str(userid)+ ' does not exist!"}',404


@app.route('/users/<int:userid>',methods=['DELETE'])
@login_required
def deleteUser(userid):
    try:

        count=User.deleteUser(userid)
        output={"Rows Affected":count}
        return jsonify(output),200
    
    except Exception as err:
        print(err)
        output={"Message":"Error occurred."}
        return jsonify(output),500


#generating a resource, JWT
@app.route('/users/login',methods=['POST'])
def loginUser():
    try:
        userData=request.json
        print("#################################### Before calling database loginUser")
        jwtToken=User.loginUser(userData['email'],userData['password'])

        output={"JWT":jwtToken}

        status=200
        if jwtToken=="":
            status=404

        return jsonify(output),status

    except Exception as err:
        print(err)
        output={"Message":"Error occurred."}
        return jsonify(output),500


if __name__ == '__main__':
    app.run(debug=True) #start the flask app with default port 5000
