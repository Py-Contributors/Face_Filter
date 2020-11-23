#!/home/inspiron3551/anaconda3/bin/python
from app import app
from waitress import serve


if __name__ == "__main__":
    print("Starting server...")
    serve(app, host="0.0.0.0", port=5000)
