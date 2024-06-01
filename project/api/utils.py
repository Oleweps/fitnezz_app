from flask import Blueprint, request, jsonify, render_template
import requests

# Define your API keys
NUTRITIONIX_APP_ID = "85a22cab"
NUTRITIONIX_APP_KEY = "d5690657cf1755bba310a4b33c11f7ce"

def get_nutrition_data(query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_APP_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "query": query
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None
