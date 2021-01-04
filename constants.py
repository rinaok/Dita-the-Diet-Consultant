CLARIFAI_API_KEY = "e27baccbdfb4460494a83b54dadaaf9a"
CALORIES_API_KEY = "840ff1e8"
CALORIES_API_ID = "21f54da4361088ddca9e38c196cb87e0"
RECIPE_API_KEY = "c006a47b2aa749eb92a5b449de19cab4"
FB_TOKEN = "EAAEtROZBcc64BAJcWyblClEZAEIAIGIw3O4npXZCawXUX8wBMzzbz3DiCtFec44gEwJfKyJFB5JXbydyJb5ZCeJjpQ7Sc4FdddthSheZBuiukt5F3sllhLxS3HdLKoCpZAeax7XC3WIbQcdApt9tDxZCy3zOaZC3OW4yzVgWfPuUPgZDZD"
CALORIES_DEFAULT = 2600
SIGN_UP = "https://nullptr.chat/signup"
MENU = "https://nullptr.chat/recipe"

chatinfo = {"userid": "",
            "chatid": ""
            }

recipeInfo = {"restriction":"",
    "maxCalories":""
}

#### MONGO DB

MONGO_HOST = 'localhost:27017'
MONGO_USER = 'admin'
MONGO_PASSWORD = 'password'

#### DIET GOALS

MAINTAIN = 0
LOSE = 1
GAIN = 2

#### NUTRITIONIX food to calories API

NUTRITIONIX_URL="https://trackapi.nutritionix.com/v2/natural/nutrients"
NUTRITIONIX_APP_ID="9ee1d833"
NUTRITIONIX_APP_KEY="460fa637c6bf310caefd273c5151edcd"

#### NUTRITIONIX sport to calories API

NUTRITIONIX_SPORT_URL="https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRITIONIX_SPORT_APP_ID="4ea82404"
NUTRITIONIX_SPORT_APP_KEY="78cfb09ac9b98b5f174989c32276b5d9"


#### USER MENU

json_menu = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": chatinfo['userid']
        },
        "message": {
            "text": "Welcome to HealthBot! What would you like to do?",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Get meal calories",
                    "payload": "Get meal calories"
                },
                {
                    "content_type": "text",
                    "title": "Get a menu",
                    "payload": "Get a menu"
                },
                {
                    "content_type": "text",
                    "title": "Sport activities",
                    "payload": "Sport activities"
                },
                {
                    "content_type": "text",
                    "title": "Edit user's details",
                    "payload": "Edit user's details"
                },
                {
                    "content_type": "text",
                    "title": "Get today's status",
                    "payload": "Get today's status"
                }
            ]
        }
    }


def quick_replies(title, options):
    quick_replies_json = {"fulfillmentMessages": [
        {
          "quickReplies": {
            "title": title,
            "quickReplies": options
          },
          "platform": "FACEBOOK",
          "lang": "en"
        }]
    }
    return quick_replies_json
