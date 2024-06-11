import requests
import json

url = "https://api.v6.unrealspeech.com/speech"

payload = {
    "Text": "This is a test",
    "VoiceId": "Scarlett",
    "Bitrate": "192k",
    "Speed": "0",
    "Pitch": "1",
    "TimestampType": "word"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "Bearer EgDQ8NlKEcZhvSDqnewrSqgoKSCXMvWTO1BozKgmBJy15embpNoM80"
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)


res = json.loads(response.text)
r = requests.get(res["OutputUri"])
with open("audio.mp3", 'wb') as f:
    for i in r : f.write(i)
k = requests.get(res["TimestampsUri"])
with open("subs.json", 'wb') as f:
    for i in k : f.write(i)

