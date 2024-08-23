from datetime import *
import tkinter
import webbrowser
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from PIL import Image, ImageTk
from tkinter import messagebox
import smtplib
import urllib.request
import requests
import pytz

# ---------- Window ---------- #

window = tkinter.Tk()
window.title("Weather App")
window.geometry("900x700+300+200")
window.config(bg="#fff", padx=10, pady=5)
window.resizable(False, False)


# ---------- CONSTANTS ---------- #

SEARCH_IMG = ImageTk.PhotoImage(Image.open("images/search.png"))
CURRENT_IMG = ImageTk.PhotoImage(Image.open("images/logo.png"))
BOX_IMG = ImageTk.PhotoImage(Image.open("images/box.png"))
WIND_IMG = ImageTk.PhotoImage(Image.open("images/wind.png").resize((60, 60)))
HUMIDITY_IMG = ImageTk.PhotoImage(Image.open("images/humidity.png").resize((60, 60)))
DESCRIPTION_IMG = ImageTk.PhotoImage(Image.open("images/temperature.png").resize((60, 60)))
PRESSURE_IMG = ImageTk.PhotoImage(Image.open("images/pressure.png").resize((60, 60)))
SEARCH_ICON = ImageTk.PhotoImage(Image.open("images/search_icon.png").resize((40, 40)))

CLEAR_IMG = ImageTk.PhotoImage(Image.open("images/clear.png").resize((260, 260)))
CLOUDS_IMG = ImageTk.PhotoImage(Image.open("images/clouds.png").resize((260, 260)))
DRIZZLE_IMG = ImageTk.PhotoImage(Image.open("images/drizzle.png").resize((260, 260)))
ATMOSPHERE_IMG = ImageTk.PhotoImage(Image.open("images/haze.png").resize((260, 260)))
RAIN_IMG = ImageTk.PhotoImage(Image.open("images/rain.png").resize((260, 260)))
SNOW_IMG = ImageTk.PhotoImage(Image.open("images/snow.png").resize((260, 260)))
THUNDERSTORM_IMG = ImageTk.PhotoImage(Image.open("images/thunderstorm.png").resize((260, 260)))

CLEAR_IMG_small = ImageTk.PhotoImage(Image.open("images/clear.png").resize((60, 60)))
CLOUDS_IMG_small = ImageTk.PhotoImage(Image.open("images/clouds.png").resize((60, 60)))
DRIZZLE_IMG_small = ImageTk.PhotoImage(Image.open("images/drizzle.png").resize((60, 60)))
ATMOSPHERE_IMG_small = ImageTk.PhotoImage(Image.open("images/haze.png").resize((60, 60)))
RAIN_IMG_small = ImageTk.PhotoImage(Image.open("images/rain.png").resize((60, 60)))
SNOW_IMG_small = ImageTk.PhotoImage(Image.open("images/snow.png").resize((60, 60)))
THUNDERSTORM_IMG_small = ImageTk.PhotoImage(Image.open("images/thunderstorm.png").resize((60, 60)))

FONT_NAME = "Microsoft YaHei UI Light"
MY_API_KEY = "YOUR_API_KEY" # Your OpenWeatherMap API key from https://home.openweathermap.org/api_keys

weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# ---------- Global Variables ---------- #
search_img: tkinter.Label   # Search image
search_entry: tkinter.Entry # Search entry
search_icon: tkinter.Button # Search icon

title_label: tkinter.Label  # Title label
time_label: tkinter.Label   # Time label
current_weather: tkinter.Label  # Current weather image
current_dg: tkinter.Label   # Current temperature
current_details: tkinter.Label  # Current details

wind_label: tkinter.Label   # Wind label
wind_: tkinter.Label    # Wind value
humidity_label: tkinter.Label   # Humidity label
humidity_: tkinter.Label    # Humidity value
description_label: tkinter.Label    # Description label
description_: tkinter.Label   # Description value
pressure_label: tkinter.Label   # Pressure label
pressure_: tkinter.Label    # Pressure value

