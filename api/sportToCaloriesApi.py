import constants as const
import json
import requests


class SportCaloriesCalculator:

    def sport_search(self, term):
        print("Calculating calories for " + term)
        url = const.NUTRITIONIX_SPORT_URL
        headers_calories = {
            'x-app-id': const.NUTRITIONIX_SPORT_APP_ID,
            'x-app-key': const.NUTRITIONIX_SPORT_APP_KEY,
            'Content-Type': "application/json"
        }
        payload = {
            "query": term
        }
        payload_formatted = json.dumps(payload)
        response = requests.request("POST", url, data=payload_formatted, headers=headers_calories)
        res = response.json()
        res = res['exercises'][0]['nf_calories']
        print(res)
        return res