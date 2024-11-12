import os
import requests
import json
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("x-rapidapi-key")
api_host = os.getenv("x-rapidapi-host")

url = "https://basketball-head.p.rapidapi.com/players/jamesle01/games/2024"

payload = { "pageSize": 100 }
headers = {
	"x-rapidapi-key": api_key,
	"x-rapidapi-host": api_host,
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    player_stats = response.json()

    with open("lebron_games.json", "w") as outfile:
        json.dump(player_stats, outfile, indent=4)  # Indentation for readability

else:
    print(f"Error: API request failed with status code {response.status_code}")