# Daily weather UI
frame: tkinter.Frame    # Frame for daily weather

day1_frame: tkinter.Frame   # Frame for day 1
day1_label: tkinter.Label   # Day 1 label
day1_img: tkinter.Label # Day 1 image
day1_label_day: tkinter.Label   # Day 1 day temperature
day1_label_night: tkinter.Label # Day 1 night temperature

day2_frame: tkinter.Frame   # Frame for day 2
day2_label: tkinter.Label   # Day 2 label
day2_img: tkinter.Label # Day 2 image
day2_label_day: tkinter.Label   # Day 2 day temperature
day2_label_night: tkinter.Label # Day 2 night temperature

day3_frame: tkinter.Frame   # Frame for day 3
day3_label: tkinter.Label   # Day 3 label
day3_img: tkinter.Label # Day 3 image
day3_label_day: tkinter.Label   # Day 3 day temperature
day3_label_night: tkinter.Label # Day 3 night temperature

day4_frame: tkinter.Frame   # Frame for day 4
day4_label: tkinter.Label   # Day 4 label
day4_img: tkinter.Label # Day 4 image
day4_label_day: tkinter.Label   # Day 4 day temperature
day4_label_night: tkinter.Label # Day 4 night temperature

day5_frame: tkinter.Frame   # Frame for day 5
day5_label: tkinter.Label   # Day 5 label
day5_img: tkinter.Label # Day 5 image
day5_label_day: tkinter.Label   # Day 5 day temperature
day5_label_night: tkinter.Label # Day 5 night temperature

day6_frame: tkinter.Frame   # Frame for day 6
day6_label: tkinter.Label   # Day 6 label
day6_img: tkinter.Label # Day 6 image
day6_label_day: tkinter.Label   # Day 6 day temperature
day6_label_night: tkinter.Label # Day 6 night temperature

day7_frame: tkinter.Frame   # Frame for day 7
day7_label: tkinter.Label   # Day 7 label
day7_img: tkinter.Label # Day 7 image
day7_label_day: tkinter.Label   # Day 7 day temperature
day7_label_night: tkinter.Label # Day 7 night temperature

# ---------- Functions ---------- #

def search_weather():
    """
    Searches for the weather data of the city entered the search box.

    :return: None
    """

    city = search_entry.get()

    if not is_entry_valid(city):
        return

    is_city_valid, lat, lng = search_city(city)

    if not is_city_valid:
        return

    bool_, \
        current_temp, \
        feels_like, \
        pressure, \
        humidity, \
        wind_speed, \
        weather_id, \
        description, \
        main_description, \
        timezone, \
        daily_data = get_weather_data(lat, lng)

    weather_icon = check_weather_icon(weather_id)
    current_weather.config(image=weather_icon)
    current_dg.config(text=f"{current_temp}°C")
    current_details.config(text=f"{main_description} | Feels like {feels_like}")
    wind_.config(text=f"{wind_speed}m/s")
    humidity_.config(text=f"{humidity}%")
    description_.config(text=description)
    pressure_.config(text=pressure)
    config_daily(daily_data)
    search_timezone(timezone)


