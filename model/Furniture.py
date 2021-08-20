from model.DatabasePool import DatabasePool

class Furniture:

    @classmethod
    def getFurnitureByCat(cls,catid):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql="select f.cat_id,c.cat_name,f.description,f.dimension,f.images,f.it_id,f.item_code,f.name,f.price,f.quantity from furniture f,category c where c.cat_id = f.cat_id and c.cat_id=%s"
        cursor.execute(sql,(catid,))
        furniture = cursor.fetchall()

        dbConn.close()

        return furniture