class User:

    def __init__(self, userid: str, name: str, age: int, birthday: str, gender: str, height: int, weight: int,
                 goal: str, activity: str, kosher: bool, vegetarian: bool, vegan: bool, calories: int):
        """
       Handles the initialization of the user class.
       :param userid: User ID of the user.
       :param name: Name of the user.
       :param age: Age in years of the user.
       :param birthday: Date of birth of the user.
       :param gender: Gender of the user. (male, female)
       :param height: Height in centimeters of the user.
       :param weight: Weight in kilograms of the user.
       :param goal: Can be either "Want to lose weight", Want to gain weight", or "Want to maintain
                    current weight".
       :param activity: Options are "Active", "Moderately", and "Inactive".
       :param kosher: bool of the user's kosher status.
       :param vegetarian: bool of the user's vegetarian status.
       :param vegan: bool of the user's vegan status.
       :param calories: Daily Calories (int)
       """
        self.id = userid
        self.name = name
        self.age = age
        self.gender = gender
        self.weight = weight
        self.height = height
        self.goal = goal
        self.kosher = kosher
        self.vegetarian = vegetarian
        self.vegan = vegan
        self.activity = activity
        self.calories = calories
        self.birthday = birthday