def config_daily(daily_data):
    """
    Configures the UI for displaying the 7-day weather forecast.

    :param daily_data: List of dictionaries containing the daily weather data
    :return: None
    """

    day1_label_day.config(text=f"Day:{daily_data[0]['temp']['day']}°C")
    day1_label_night.config(text=f"Night:{daily_data[0]['temp']['night']}°C")
    day1_img.config(image=check_weather_icon_small(daily_data[0]["weather"][0]["id"]))

    day2_label_day.config(text=f"Day:{daily_data[1]['temp']['day']}°C")
    day2_label_night.config(text=f"Night:{daily_data[1]['temp']['night']}°C")
    day2_img.config(image=check_weather_icon_small(daily_data[1]["weather"][0]["id"]))

    day3_label_day.config(text=f"Day:{daily_data[2]['temp']['day']}°C")
    day3_label_night.config(text=f"Night:{daily_data[2]['temp']['night']}°C")
    day3_img.config(image=check_weather_icon_small(daily_data[2]["weather"][0]["id"]))

    day4_label_day.config(text=f"Day:{daily_data[3]['temp']['day']}°C")
    day4_label_night.config(text=f"Night:{daily_data[3]['temp']['night']}°C")
    day4_img.config(image=check_weather_icon_small(daily_data[3]["weather"][0]["id"]))

    day5_label_day.config(text=f"Day:{daily_data[4]['temp']['day']}°C")
    day5_label_night.config(text=f"Night:{daily_data[4]['temp']['night']}°C")
    day5_img.config(image=check_weather_icon_small(daily_data[4]["weather"][0]["id"]))

    day6_label_day.config(text=f"Day:{daily_data[5]['temp']['day']}°C")
    day6_label_night.config(text=f"Night:{daily_data[5]['temp']['night']}°C")
    day6_img.config(image=check_weather_icon_small(daily_data[5]["weather"][0]["id"]))

    day7_label_day.config(text=f"Day:{daily_data[6]['temp']['day']}°C")
    day7_label_night.config(text=f"Night:{daily_data[6]['temp']['night']}°C")
    day7_img.config(image=check_weather_icon_small(daily_data[6]["weather"][0]["id"]))


def check_weather_icon(weather_id):
    """
    Returns the weather icon based on the weather id.

    :param weather_id: The weather id
    :return: The weather icon
    """

    code = int(str(weather_id)[0])
    if code == 2:
        return THUNDERSTORM_IMG
    if code == 3:
        return DRIZZLE_IMG
    if code == 5:
        return RAIN_IMG
    if code == 6:
        return SNOW_IMG
    if code == 7:
        return ATMOSPHERE_IMG
    if weather_id == 800:
        return CLEAR_IMG
    if code == 8:
        return CLOUDS_IMG


def check_weather_icon_small(weather_id):
    """
    Returns the small weather icon based on the weather id.

    :param weather_id: The weather id
    :return: The small weather icon
    """

    code = int(str(weather_id)[0])
    if code == 2:
        return THUNDERSTORM_IMG_small
    if code == 3:
        return DRIZZLE_IMG_small
    if code == 5:
        return RAIN_IMG_small
    if code == 6:
        return SNOW_IMG_small
    if code == 7:
        return ATMOSPHERE_IMG_small
    if weather_id == 800:
        return CLEAR_IMG_small
    if code == 8:
        return CLOUDS_IMG_small


def get_weather_data(lat, lng):
    """
    Gets the weather data from the OpenWeatherMap API.

    :param lat: The latitude of the location
    :param lng: The longitude of the location
    :return: The weather data
    """

    if not is_connected_to_internet():
        show_error_message_box("Please make sure you are connected to the internet")
        return False, "", "", "", "", "", "", ""

    parameters = {
        "lat": lat,
        "lon": lng,
        "appid": MY_API_KEY,
        "exclude": "minutely",
        "units": "metric"
    }

    response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
    response.raise_for_status()

    weather_data = response.json()
    timezone_ = weather_data["timezone"]
    current_temp = weather_data["current"]["temp"]
    feels_like = weather_data["current"]["feels_like"]
    pressure = weather_data["current"]["pressure"]
    humidity = weather_data["current"]["humidity"]
    wind_speed = weather_data["current"]["wind_speed"]
    weather_id = weather_data["current"]["weather"][0]["id"]
    description = weather_data["current"]["weather"][0]["description"]
    main_description = weather_data["current"]["weather"][0]["main"]
    daily_data = weather_data["daily"]

    return True, current_temp, feels_like, pressure, humidity, wind_speed, weather_id, description, main_description, timezone_, daily_data


def is_connected_to_internet():
    """
    Checks if the user is connected to the internet.

    :return: True if connected, False otherwise
    """

    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False


def search_timezone(result):
    """
    Searches for the timezone of the city entered the search box.

    :param result: The timezone of the city
    :return: None
    """

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    time_label.config(text=current_time)


