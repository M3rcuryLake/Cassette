import json

def json_to_srt(json_file_path, srt_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)	
        print(data)

    with open(srt_file_path, 'w') as srt_file:
        index = 1
        for subtitle in data:
            start_time = subtitle['start']
            end_time = subtitle['end']
            text = subtitle['word']

            srt_file.write(f"{index}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{text}\n\n")

            index += 1

# Example usage
json_file_path = 'subs.json'
srt_file_path = 'subs.srt'

json_to_srt(json_file_path, srt_file_path)

