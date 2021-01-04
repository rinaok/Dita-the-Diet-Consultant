# Functions according to intents
import base64

from api.foodRecognizer import FoodRecognizer
import constants as const
from api.mongodb import MongoDB
from api.caloriesApi import CaloriesCalculator
from api.sportToCaloriesApi import SportCaloriesCalculator
from user import User


class IntentsHandler:

    def __init__(self, request, debug_mode=False):
        self.request = request
        self.debug_mode = debug_mode
        if self.debug_mode:
            print(request)
        self.food_data = FoodRecognizer()
        self.mongo = MongoDB()
        self.calories_calculator = CaloriesCalculator()
        self.sport_calories_calculator = SportCaloriesCalculator()
        self.user = None
        self.original_detect_intent_request, self.payload, self.payload_data, self.sender_data, \
        self.recipient_data, self.query_result, self.query_text, self.attachments_list, \
        self.attached_url, self.intent_display_name, self.end_conversation, self.parameters_detail,\
        self.detail = self.parse_request(request)
        self.suffix = "What would you like to do next?"

    def parse_request(self, request):
        intent_display_name = request.get('queryResult', {}).get('intent', {}).get('displayName', '')
        original_detect_intent_request = request.get('originalDetectIntentRequest', dict())
        payload = original_detect_intent_request.get('payload', dict())
        payload_data = payload.get('data', dict())
        sender_data = payload_data.get('sender', dict())
        recipient_data = payload_data.get('recipient', dict())
        query_result = request.get('queryResult', dict())
        output_contexts = query_result.get('outputContexts', list())
        if len(output_contexts) > 0:
            parameters_detail = output_contexts[0].get('parameters', dict()).get('detail', list())
            if len(parameters_detail) > 0:
                detail = parameters_detail[0]
            else:
                detail = None
        else:
            parameters_detail = list()
            detail = None
        query_text = query_result.get('queryText', '')
        end_conversation = query_result.get('intent', dict()).get('endInteraction', False)
        attachments_list = payload_data.get('message', {}).get('attachments', list())
        if len(attachments_list) > 0:
            attached_url = attachments_list[0].get('payload', {}).get('url', '')
        else:
            attached_url = ''
        return (original_detect_intent_request, payload, payload_data, sender_data, recipient_data,
                query_result, query_text, attachments_list, attached_url, intent_display_name, end_conversation,
                parameters_detail, detail)

    def init_user(self, userid):
        user_item = self.mongo.get_user_by_id(userid)
        if user_item is not None:
            user = User(user_item['id'],
                        user_item['name'],
                        user_item['age'],
                        user_item['birthday'],
                        user_item['gender'],
                        user_item['height'],
                        user_item['weight'],
                        user_item['goal'],
                        user_item['activity'],
                        user_item['kosher'],
                        user_item['vegetarian'],
                        user_item['vegan'],
                        user_item['calories'])
            return user
        else:
            raise Exception(f"User ID {userid} was not found in the DB")

    def welcome(self):
        if self.sender_data:
            const.chatinfo['userid'] = str(self.sender_data.get('id', ''))
            const.chatinfo['chatid'] = str(self.recipient_data.get('id', ''))
        else:
            const.chatinfo['userid'] = 'None'
            const.chatinfo['chatid'] = 'None'
        user = self.mongo.get_user_by_id(const.chatinfo['userid'])
        if user is None:
            url_params = f"{const.chatinfo['userid']}&chatid={const.chatinfo['chatid']}"
            base64_message = self.encode_base64(url_params)
            fulfillment_text = {
                "fulfillmentText": f"Welcome to Dita the HealthBot! "
                                   f"Please sign up in the following form: {const.SIGN_UP}?params={str(base64_message)}"
            }
        else:
            fulfillment_text = const.quick_replies("Welcome to Dita the healthbot! What would you like to do?",
                                                   ["Get meal calories",
                                                    "Get a menu",
                                                    "Sport activities",
                                                    "Edit user's details",
                                                    "Get today's status"])
        return fulfillment_text

    def encode_base64(self, str_params):
        message_bytes = str_params.encode('ascii')  # convert to a bytes-like object
        base64_bytes = base64.b64encode(message_bytes)  # Base64 encode and store in Base64_bytes
        base64_message = base64_bytes.decode('ascii')  # get the string representation of the Base64 conversion
        if self.debug_mode:
            print("Original string params before Base64: " + str_params)
        return base64_message

    def switch_menu(self, option):
        if self.debug_mode:
            print("Got user request: " + option)
        return {
            "Get meal calories": "Please describe your meal or upload a picture of it",
            "Get a menu": self.get_todays_menu(),
            "Sport activities": "Please describe your sport activity",
            "Get today's status": self.get_todays_status(),
            "Edit user's details": const.quick_replies("What would you like to modify?",
                                                       ["Weight",
                                                        "Height",
                                                        "Diet Preference",
                                                        "Diet Restrictions",
                                                        "Activity Rate"])
        }.get(option, "Please choose an option from the menu")  # default if option not found

    def return_response_statement(self, response):
        if self.end_conversation:
            ful_response = const.quick_replies(f"{response}\n\n{self.suffix}", ["Continue to chat"])
            return ful_response
        else:
            return {"fulfillmentText": response}

    def get_todays_status(self):
        user = self.init_user(const.chatinfo['userid'])
        calories_left = float(self.mongo.query_db_column('calories_left'))
        response = None
        if user.goal == const.MAINTAIN or user.goal == const.LOSE:
            if calories_left <= 0:
                response = "Did you perform a sport activity today?"
            else:
                response = "You are doing great today! " \
                            f"You have {calories_left} calories left"
        else:
            if calories_left > 0:
                response = f"There are still {calories_left} left calories that need to be consumed in order to meet" \
                           " today’s goals"
            else:
                response = f"You gained today {abs(calories_left)} calories, you are doing great!"
        return self.return_response_statement(response)

    def get_todays_menu(self):
        user = self.init_user(const.chatinfo['userid'])
        if self.debug_mode:
            print("user details >> " , user)
        const.recipeInfo['maxCalories'] = self.mongo.query_db_column('calories_left')
        if user.kosher:
            const.recipeInfo['restriction'] = "kosher"
        if user.vegetarian:
            const.recipeInfo['restriction'] = "vegetarian"
        if user.vegan:
            const.recipeInfo['restriction'] = "vegan"
        url_params = f"apiKey={const.RECIPE_API_KEY}&maxCalories={const.recipeInfo['maxCalories']}" \
                     f"&restriction={const.recipeInfo['restriction']}"
        base64_message = self.encode_base64(url_params)
        response = f"This is your menu for today: {const.MENU}?params={str(base64_message)}"
        if self.debug_mode:
            print("get_todays_menu >>", response)
        return self.return_response_statement(response)

    def upload_image(self):
        if self.debug_mode:
            print("IMAGE: " + self.attached_url)
        response = self.food_data.get_top_ingr(self.attached_url)
        if self.debug_mode:
            print("Top ingr: " + str(response))
        response = self.get_calories_summary(response)
        return self.return_response_statement(response)

    def calories_calc(self):
        food_selection = self.query_text
        response = self.get_calories_summary(food_selection)
        return self.return_response_statement(response)

    def get_calories_summary(self, food_selection):
        food_search_result, current_calories = self.calories_calculator.food_search(food_selection)
        total_cal = self.mongo.query_db_column('calories_left')
        diff = float(total_cal) - current_calories
        self.mongo.store_calorie_count(str(diff), const.chatinfo['userid'])
        return f"Your meal contains the following:\n" \
                f"{food_search_result}\n" \
                f"Your remaining amount of calories for today is {diff}"

    def sport_calories_calc(self):
        sport_selection = self.query_text
        if self.debug_mode:
            print(sport_selection)
        calories_burn = self.sport_calories_calculator.sport_search(sport_selection)
        total_cal = self.mongo.query_db_column('calories_left')
        diff = float(total_cal) + float(calories_burn)
        self.mongo.store_calorie_count(str(diff), const.chatinfo['userid'])
        response = f"You burned {calories_burn} calories. Your remaining amount of calories for today is {diff}"
        return self.return_response_statement(response)

    def validate_input(self, field, value):
        valid = False
        if self.debug_mode:
            print(f"field: {field} - value: {value}")
        if field == 'weight' or field == 'height':
            valid = True
            if str(value).isnumeric():
                self.mongo.update_column(field, value)
            else:
                return f"Error: {field} must me a numeric value"

        elif field == 'diet preference':
            valid = True
            diet = const.MAINTAIN
            if "lose" in value:
                diet = const.LOSE
            elif "gain" in value:
                diet = const.GAIN
            self.mongo.update_column('goal', diet)

        elif field == 'diet restrictions':
            valid = True
            if "not" in value.lower():
                self.mongo.update_column(value.lower()[4:], False)
            else:
                self.mongo.update_column(value.lower(), True)

        elif field == 'activity rate':
            valid = True
            self.mongo.update_column('activity', value)
            self.update_calories()

        if valid:
            response = f"The {field} field was updated successfully!"
        else:
            response = "Invalid field to update, please try again"

        return self.return_response_statement(response)

    def update_calories(self):
        age_val = self.mongo.get_column(const.chatinfo['userid'], "age")
        gender_val = self.mongo.get_column(const.chatinfo['userid'], "gender")
        activity_val = self.mongo.get_column(const.chatinfo['userid'], "activity")
        current_total_calories = self.mongo.get_column(const.chatinfo['userid'], "calories")
        current_left_calories = self.mongo.get_column(const.chatinfo['userid'], "calories_left")
        calories_calulator = CaloriesCalculator()
        total_calories = calories_calulator.calculate_calories_according_to_activity(str(age_val['age']),
                                                                                     str(gender_val['gender']),
                                                                                     str(activity_val['activity']))
        diff = float(current_total_calories['calories']) - total_calories
        left_calories = float(current_left_calories['calories_left']) - diff
        self.mongo.update_column("calories", total_calories)
        self.mongo.update_column("calories_left", left_calories)

    def edit_field(self):
        if self.detail:
            new_val = str(self.query_text)
            return self.validate_input(self.detail.lower(), new_val)
        else:
            raise ValueError("parameter_detail is missing the field value")

    def edit_const_fields(self):
        fulfillment_text = {"fulfillmentText": f"Please enter your new {self.query_text.lower()}"}
        if self.query_text == 'Diet Preference':
            fulfillment_text = const.quick_replies("Please choose your new diet preference",
                                                   ["Want to lose weight",
                                                    "Want to gain weight",
                                                    "Maintain my weight"])
        elif self.query_text == 'Diet Restrictions':
            fulfillment_text = const.quick_replies("Please choose your new diet restriction",
                                                   ["Kosher",
                                                    "Vegetarian",
                                                    "Vegan",
                                                    "Not Kosher",
                                                    "Not Vegetarian",
                                                    "Not Vegan"])
        elif self.query_text == 'Activity Rate':
            fulfillment_text = const.quick_replies("Please choose your new activity rate",
                                                   ["Active",
                                                    "Moderate",
                                                    "Inactive"])
        else:
            fulfillment_text = {"fulfillmentText": f"Please enter your new {self.query_text.lower()}"}
        return fulfillment_text




