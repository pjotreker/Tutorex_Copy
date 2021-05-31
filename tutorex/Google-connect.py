from Google import Create_Service
CLIENT_SECRET_FILE='client_secret_931883415580-u8abq0vriqvfberg8k0ddklvtj30g7ve.apps.googleusercontent.com.json'
API_NAME='drive'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/drive']

API_NAME_CALENDAR='calendar'
SCOPES_CALENDAR=['https://www.googleapis.com/auth/calendar']

service=Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

service_calendar=Create_Service(CLIENT_SECRET_FILE, API_NAME_CALENDAR, API_VERSION, SCOPES_CALENDAR)
#print(dir(service_calendar))