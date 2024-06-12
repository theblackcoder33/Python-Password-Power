import sys
import getpass
import platform

if platform.system() == 'Windows':
    import msvcrt
else:
    import termios
    import tty

def getpass_with_stars(prompt="Please enter password: "):
    if platform.system() == 'Windows':
        return getpass_with_stars_windows(prompt)
    else:
        return getpass_with_stars_unix(prompt)

def getpass_with_stars_windows(prompt):
    print(prompt, end='', flush=True)
    password = ''
    while True:
        char = msvcrt.getch()
        if char in {b'\r', b'\n'}:
            break
        elif char == b'\x08':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                print('\b \b', end='', flush=True)
        else:
            password += char.decode()
            print('*', end='', flush=True)
    print()  # For the newline after password input
    return password

def getpass_with_stars_unix(prompt):
    print(prompt, end='', flush=True)
    password = ''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)
            if char == '\n' or char == '\r':
                break
            elif char == '\x7f':
                if len(password) > 0:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            else:
                password += char
                print('*', end='', flush=True)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print()  # For the newline after password input
    return password

def check_password(password):
    length = len(password)
    
    # Check password length
    if length < 6:
        return "Password must be at least 6 characters long!"

    upper_chars = any(c.isupper() for c in password)
    lower_chars = any(c.islower() for c in password)
    digits = any(c.isdigit() for c in password)
    special_chars = any(not c.isalnum() for c in password)

    # Check for character types
    if not upper_chars:
        return "Password must contain at least one uppercase character!"
    if not lower_chars:
        return "Password must contain at least one lowercase character!"
    if not digits:
        return "Password must contain at least one digit!"
    if not special_chars:
        return "Password must contain at least one special character!"

    # Determine password strength
    if length >= 10:
        return "The strength of the password is strong."
    else:
        return "The strength of the password is medium."

# Get username (or other non-sensitive information) using input()
username = input("Please enter username: ")

# Get password securely using the custom function
password = getpass_with_stars()

# Check password and print the result
print(check_password(password))
