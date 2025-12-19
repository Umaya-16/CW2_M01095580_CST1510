import bcrypt # bcrypt is used to hash passwords securely so they are not stored in plain text
import re # re is used for regular expressions to check if usernames and passwords match certain rules
import os # os is used to check if the user file exists before trying to read it

# this function makes a password safe by hashing it
def hash_password(password):
    binary_password = password.encode("utf-8") # turn the password into bytes
    salt = bcrypt.gensalt() # make a random salt
    hashed = bcrypt.hashpw(binary_password, salt) # hash the password with the salt
    return hashed.decode("utf-8") # turn it back into text so I can save it

# this function checks if the password matches the saved hash
def valid_hash(password, hashed):
    bin_pwd = password.encode("utf-8") # turn the password into bytes
    bin_hash = hashed.encode("utf-8") # turn the saved hash into bytes
    return bcrypt.checkpw(bin_pwd, bin_hash) # compare them

# check if the username is ok (letters, numbers, underscore, at least 3 chars)
def validate_username(username):
    return bool(re.match(r"^[A-Za-z0-9_]{3,}$", username)) # regex makes sure username is valid

# check if the password is strong enough
def validate_password(password):
    if len(password) < 8: # must be at least 8 characters
        return False
    if not re.search(r"[A-Z]", password): # must have a capital letter
        return False
    if not re.search(r"[a-z]", password): # must have a lowercase letter
        return False
    if not re.search(r"[0-9]", password): # must have a number
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): # must have a symbol
        return False
    return True # if all checks pass then the password is strong

# this is for registering a new user
def register_user():
    user_name = input("Enter your Username: ").strip() # get username input
    if not validate_username(user_name): # check if username is valid
        print("Invalid username. Must be at least 3 characters and alphanumeric.")
        return

    password = input("Enter your Password: ").strip() # get password input
    password_confirm = input("Repeat your Password: ").strip() # confirm password

    if password != password_confirm: # check if passwords match
        print("Passwords do not match.")
        return

    if not validate_password(password): # check if password is strong
        print("Weak password. Must be at least 8 characters, include uppercase, lowercase, number, and symbol.")
        return

    hashed = hash_password(password) # hash the password
    with open("user.txt", "a") as f: # open the file in append mode
        f.write(f"{user_name},{hashed}\n") # save username and hashed password
    print("User registered successfully!")

# this is for logging in
def login_user():
    user_name = input("Enter your Username: ").strip() # get username input
    password = input("Enter your Password: ").strip() # get password input

    if not os.path.exists("user.txt"): # check if user file exists
        print("No users registered yet.")
        return False

    with open("user.txt", "r") as f: # open the file in read mode
        lines = f.readlines() # read all lines

        for line in lines: # loop through each line
            u_name, hashed = line.strip().split(",") # split into username and hash
            if user_name == u_name: # check if username matches
                if valid_hash(password, hashed): # check if password matches hash
                    print("Login successful!")
                    return True
                else:
                    print("Invalid password.")
                    return False
    print("Username not found.") # if no username matched
    return False