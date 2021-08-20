from flask import Flask,jsonify,render_template,request,g
from config.Settings import Settings
import functools
import jwt
import re

def login_required(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        token=request.headers.get('Authorization')
        print(token)

        auth=True
        #print(token.index("Bearer"))
        if token and token.index("Bearer")==0:
            token=token.split(" ")[1]
        else:
            auth=False
        
        if auth:
            try:

                #decode
                payload=jwt.decode(token,Settings.secretKey,'HS256');
                g.role=payload['role']
                g.userid=payload['userid']
            except Exception as err:
                print(err)
                auth=False
        
        if auth==False:
            output={"Message":"Error JWT"}
            return jsonify(output),403


        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator




def admin_required(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        #Apply your own code to do the necessary checks
        if g.role != "":
            role = g.role
        
        if role!="admin":
            output={"Message":"You need to be admin"}
            return jsonify(output),403
        
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator

def require_isAdminOrSelf(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        #Apply your own code to do the necessary checks
        if g.role != "":
            role = g.role
        
        print("role : "+role )
        print("str(kwargs['userid']) : "+str(kwargs['userid']))
        print("g.userid :"+str(g.userid))
        
        if role!="admin" and (kwargs['userid']!=g.userid):
            output={"Message":"You need to be admin or be the actual user to retrieve your record"}
            return jsonify(output),403
        
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator


def validateNumber(num):

    pattern=re.compile("^[+-]?([0-9]+\.?[0-9]+|\.[0-9]+)$")

    if (pattern.match(num)):
        return True
    else:
        return False

