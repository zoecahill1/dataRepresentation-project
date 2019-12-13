import mysql.connector
import csv
import dbconfig as cfg

class MovieDAO:
    db=""
    def __init__(self): 
        self.db = mysql.connector.connect(
        host=       cfg.mysql['host'],
        user=       cfg.mysql['user'],
        password=   cfg.mysql['password'],
        database=   cfg.mysql['database']
        )
    # Deletes data from table so top 100 can be written in
    def clear_table(self):
        cursor = self.db.cursor()
        sql="truncate table topMovies"
        cursor.execute(sql)
    # Get the top movies
    def gettop(self):
        cursor = self.db.cursor()
        sql="select * from topMovies"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionaryTop(result))

        return returnArray

    # Write top movies to db from csv
    def top_movies(self):
        with open ('ImdbTopMovies.csv', 'r') as f:
            reader = csv.reader(f)
            columns = next(reader) 
            query = 'insert into topMovies(Title,Year) values (%s,%s)'
            
            cursor = self.db.cursor()
            for data in reader:
                print (data)
                cursor.execute(query, data)
            self.db.commit()
            return print("Done")
    # Create movie
    def create(self, values):
        cursor = self.db.cursor()
        sql="insert into movies (name,genre,description,totalVotes) values (%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.db.commit()
        return cursor.lastrowid
    # Get all the movies
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
    # Get all movies by name
    def get_movie(self, name):
        cursor = self.db.cursor()
        sql="select * from movies where name = %s"
        values = (name,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)
    # Get all movies by id
    def findByID(self, id):
        cursor = self.db.cursor()
        sql="select * from movies where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        return self.convertToDictionary(result)
    # Get id from movies
    def findID(self, id):
        cursor = self.db.cursor()
        sql="select id from movies where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return result
    # Update the movies in db
    def update_movie(self, values):
        cursor = self.db.cursor()
        sql="update movies set name= %s,genre=%s, description=%s, totalVotes=%s where id = %s"
        cursor.execute(sql, values)
        self.db.commit()
    # Delete movies by name
    def delete(self, name):
        cursor = self.db.cursor()
        sql="delete from movies where name = %s"
        values = (name,)

        cursor.execute(sql, values)

        self.db.commit()
        print("Delete Done")
    # Convert for movies
    def convertToDictionary(self, result):
        colnames=['id','name','genre', "description", "totalVotes"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
    # Convert for top movies
    def convertToDictionaryTop(self, result):
        colnames=['id','Title','Year']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
    # Function to add/remove votes
    def addVote(self, values):
        cursor = self.db.cursor()
        sql="update movies set totalVotes=totalVotes + %s where id = %s"
        cursor.execute(sql, values)
        self.db.commit()

movieDAO = MovieDAO()