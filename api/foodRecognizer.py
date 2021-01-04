# Food recognition on a picture or meal description

from clarifai.rest import ClarifaiApp
import json
import constants as const


class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


class FoodRecognizer:

    def __init__(self):
        self.app_food_recognizer = ClarifaiApp(api_key=const.CLARIFAI_API_KEY)  # will use CLARIFAI_API_KEY as an api key

    def get_top_ingr(self, img):
        dict_ingr = self.call_food_model(img)  # use ML to get the food in the picture
        top_ingr = self.top_ingr(dict_ingr)  # calculate the calories in the picture
        return top_ingr

    def call_food_model(self, imageUrl):
        # call the food model
        model = self.app_food_recognizer.models.get('food-items-v1.0')
        response = model.predict_by_url(imageUrl)
        return response

    def top_ingr(self, dict_ingr):
        ingredients = dict_ingr['outputs'][0]['data']['concepts']
        top_ingr = []
        i = 0
        total_calories = 0
        print("TOP INGREDIENTS: ")
        while ingredients[i]['value'] >= 0.9:
            top_ingr.append(ingredients[i]['name'])
            print(f"{i}. {ingredients[i]['name']}")
            i += 1
        return top_ingr
