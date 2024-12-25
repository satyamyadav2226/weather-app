from flask import Flask, render_template, request
import requests

app = Flask(__name__)
api_key = "e8db3855a317bb437b89b8a836e128a7"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city").strip()
        if not city:
            error_message = "Please enter a valid city name."
        else:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": api_key,
                "units": "metric"
            }
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                data = response.json()

                weather_data = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "condition": data["weather"][0]["description"].capitalize(),
                    "wind_speed": data["wind"]["speed"]
                }
            except requests.exceptions.HTTPError:
                error_message = f"City '{city}' not found. Please check the name and try again."
            except requests.exceptions.RequestException:
                error_message = "An error occurred while fetching data. Please try again later."

    return render_template("index.html", weather=weather_data, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
