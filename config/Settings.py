import os

class Settings:
    secretKey="321897kdbmgj321djnbug#@4rhxcjk6(!d)"

    #Dev
    #host='localhost'
    #database='furniture'
    #user='root'
    #password='jupiter1'

    #Staging on heroku
    host=os.environ['HOST']
    database=os.environ['DATABASE']
    user=os.environ['USERNAME']
    password=os.environ['PASSWORD']
