import os
import requests
import datetime
from google.oauth2.credentials import Credentials 
from requests.structures import CaseInsensitiveDict
import json

Combined_calendar_data = []
SCOPES = []