"""
Sample Python Application with Intentional Security Issues
===========================================================
This app demonstrates common security vulnerabilities that 
Bandit (Python SAST tool) will detect.

Purpose: To be scanned by Bandit in the CI/CD pipeline
to demonstrate DevSecOps practices.
"""

import subprocess
import pickle
import os
from flask import Flask, request

app = Flask(__name__)

# ⚠️ SECURITY ISSUE #1: Hardcoded credentials (exposed in source code)
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-12345abcde"

# ⚠️ SECURITY ISSUE #2: Hardcoded secret in environment variable assignment
SECRET_TOKEN = "supersecret_token_12345"


@app.route("/")
def home():
    """Home endpoint - insecure information disclosure"""
    return {
        "message": "Welcome to Vulnerable App",
        "password": DATABASE_PASSWORD,  # ⚠️ Exposing password
        "api_key": API_KEY
    }


@app.route("/execute", methods=["POST"])
def execute_command():
    """
    ⚠️ SECURITY ISSUE #3: Command Injection vulnerability
    - Directly passes user input to shell command without sanitization
    """
    command = request.json.get("cmd")
    
    # Dangerous: subprocess with shell=True + user input
    result = subprocess.run(command, shell=True, capture_output=True)
    
    return {"output": result.stdout.decode()}


@app.route("/deserialize", methods=["POST"])
def deserialize_data():
    """
    ⚠️ SECURITY ISSUE #4: Insecure deserialization
    - Using pickle.loads() on user input allows arbitrary code execution
    """
    data = request.json.get("payload")
    
    # Dangerous: pickle.loads() on untrusted data
    obj = pickle.loads(data)
    
    return {"result": obj}


@app.route("/debug")
def debug_mode():
    """
    ⚠️ SECURITY ISSUE #5: Debug mode enabled in production
    - Exposes sensitive information and allows code execution
    """
    return os.environ.get("SECRET_DATA", "No data")


if __name__ == "__main__":
    # ⚠️ SECURITY ISSUE #6: Debug mode and insecure host binding
    app.run(debug=True, host="0.0.0.0", port=5000)
