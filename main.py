from g4f.client import Client
import requests
import assemblyai as aai
from pydub import AudioSegment
import random 
from moviepy.editor import *
from math import ceil
from os import system
import sys
from unrealspeech import UnrealSpeechAPI, play, save
import seewav
import tempfile
from pathlib import Path
from time import sleep




assmebly_ai_api = "<ADD YOUR OWN API KEY (AssemblyAI) >"
urs_api = "<ADD YOUR OWN API KEY (UnrealSpeech)>"

def pfp_wave(buzz):
    if buzz==1:
        video_p='pictures/Denn.png'
    if buzz==2:
        video_p='pictures/Jed.jpeg'        
    if buzz==3:
        video_p='pictures/Jess.jpeg'
    if buzz==4:
        video_p='pictures/K-11.jpeg'
    if buzz==5:
        video_p='pictures/Kee.png'                   
    if buzz==6:
        video_p='pictures/Kell.jpeg'
    if buzz==7:
        video_p='pictures/Ron.jpeg'
    
    #use seewav to generate waveform video
    #The 'seewav' module in the given codebase is a modded version of a pull request by @Phoenix616 in the github page of the base seewav module

    with tempfile.TemporaryDirectory() as tmp:
        seewav.visualize(audio=Path('output.mp3'),
                        tmp=Path(tmp),
                        out=Path("waves.mp4"),
                        fg_color=[1, 0.78, 0],
                        bg_color=[0.21, 0.22, 0.24],
                        size=(480, 480),
                        bars=70
                        )
    
    
    video= VideoFileClip("waves.mp4")
    video_duration = video.duration
    x_pos = 20
    y_pos = 'center' 

    title = (
        ImageClip(video_p)
        .set_pos((x_pos, y_pos))
        .resize(height=150)
    )
    final = CompositeVideoClip([video.set_duration(video_duration), title.set_duration(video_duration)])
    final.write_videofile("wave_out.mp4")


def v_merger(file1, file2):

    #split screen two videos

    clip1 = VideoFileClip(file1)
    clip2 = VideoFileClip(file2)
 
    final = clips_array([[clip1], [clip2]])
    final.write_videofile("merged.mp4")


def a_mixer(num):

    #mixes base audio with a background music

    if num==1: au_path = "Minecraft"
    if num==2: au_path = "Subwoofer_Lullaby"
    if num==3: au_path = "Moog_City_2"

    sound1 = AudioSegment.from_file(f"music/{au_path}.mp3", format="mp3")
    sound2 = AudioSegment.from_file("output.mp3", format="mp3")

    overlay = sound2.overlay(sound1, position=0)
    overlay.export("F_output.mp3", format="mp3")

def backdrop(buzz):

    #subclips the gameplay video according to the playtime of the audio

    #buzz=QuerList('backdrop')
    audio_path='output.mp3'

    if buzz==1:
        video_path='backdrop/minecraft.mp4'
    if buzz==2:
        video_path='backdrop/fh5.mp4'        
    if buzz==3:
        video_path='backdrop/gtav.mp4'
    if buzz==4:
        video_path='backdrop/trackmania.mp4'


    def aud_dur(file_path):
       audio_file = AudioSegment.from_file(file_path)
       duration = audio_file.duration_seconds
       return duration
    

    def vid_dur(file_path):
       TempClip= VideoFileClip(file_path)
       vid_duration=TempClip.duration
       return vid_duration
    

    audio_duration = aud_dur(audio_path)
    video_duration = vid_dur(video_path)
    print(f"Audio Duration: {audio_duration} seconds, Video Duration: {video_duration}")
    
    s_time = random.randint(0,ceil(video_duration-(audio_duration + 5)))
    e_time = s_time+ ceil(audio_duration)
    print(s_time, e_time)
    video= VideoFileClip(video_path).subclip(s_time,e_time)
    video.write_videofile('temp1.mp4')

def sub_append():

    #adds subtitle

    system("ffmpeg -i subs.srt subtitle.ass")   
    ass_file_path = 'subtitle.ass'
    new_style_definition = 'Style: Default,Permanent Marker,15 ,&H0099ff,&Hffffff,&H0,&H0,1,0,0,0,100,100,0,0,1,1,2,5,50,50,50,1\n'
 
    with open(ass_file_path, 'r', encoding='utf-8') as file:
         lines = file.readlines()

    for line in lines:
        if line.strip().startswith('Style:'):
            lines[(lines.index(line))]=new_style_definition
    with open('subtitle.ass', 'w') as file:
        file.write(''.join(lines))
    
    system('''ffmpeg -i temp2.mp4 -vf "ass=subtitle.ass" -c:a copy -c:v libx264 -crf 23 -preset veryfast Final_Output.mp4''')


