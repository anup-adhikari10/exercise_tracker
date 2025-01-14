import requests
from datetime import datetime
import os



basic_auth_headers = {
    "Authorization": "Basic {os.environ['ENV_SHEETY_TOKEN']}"
}

GENDER = "MALE"
WEIGHT_KG = 70
HEIGHT_CM = 170
AGE = 24

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]
exercise_text  = input("Tell me what exercise you did: ")
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}


response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)



today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
sheet_response = requests.post(
    sheet_endpoint,
    json=sheet_inputs,
    auth=(
        os.environ["ENV_SHEETY_USERNAME"],
        os.environ["ENV_SHEETY_PASSWORD"],
    )
)

print(sheet_response.text)





