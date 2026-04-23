import urllib.request
import os

print("Downloading Face Scanner file... Please wait.")

url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
filename = "haarcascade_frontalface_default.xml"

try:
    urllib.request.urlretrieve(url, filename)
    print(" Success!.")
    print(f"File Location: {os.path.abspath(filename)}")
except Exception as e:
    print(f" Error: {e}")