import requests
import os
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 95
HEIGHT_CM = 170
AGE = 40


try:
    APP_ID = os.environ["APP_ID"]
    API_KEY = os.environ["API_KEY"]
    SHEETY_AUTH = os.environ["SHEETY_AUTH"]
    SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]
except KeyError as err:
    print(f"{err} does not exist in OS environment variables")
else:

    exercise_endpoint = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"

    exercise_text = input("Tell me which exercises you did: ")

    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
    }

    parameters = {
        "query": exercise_text,
        "gender": GENDER,
        "weight_kg": WEIGHT_KG,
        "height_cm": HEIGHT_CM,
        "age": AGE
    }

    try:
        response = requests.post(exercise_endpoint, json=parameters, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        result = response.json()

        auth_headers = {
            "Authorization": SHEETY_AUTH
        }

        for exercise in result["exercises"]:
            sheety_parameters = {
                "workout": {
                    "date": datetime.now().strftime("%d/%m/%Y"),
                    "time": datetime.now().strftime("%X"),
                    "exercise": exercise["name"].title(),
                    "duration": exercise["duration_min"],
                    "calories": exercise["nf_calories"],
                }
            }

            try:
                sheety_response = requests.post(SHEETY_ENDPOINT, json=sheety_parameters, headers=auth_headers)
                sheety_response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
