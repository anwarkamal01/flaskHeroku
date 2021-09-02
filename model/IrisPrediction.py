from model.DatabasePool import DatabasePool
from config.Settings import Settings

import datetime
import jwt


class IrisPrediction:

    @classmethod
    def getPredictions(cls,username):
        try:
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f"Connected to {db_Info}");

            cursor = dbConn.cursor(dictionary=True)
            #sql="select * from user where userid=%s"
            sql="SELECT i.prediction_id,i.sepal_length,i.sepal_width,i.petal_length,i.petal_width,u.username,i.insertion_date,i.prediction FROM irisprediction i, user u WHERE i.user_id = u.userid and u.username =%s"

            cursor.execute(sql,(username,))
            predictions = cursor.fetchall() 

            return predictions

        finally:
            dbConn.close()
            print("release connection")

    @classmethod
    def insertPrediction(cls,user_id,sepal_length,sepal_width,petal_length,petal_width,prediction):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ just before inserting iris prediction into database")
            sql="INSERT INTO irisprediction (user_id, sepal_length, sepal_width, petal_length, petal_width, prediction) VALUES (%s,%s,%s,%s,%s,%s)"
            s1=str(prediction)
            cursor.execute(sql,(user_id,sepal_length,sepal_width,petal_length,petal_width,s1))
            dbConn.commit()

            count=cursor.rowcount
            print(cursor.lastrowid)

            return count
        finally:
            dbConn.close()

    @classmethod
    def deletePrediction(cls,predictionid):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)

        sql="delete FROM irisprediction where prediction_id=%s"
        cursor.execute(sql,(predictionid,))
        dbConn.commit()
        rows=cursor.rowcount

        dbConn.close()

        return rows
