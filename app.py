import base64

from flask import Flask, request, render_template, send_from_directory
from flask import jsonify
from werkzeug.utils import redirect
from tasks.updateCalories import reset_calories
from user import User
from intentsHandler import IntentsHandler
import os
from tasks.userQuery import RepeatEvery
import constants as const
from api.mongodb import MongoDB
from api.caloriesApi import CaloriesCalculator
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
calories_calulator = CaloriesCalculator()
mongo = MongoDB()

# Schedule a job to reset calories count every day
sched = BackgroundScheduler()
sched.add_job(reset_calories, 'cron', hour='0')
sched.start()


# Handle favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def welcome():
    return render_template('index.html')

def decode_base64(params):
    base64_bytes = params.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    print("Params decoded: " + message)
    params = message.split('&')
    return params


@app.route('/signup')
def signup_page():
    base64_message = request.args.get('params')
    if len(base64_message) > 1:
        if 'userid=' in base64_message[0]:
            const.chatinfo['userid'] = base64_message[0].split('userid=')[1]
        if 'chatid' in base64_message[1]:
            const.chatinfo['chatid'] = base64_message[1].split('chatid=')[1]
    return render_template('signup.html', userid=const.chatinfo['userid'], chatid=const.chatinfo['chatid'])


@app.route('/recipe')
def menu_page():
    base64_message = request.args.get('params')
    params = decode_base64(base64_message)
    if len(params) > 2:
        if 'apiKey=' in params[0]:
            const.RECIPE_API_KEY = params[0].split('apiKey=')[1]
        if 'maxCalories=' in params[1]:
            const.recipeInfo['maxCalories'] = params[1].split('maxCalories=')[1]
        if 'restriction=' in params[2]:
            const.recipeInfo['restriction'] = params[2].split('restriction=')[1]
    else:
        raise ValueError("Missing one parameter in URL params: " + str(params))
    return render_template('recipe.html', apiKey=const.RECIPE_API_KEY, maxCalories=const.recipeInfo['maxCalories'],
                           restriction=const.recipeInfo['restriction'])


@app.route('/post_fields', methods=['POST'])
def post_fields():
    const.chatinfo['userid'] = request.args.get('userid')
    const.chatinfo['chatid'] = request.args.get('chatid')
    print("Got fields from sign up form for user: " + const.chatinfo['userid'])
    kosher = False
    vegetarian = False
    vegan = False
    if request.form.get('vegetarian'):
        vegetarian = True
    if request.form.get('vegan'):
        vegan = True
    if request.form.get('kosher'):
        kosher = True
    birthday_year = request.form['birthday'].split("-")[0]
    birthday_month = request.form['birthday'].split("-")[1]
    birthday_day = request.form['birthday'].split("-")[2]
    now = datetime.datetime.now()
    age = now.year - int(birthday_year)
    if int(birthday_month) > now.month:
        age -= 1
    elif int(birthday_month) == now.month and int(birthday_day) > now.day:
        age -= 1
    calories = calories_calulator.calculate_calories_according_to_activity(age, request.form['gender'], request.form['activity'])
    goal = const.MAINTAIN
    if "lose" in request.form['preference']:
        goal = const.LOSE
    elif "gain" in request.form['preference']:
        goal = const.GAIN
    user = User(const.chatinfo['userid'], request.form['name'], age, request.form['birthday'], request.form['gender'],
                request.form['height'], request.form['weight'], goal,  request.form['activity'],
                kosher, vegetarian, vegan, calories)
    mongo.add_to_db(user)
    thread = RepeatEvery(3, const.chatinfo['userid'])
    print("Starting thread for user id " + const.chatinfo['userid'])
    thread.start()
    thread.join(21)  # allow thread to execute a while...
    thread.stop()
    print("Thread for user id " + const.chatinfo['userid'] + " has stopped")
    return redirect("https://www.facebook.com/messages/t/"+const.chatinfo['chatid'])


@app.route('/dialogflow', methods=["POST"])
def fullfillment():
    try:
        req_data = request.get_json()
        handler = IntentsHandler(request=req_data, debug_mode=True)
        response = dict()

        if handler.intent_display_name == 'Default Welcome Intent':
            response = handler.welcome()

        elif handler.intent_display_name == 'Get a menu':
            response = handler.get_todays_menu()

        elif handler.intent_display_name == 'Get todays status':
            response = handler.get_todays_status()

        elif handler.intent_display_name == 'Explore uploaded image':
            response = handler.upload_image()

        elif handler.intent_display_name == 'Get sport activity - custom':
            response = handler.sport_calories_calc()

        elif handler.intent_display_name == 'Meal description':
            response = handler.calories_calc()

        elif handler.intent_display_name == 'Edit personal details - field':
            response = handler.edit_const_fields()

        elif handler.intent_display_name == 'Edit personal details - getField':
            response = handler.edit_field()

        if len(response) == 0:
            raise ValueError(f"No intent found for request with intent display name: {handler.intent_display_name}")
        else:
            return jsonify(response)
    except Exception as e:
        print("Error: {}".format(e))


if __name__ == '__main__':
    app.run()
