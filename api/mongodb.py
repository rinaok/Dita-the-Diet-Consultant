# Queries to MongoDB

from pymongo import MongoClient
from pprint import pprint
import constants as const


class MongoDB:

    def __init__(self):
        self.mongo_client = MongoClient(host=[const.MONGO_HOST],
                                        username=const.MONGO_USER,
                                        password=const.MONGO_PASSWORD,
                                        connect=True)
        self.users_db = self.mongo_client["Users"]
        self.users_col = self.users_db["users"]

    def add_to_db(self, user):
        print("Adding a new user to the DB: {}".format(user.name))
        new_user = {"id": user.id, "name": user.name, "age": user.age, "birthday": user.birthday,
                    "gender": user.gender, "weight": user.weight, "height": user.height, "goal": user.goal,
                    "activity": user.activity, "kosher": user.kosher, "vegetarian": user.vegetarian,
                    "vegan": user.vegan, "calories": user.calories, "calories_left": user.calories}
        self.users_col.insert_one(new_user)

    def get_user_by_id(self, userid):
        print("Searching for user id: " + userid)
        query = {"id": userid}
        count = self.users_col.find(query).count()
        if count > 0:
            document = self.users_col.find_one(query)
            pprint(document)
            return document
        return None

    def get_info(self, userid):
        print("USER ID: " + userid)
        document = self.get_user_by_id(userid)
        if document is None:
            return None
        else:
            return document['age'], document['gender']

    def store_calorie_count(self, cal_count, userid):
        query = {"id": userid}
        new_value = {"$set": {"calories_left": cal_count}}
        self.users_col.update_one(query, new_value)
        print("Updated total calories of user {} to be {} calories".format(const.chatinfo['userid'], cal_count))

    def query_db_column(self, column):
        query = {"id": const.chatinfo['userid']}
        res = self.users_col.find_one(query)
        if res is not None:
            return res[column]
        else:
            return const.CALORIES_DEFAULT

    def update_column(self, column, new_value):
        query = {"id": const.chatinfo['userid']}
        new_value = {"$set": {column: new_value}}
        self.users_col.update_one(query, new_value)

    def all_users(self):
        return self.users_col.find()

    def get_column(self, userid, column):
        return self.users_col.find_one({"id": userid}, {column: 1})
