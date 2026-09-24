import os
import hashlib

# 🛑 BUG 1: Hardcoded sensitive information (Security Risk)
API_SECRET_KEY = "SUPER_SECRET_AWS_KEY_12345"

def calculate_hash(user_input):
    # 🛑 BUG 2: Using an insecure, outdated hashing algorithm
    hasher = hashlib.md5()
    hasher.update(user_input.encode('utf-8'))
    return hasher.hexdigest()

def read_user_file(filename):
    # 🛑 BUG 3: Unhandled exception risk (No try/except block if file doesn't exist)
    # 🛑 BUG 4: Resource leak (Not using 'with' statement leaves file handles open)
    f = open(filename, 'r')
    data = f.read()
    print("File read completely!")
    return data

if __name__ == "__main__":
    print(calculate_hash("hello"))
    # 🛑 BUG 5: Plain print statement instead of standard logging modules

# Triggering a fresh AI pipeline execution run