def add_aud(fil, aud):
    
    #adds audio to the given video
    
    videoclip = VideoFileClip(fil)
    audioclip = AudioFileClip(aud)

    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile("temp2.mp4", codec='libx264', audio_codec='aac')


def subs():

    #generates subtitles using AssemblyAI API  

    aai.settings.api_key = assmebly_ai_api
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe('./output.mp3')
    with open(f'subs.srt', 'a+') as handler:
        handler.write(transcript.export_subtitles_srt())

def model(buzz):

    #generates Transcript of the video using g4f gpt 3.5 Turbo model

    client = Client()
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Just answer the given question under 60 words in English, DO NOT include any titles, bullet points, Citations, or any special charecters, just the transcript. Now here is the Prompt :  " + buzz  }],
    )
    gen=response.choices[0].message.content
    return(gen)

def voice_charecter(charecter, trs):

    #generates voice

    api_key = urs_api
    speech_api = UnrealSpeechAPI(api_key)
    text_to_speech = trs
    timestamp_type = "sentence"  # Choose from 'sentence' or 'word'
    voice_id = charecter  # Choose the desired voice
    bitrate = "192k"
    speed = 0 
    pitch = 1.0
    audio_data = speech_api.speech(text=text_to_speech,voice_id=voice_id, bitrate=bitrate, timestamp_type=timestamp_type, speed=speed, pitch=pitch)
    save(audio_data, "output.mp3")


def clear():
    if sys.platform.startswith('linux'):
        system("clear")
    elif sys.platform.startswith('win'):
        system("cls")
    print('\033[94m'+'''
░░      ░░░░      ░░░░      ░░░░      ░░░        ░░        ░░        ░░        ░
▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒  ▒▒▒▒▒▒▒
▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓      ▓▓▓▓      ▓▓▓      ▓▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓  ▓▓▓▓▓      ▓▓▓
█  ████  ██        ████████  ████████  ██  ███████████  ████████  █████  ███████
██      ███  ████  ███      ████      ███        █████  ████████  █████        █
                                                                      
''')

def cleanup():
    if sys.platform.startswith('linux'): system("rm -rf F_output.mp3 merged.mp4 output.mp3 subs.srt subtitle.ass temp1.mp4 temp2.mp4 wave_out.mp4 waves.mp4")
    elif sys.platform.startswith('win'): system("del F_output.mp3 merged.mp4 output.mp3 subs.srt subtitle.ass temp1.mp4 temp2.mp4 wave_out.mp4 waves.mp4")

def main():
    clear()
    QueryList={}
    QueryList["script"]=input('\033[94m'+'''1. Transcript Prompt :
    
>>>  ''')
    clear()
    QueryList["music"]=int(input('''\n2. Use Background music?
2.1 : Minecraft (press 1)
2.2 : Subwoofer Lullaby (press 2)
2.3 : Moog City 2 (press 3)

>>> '''))
    clear()
    QueryList["voices"]=input(f'''\n3. Coose a voice :
3.1 : Dan: Young Male
3.2 : Will: Mature Male
3.3 : Scarlett: Young Female
3.4 : Liv: Young Female
3.5 : Amy: Mature Female

>>> ''')
    clear()
    QueryList["backdrop"]=int(input('''4. Choose a background game.
4.1 : Minecraft (press 1)
4.2 : Forza Horizon 5 (press 2)
4.3 : GTAV (press 3)
4.4 : trackmania (press 4)


>>>'''))
    clear()
    QueryList["charecter"]=int(input('''4. Choose a charecter image.
5.1 : Denn (press 1)
5.2 : Jed (press 2)
5.3 : Jess (press 3)
5.4 : K-11 (press 4)
5.5 : Kee (press 5)
5.6 : Kell (press 6)
5.7 : Ron (press 7)           

>>>'''))
#    clear()
    
    script = model(QueryList['script'])
    sleep(2)
    print(script)
    print('\n'+'Script Generated\n')
    
    voice_charecter(QueryList['voices'], script)
    print('\n'+' Voice Generated\n')
    sleep(2)
    subs()
    
    backdrop(QueryList["backdrop"])
    print('\n Backdrop Generated\n')
   
    pfp_wave(QueryList['charecter'])
    sleep(2)
    a_mixer(QueryList['music'])
    v_merger('wave_out.mp4', 'temp1.mp4')
    add_aud("merged.mp4", "F_output.mp3")
    sleep(2)
    sub_append()
    print("\n Job Finished")
    
    delr=input("delete all non essential files? (y/n) : ")
    if delr=="y" : cleanup()
    if delr=="n" : pass
    
if __name__ == "__main__":
    _is_main = True
    main()
    
    



    
       