def search_city(city):
    """
    Searches for the city entered in the search box.

    :param city: The city entered in the search box
    :return: The latitude and longitude of the city
    """

    try:
        geolocator = Nominatim(user_agent="HectorCode")
        location = geolocator.geocode(city)
        location_lat = location.latitude
        location_lng = location.longitude
        # result = TimezoneFinder().timezone_at(lng=location_lng, lat=location_lat)
        return True, location_lat, location_lng
    except:
        show_error_message_box("This city is not valid. Please enter a valid city.")
        return False, "", ""


def is_entry_valid(entry):
    """
    Checks if the entry is valid.

    :param entry: The entry to check
    :return: True if valid, False otherwise
    """

    if not is_entry_empty(entry):
        return False

    if not is_entry_letters(entry):
        return False

    return True


def is_entry_letters(entry):
    """
    Checks if the entry contains only letters.

    :param entry: The entry to check
    :return: True if valid, False otherwise
    """

    if any(not letter.isalpha() for letter in entry if letter != " "):
        show_error_message_box("Please enter valid city")
        return False

    return True


def is_entry_empty(entry):
    """
    Checks if the entry is empty.

    :param entry: The entry to check
    :return: True if valid, False otherwise
    """

    if len(entry) == 0:
        show_error_message_box("Please enter a city")
        return False

    return True


def show_error_message_box(msg):
    """
    Shows an error message box.

    :param msg: The message to display
    :return: None
    """

    messagebox.showerror(title="Oops", message=msg)


def weekday(n):
    """
    Returns the weekday based on the number of days from the current day.

    :param n: The number of days from the current day
    :return: The weekday
    """

    day = datetime.now().weekday()

    for i in range(n):
        day += 1

        if day > 6:
            day = 0

    return weekdays[day]


# ---------- UI ---------- #

def initialize_gui():
    """
    Initializes the GUI.
    :return: None
    """

    initialize_search_box_entry()
    initialize_current_weather_ui()
    initialize_weather_details_ui()
    initialize_daily_weather_ui()


def initialize_search_box_entry():
    """
    Initializes the search box and entry UI.
    :return: None
    """

    # Search box & Entry UI
    global search_img, search_entry, search_icon
    search_img = tkinter.Label(image=SEARCH_IMG, bg="white")
    search_img.place(x=150, y=20)

    search_entry = tkinter.Entry(window, border=0, fg="white", bg="#404040", highlightthickness=0, justify="center",
                                 width=17, font=("poppins", 25, "bold"))
    search_entry.insert(0, "johannesburg")
    search_entry.place(x=180, y=40)
    search_entry.focus()

    search_icon = tkinter.Button(image=SEARCH_ICON, borderwidth=0, cursor="hand2", bg="#404040", highlightthickness=0,
                                 command=search_weather)
    search_icon.place(x=550, y=36)


def initialize_current_weather_ui():
    """
    Initializes the current weather UI.

    :return: None
    """

    # Current weather UI
    global title_label, time_label, current_weather, current_dg, current_details
    title_label = tkinter.Label(text="Current Weather", font=("arial", 25, "bold"), fg="#5F9EA0", bg="white")
    title_label.place(x=250, y=90)
    time_label = tkinter.Label(text="Time", font=("arial", 15, "bold"), fg="#5F9EA0", bg="white")
    time_label.place(x=250, y=125)

    current_weather = tkinter.Label(image=CURRENT_IMG, highlightthickness=0, bg="white")
    current_weather.place(x=50, y=150)

    current_dg = tkinter.Label(text="", font=("arial", 40, "bold"), fg="#5F9EA0", bg="white")
    current_dg.place(x=330, y=200)

    current_details = tkinter.Label(text="", font=("arial", 15, "bold"), fg="#5F9EA0", bg="white")
    current_details.place(x=330, y=300)


