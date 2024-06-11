from os import system
import sys
from time import sleep
import requests

print("""[*] BEFORE EXECUTION 
Sign Up at AssmeblyAI (https://www.assemblyai.com/) and 
UnrealSpeech (https://unrealspeech.com/) and replace
the variables assembly_ai_api and urs_api with your own API.
The code uses the font "Permanant Marker" which is located in the
./assets/ directory. Make sure to install it before proceeding. 
Tested on GNU/Linux (Ubuntu 22.04 Jammy-Jellyfish) only.
(idk about windows)


Continuing in 8 sec.""")
sleep(8)

print("MAKE SURE PYTHON-PIP IS INSTALLED")

res = requests.get("https://google.com")
if res.status_code == 200:
    print('Internet Connectivity : OK')
    if sys.platform.startswith('linux'):
        system('''sudo apt-get install -y python3-dev libasound2-dev ffmpeg''')
        system('''pip install -r requirements.txt''')
        print("[*] Setup completed, Execute the script with 'python3 main.py'")
        
    elif sys.platform.startswith('win'):
        system('''pip install -r requirements.txt''')
        print("[*] Setup completed, Execute the script with 'python main.py'")
        
    else:
        print("[*] ERROR : make sure pip is set to path")

else :
    print('Internet Connectivity : False')

        

