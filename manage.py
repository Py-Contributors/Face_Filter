#!/home/inspiron3551/anaconda3/bin/python
from waitress import serve

from main import app

if __name__ == "__main__":
    print("Starting server...")
    serve(app, host="0.0.0.0", port=8000)