def initialize_weather_details_ui():
    """
    Initializes the weather details UI.

    :return: None
    """

    # Weather details UI
    global wind_label, wind_, humidity_label, humidity_, description_label, description_, pressure_label, pressure_
    wind_label = tkinter.Label(text="Wind", fg="#A9A9A9", bg="white", font=("Helvetica", 15, "bold"))
    wind_ = tkinter.Label(text="...m/s", fg="#A9A9A9", bg="white", font=("Helvetica", 15, "bold"))
    wind_label.place(x=710, y=120)
    wind_.place(x=710, y=145)
    tkinter.Label(image=WIND_IMG, highlightthickness=0, bg="white").place(x=650, y=110)

    humidity_label = tkinter.Label(text="Humidity", fg="#A9A9A9", bg="white", font=("Helvetica", 15, "bold"))
    humidity_ = tkinter.Label(text="...%", fg="#A9A9A9", bg="white", font=("Helvetica", 15, "bold"))
    humidity_label.place(x=710, y=220)
    humidity_.place(x=710, y=245)
    tkinter.Label(image=HUMIDITY_IMG, highlightthickness=0, bg="white").place(x=650, y=210)

    description_label = tkinter.Label(text="Description", fg="#A9A9A9", bg="white", font=("Helvetica", 15, "bold"))
    description_ = tkinter.Label(text="...", fg="#A9A9A9", bg="white", font=("Helvetica", 15, "bold"))
    description_label.place(x=710, y=320)
    description_.place(x=710, y=345)
    tkinter.Label(image=DESCRIPTION_IMG, highlightthickness=0, bg="white").place(x=650, y=310)

    pressure_label = tkinter.Label(text="Pressure", fg="#A9A9A9", bg="white", font=("Helvetica", 15, "bold"))
    pressure_ = tkinter.Label(text="...", fg="#A9A9A9", bg="white", font=("Helvetica", 15, "bold"))
    pressure_label.place(x=710, y=420)
    pressure_.place(x=710, y=445)
    tkinter.Label(image=PRESSURE_IMG, highlightthickness=0, bg="white").place(x=650, y=410)


