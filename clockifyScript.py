import requests
import pytz
from datetime import datetime
import json
import os

API_BASE_URL = "https://api.clockify.me/api/v1"
GLOBAL_BASE_URL = "https://global.api.clockify.me/"
FERIADOS_API_URL = "http://nolaborables.com.ar/api/v2/feriados/"
TIME_ENTRIES_GLOBAL = "/timeEntries"
TIME_ENTRIES = "/time-entries"
WORKSPACES = "/workspaces/"

# Reemplazar api token en archivo apiToken
API_TOKEN = ""
MOBILE_WORKSPACE = "65d4ae69961c52426de70bf6"
CONECTORES_BEES_PROJECT_ID = "65d4be4719c439782df7b39b"


def make_api_request(url, method, headers=None, data=None):
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            print("Invalid HTTP method.")
            return None
        print("request hecho a : " + url)
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None


def make_clockify_api_request(baseUrl, method, endpoint, data):

    url = baseUrl + WORKSPACES + MOBILE_WORKSPACE + endpoint
    headers = {
        "X-Api-Key": API_TOKEN,
        "content-type": "application/json",
    }
    return make_api_request(url, method, headers, data)


def cargar_horas():
    current_date = datetime.now(pytz.timezone("Etc/GMT+3"))
    time_9am_today = current_date.replace(
        hour=9, minute=0, second=0, microsecond=0
    ).isoformat()
    time_1pm_today = current_date.replace(
        hour=13, minute=0, second=0, microsecond=0
    ).isoformat()
    time_2pm_today = current_date.replace(
        hour=14, minute=0, second=0, microsecond=0
    ).isoformat()
    time_6pm_today = current_date.replace(
        hour=18, minute=0, second=0, microsecond=0
    ).isoformat()

    time_info_map = {
        0: [time_9am_today, time_1pm_today],
        1: [time_2pm_today, time_6pm_today],
    }

    for i in range(2):
        data = {
            "projectId": CONECTORES_BEES_PROJECT_ID,
            "description": "default",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "start": time_info_map[i][0],
            "end": time_info_map[i][1],
            "billable": "true",
            "type": "REGULAR",
        }
        response = make_clockify_api_request(API_BASE_URL, "POST", TIME_ENTRIES, data)


def get_recent_time_logs():
    return make_clockify_api_request(
        GLOBAL_BASE_URL, "GET", TIME_ENTRIES_GLOBAL + "/recent?limit=8", None
    )


def todayEsFeriado():
    today = datetime.now()

    url = FERIADOS_API_URL + str(today.year)

    params = {
        "formato": "mensual",
    }

    url = f"{url}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"

    response = make_api_request(url, "GET", None, None)
    data = json.dumps(response)
    parsedData = json.loads(data)
    feriados_del_mes = parsedData[today.month - 1]

    return today.day in feriados_del_mes


def read_api_token_from_file():
    tokenValue = None
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "apiToken.json")
        print(file_path)
        with open(file_path, "r") as file:
            data = json.load(file)
            tokenValue = data.get("token")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON.")
    return tokenValue


API_TOKEN = read_api_token_from_file()
recentLogs = get_recent_time_logs()

# Esto se hace por si se cargan a mano horas (dias flex) o por si se corre mas de una vez el script
if recentLogs and len(recentLogs) != 0:
    print("----------Ya hay registro de horas en el sistema-----")
    print(recentLogs)
else:
    if datetime.now().weekday() < 5 and (not todayEsFeriado()):
        cargar_horas()
        print("----------Horas cargadas, hasta la vista----------")
    else:
        print("----------Como vas a laburar feriado o finde?-----")
