from pymongo import MongoClient

class Database():

    def __init__(self, connection_string:str ):
        self.__client = MongoClient( connection_string )
        self.__db = self.__client['snapzel']
    
    def get_collection( self,collection_name:str):
        return self.__db[collection_name]