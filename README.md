# Basic Event Management API

## Overview

This is a simple API for creating and watching a list of event.
No authentication is needed for getting a list of events, but you must provide an auth token when create a new event (add such header parameter: **Authorization = Token <put_your_authtoken_here>**).
Admin panel is also provided after setting up and running the project server (http://127.0.0.1:8000/admin/) <br>
Server supports such datetime format: **"day/month/year hours:minutes:seconds"** (e.g. 07/02/2023 19:11:05)

## Available API endpoints
The server is running at http://127.0.0.1:8000/ so this part will be omitted in the endpoints below.
+ POST /api/v1/users/signup/ - register a new user with the given 'email' and 'password'.
+ POST /api/v1/users/login/ - obtain an auth token for a user.
+ GET /api/v1/events/ - get a list of events.
+ POST /api/v1/events/ - create a new event (authorization required).

## Swagger UI
You can also visit http://127.0.0.1:8000/swagger/ to get more info about each certain endpoint. For using the closed endpoints firstly authorize in the Swagger UI entering Token(apiKey) like this: **Token <put_your_authtoken_here>**

## Usage
```bash
git clone https://github.com/Voorhees2019/EventManagementAPI.git
cd EventManagementAPI/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/manage.py migrate
python backend/manage.py createsuperuser
python backend/manage.py runserver
```
The project should be available on your localhost, check the output of your command line for more details.

## Testing
Simply run the tests by executing from the project root directory:
```bash
pytest
```
