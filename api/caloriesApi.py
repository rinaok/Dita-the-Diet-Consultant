# Calculate calories in a meal

import constants as const
import json
import requests


class CaloriesCalculator:

    def calculate_calories_according_to_activity(self, age, gender, active_rate):
        age = int(age)
        max_calories = const.CALORIES_DEFAULT
        if gender == "Male":
            if age < 30:
                if active_rate == "Inactive":
                    max_calories = 2600
                elif active_rate == "Moderately":
                    max_calories = 2800
                elif active_rate == "Active":
                    max_calories = 3000
            elif age > 30 and age < 50:
                if active_rate == "Inactive":
                    max_calories = 2400
                elif active_rate == "Moderately":
                    max_calories = 2600
                elif active_rate == "Active":
                    max_calories = 3000
            else:
                if active_rate == "Inactive":
                    max_calories = 2200
                elif active_rate == "Moderately":
                    max_calories = 2400
                elif active_rate == "Active":
                    max_calories = 2800
        else:
            if age < 30:
                if active_rate == "Inactive":
                    max_calories = 2000
                elif active_rate == "Moderately":
                    max_calories = 2200
                elif active_rate == "Active":
                    max_calories = 2400
            if age > 30 and age < 50:
                if active_rate == "Inactive":
                    max_calories = 1800
                elif active_rate == "Moderately":
                    max_calories = 2000
                elif active_rate == "Active":
                    max_calories = 2200
            else:
                if active_rate == "Inactive":
                    max_calories = 1600
                elif active_rate == "Moderately":
                    max_calories = 1800
                elif active_rate == "Active":
                    max_calories = 2200
        return max_calories

    def food_search(self, term):
        url = const.NUTRITIONIX_URL
        headers_calories = {
            'x-app-id': const.NUTRITIONIX_SPORT_APP_ID,
            'x-app-key': const.NUTRITIONIX_SPORT_APP_KEY,
            'Content-Type': "application/json"
        }
        str_items = ""
        if type(term) is list:
            for item in term:
                str_items += f"{item} and "
        else:
            str_items = term

        payload = {
            "query": str_items,
            "timezone": "US/Eastern"
        }
        print(f"Sending request: {payload}")
        payload_formatted = json.dumps(payload)
        response = requests.request("POST", url, data=payload_formatted, headers=headers_calories)
        res = response.json()
        if 'foods' not in res:
            print("Error, no food options returned for " + str(term))
            return "Sorry, I couldn't figure it out", 0
        print(f"NUTRITIONIX API response: {len(res['foods'])} types of foods")
        total = 0
        response = ""
        for item in res['foods']:
            response += f"{item['food_name']} ({item['serving_qty']} {item['serving_unit']}):" \
                        f" {item['nf_calories']} calories\n"
            total += round(item['nf_calories'])
        response += f"Total Calories: {total}"
        return response, total
