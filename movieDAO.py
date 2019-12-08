import mysql.connector
class MovieDAO:
    db=""
    def __init__(self): 
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
        )


    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into movies (name,genre,description,totalVotes) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid

    def getAll(self):
        cursor = self.db.cursor()
        sql="select * from movies"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))

        return returnArray

    #def getUser(self):
    #    cursor = self.db.cursor()
    #    sql="select * from users where admin = 1"

    #    cursor.execute(sql)
    #    result = cursor.fetchone()
    #    return self.convertToDictionaryUser(result)

    def get_movie(self, name):
        cursor = self.db.cursor()
        sql="select * from movies where name = %s"
        values = (name,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    def findByID(self, id):
        cursor = self.db.cursor()
        sql="select * from movies where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)

    def findID(self, id):
        cursor = self.db.cursor()
        sql="select id from movies where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return result

    def update_movie(self, values):
        cursor = self.db.cursor()
        sql="update movies set name= %s,genre=%s, description=%s, totalVotes=%s where id = %s"
        cursor.execute(sql, values)
        self.db.commit()

    def delete(self, name):
        cursor = self.db.cursor()
        sql="delete from movies where name = %s"
        values = (name,)

        cursor.execute(sql, values)

        self.db.commit()
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','name','genre', "description", "totalVotes"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item


    #def convertToDictionaryUser(self, result):
    #    colnames=['id','name','username', "password", "admin"]
    #    item = {}
    #    
    #    if result:
    #        for i, colName in enumerate(colnames):
    #            value = result[i]
    #            item[colName] = value
    #    
    #    return item
        
    def addVote(self, values):
        cursor = self.db.cursor()
        sql="update movies set totalVotes=totalVotes + %s where id = %s"
        cursor.execute(sql, values)
        self.db.commit()

movieDAO = MovieDAO()