def initialize_daily_weather_ui():
    """
    Initializes the daily weather UI.
    :return: None
    """

    # Daily weather UI
    global frame, day1_frame, day1_label, day1_img, day1_label_day, day1_label_night
    global day2_frame, day2_label, day2_img, day2_label_day, day2_label_night
    global day3_frame, day3_label, day3_img, day3_label_day, day3_label_night
    global day4_frame, day4_label, day4_img, day4_label_day, day4_label_night
    global day5_frame, day5_label, day5_img, day5_label_day, day5_label_night
    global day6_frame, day6_label, day6_img, day6_label_day, day6_label_night
    global day7_frame, day7_label, day7_img, day7_label_day, day7_label_night

    frame = tkinter.Frame(width=900, height=180, bg="gray")
    frame.pack(padx=5, pady=5, side=tkinter.BOTTOM)

    day1_frame = tkinter.Frame(frame, width=118, height=150, bg="#A9A9A9")
    day1_frame.place(x=10, y=10)
    # day1_weekday = weekday(1)
    day1_label = tkinter.Label(day1_frame, text=weekday(1), fg="white", bg="#A9A9A9", font=("Helvetica", 13, "bold"))
    day1_label.place(x=38, y=10)
    day1_img = tkinter.Label(day1_frame, image=CLEAR_IMG_small, highlightthickness=0, bg="#A9A9A9")
    day1_img.place(x=25, y=30)
    day1_label_day = tkinter.Label(day1_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day1_label_day.place(x=0, y=95)
    day1_label_night = tkinter.Label(day1_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day1_label_night.place(x=0, y=120)

    day2_frame = tkinter.Frame(frame, width=118, height=150, bg="#A9A9A9")
    day2_frame.place(x=130, y=10)
    day2_label = tkinter.Label(day2_frame, text=weekday(2), fg="white", bg="#A9A9A9", font=("Helvetica", 13, "bold"))
    day2_label.place(x=38, y=10)
    day2_img = tkinter.Label(day2_frame, image=CLEAR_IMG_small, highlightthickness=0, bg="#A9A9A9")
    day2_img.place(x=25, y=30)
    day2_label_day = tkinter.Label(day2_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day2_label_day.place(x=0, y=95)
    day2_label_night = tkinter.Label(day2_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day2_label_night.place(x=0, y=120)

    day3_frame = tkinter.Frame(frame, width=118, height=150, bg="#A9A9A9")
    day3_frame.place(x=250, y=10)
    day3_label = tkinter.Label(day3_frame, text=weekday(3), fg="white", bg="#A9A9A9", font=("Helvetica", 13, "bold"))
    day3_label.place(x=38, y=10)
    day3_img = tkinter.Label(day3_frame, image=CLEAR_IMG_small, highlightthickness=0, bg="#A9A9A9")
    day3_img.place(x=25, y=30)
    day3_label_day = tkinter.Label(day3_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day3_label_day.place(x=0, y=95)
    day3_label_night = tkinter.Label(day3_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day3_label_night.place(x=0, y=120)

    day4_frame = tkinter.Frame(frame, width=118, height=150, bg="#A9A9A9")
    day4_frame.place(x=370, y=10)
    day4_label = tkinter.Label(day4_frame, text=weekday(4), fg="white", bg="#A9A9A9", font=("Helvetica", 13, "bold"))
    day4_label.place(x=38, y=10)
    day4_img = tkinter.Label(day4_frame, image=CLEAR_IMG_small, highlightthickness=0, bg="#A9A9A9")
    day4_img.place(x=25, y=30)
    day4_label_day = tkinter.Label(day4_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day4_label_day.place(x=0, y=95)
    day4_label_night = tkinter.Label(day4_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day4_label_night.place(x=0, y=120)

    day5_frame = tkinter.Frame(frame, width=118, height=150, bg="#A9A9A9")
    day5_frame.place(x=490, y=10)
    day5_label = tkinter.Label(day5_frame, text=weekday(5), fg="white", bg="#A9A9A9", font=("Helvetica", 13, "bold"))
    day5_label.place(x=38, y=10)
    day5_img = tkinter.Label(day5_frame, image=CLEAR_IMG_small, highlightthickness=0, bg="#A9A9A9")
    day5_img.place(x=25, y=30)
    day5_label_day = tkinter.Label(day5_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day5_label_day.place(x=0, y=95)
    day5_label_night = tkinter.Label(day5_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day5_label_night.place(x=0, y=120)

    day6_frame = tkinter.Frame(frame, width=118, height=150, bg="#A9A9A9")
    day6_frame.place(x=610, y=10)
    day6_label = tkinter.Label(day6_frame, text=weekday(6), fg="white", bg="#A9A9A9", font=("Helvetica", 13, "bold"))
    day6_label.place(x=38, y=10)
    day6_img = tkinter.Label(day6_frame, image=CLEAR_IMG_small, highlightthickness=0, bg="#A9A9A9")
    day6_img.place(x=25, y=30)
    day6_label_day = tkinter.Label(day6_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day6_label_day.place(x=0, y=95)
    day6_label_night = tkinter.Label(day6_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day6_label_night.place(x=0, y=120)

    day7_frame = tkinter.Frame(frame, width=118, height=150, bg="#A9A9A9")
    day7_frame.place(x=730, y=10)
    day7_label = tkinter.Label(day7_frame, text=weekday(7), fg="white", bg="#A9A9A9", font=("Helvetica", 13, "bold"))
    day7_label.place(x=38, y=10)
    day7_img = tkinter.Label(day7_frame, image=CLEAR_IMG_small, highlightthickness=0, bg="#A9A9A9")
    day7_img.place(x=25, y=30)
    day7_label_day = tkinter.Label(day7_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day7_label_day.place(x=0, y=95)
    day7_label_night = tkinter.Label(day7_frame, text="", fg="white", bg="#A9A9A9", font=("Helvetica", 12, "bold"))
    day7_label_night.place(x=0, y=120)


if __name__ == "__main__":
    initialize_gui()
    window.mainloop()
