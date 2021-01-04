# Hackathon-winning

To run, commit the code and `git pull master` from the server.

First add API Keys here:
```python
        CLARIFAI_API_KEY = ""
        self.app_food_recognizer = ClarifaiApp(api_key=CLARIFAI_API_KEY)  # will use CLARIFAI_API_KEY as an api key
        self.calories_api_key = ""
        self.calories_api_id = ""
```

and here:

```python
querystring = {"appId": "",
               "appKey": ""
               }
```

To restart the `gunicorn` service on the server, run `sudo systemctl restart gunicorn.service`.
