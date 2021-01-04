# At the end of the day, reset the number of calories left for each user in the DB

from api.mongodb import MongoDB


def reset_calories():
    print("Resetting calories for all users since it's a new day!")
    mongo = MongoDB()
    users_lst = list(mongo.all_users())
    print(users_lst)
    for user in users_lst:
        print("Running for user: " + user['name'])
        new_value = mongo.get_column(user['id'], 'calories')
        print("Got new val: " + str(new_value['calories']))
        mongo.store_calorie_count(str(new_value['calories']), user['id'])
        print("updated calories for user " + user['id'])
