#!/usr/bin/env python3

import argparse
import json
from moviepy.editor import *
import os
import pytube
from youtube_transcript_api import YouTubeTranscriptApi


''' Process input arguments '''
parser = argparse.ArgumentParser(description='YouTube Dowloader, extractor and transcript processor')
parser.add_argument("-l", "--YouTubeLink", help="YouTube Link")
args = parser.parse_args()

''' Dictionary for link, ID and output JSON file '''
video_data = {"YouTubeLink":[args.YouTubeLink],"Name":[],"ID":[], "JSONFile":[]}


def getYTvideoName() -> str:
    ''' Get YouTube Video name for naming the output files '''
    link = str(video_data["YouTubeLink"])
    video_name = pytube.YouTube(link)
    title = video_name.streams[0].title
    video_data["Name"] = title

def seperateYtID() -> str:
    ''' Extract ID from the YouTube link and populate the dictionary '''
    raw_ID = str(video_data["YouTubeLink"])
    ID = raw_ID.split("=")[1].split("&")[0].replace("'","").replace("]","")
    video_data["ID"] = ID

def convert_to_mp3(video, name) -> None:
    ''' convert YT video to mp3 '''
    video = VideoFileClip(os.path.join(video))
    name = video.audio.write_audiofile(os.path.join(name))

def getYouTubeVideo(link) -> None:
    save_path = "."
    try:
        video = pytube.YouTube(str(link))
    except: 
        print("Connection Error, unable to reach YouTube")
    video_name = str(video_data["Name"]) + ".mp4"
    stream = video.streams.first()
    try:
        stream.download(save_path)
    except: 
        print("Unable to download YouTube video") 
    os.rename(video.streams.first().default_filename, video_name)
    convert_to_mp3(video_name, video_data["Name"] + ".mp3")

def getTranscript() -> None:
    ''' Get YouTube transcript '''
    ytID = video_data["ID"]
    transcript = YouTubeTranscriptApi.get_transcript(ytID)
    JSON_name = video_data["Name"]
    JSONFile = JSON_name + ".json"
    video_data["JSONFile"] = JSONFile
    with open(JSONFile, 'w', encoding='utf-8') as json_file:
        json.dump(transcript, json_file)

def processJSON():
    ''' Take JSON transcript from YouTube and reformat '''
    JSON_string = None
    with open(video_data["JSONFile"]) as f:
        JSON_string = f.read()
    try:
        parsed_json = json.loads(JSON_string)
        formatted_json = json.dumps(parsed_json, indent = 4,sort_keys=True)
        with open(video_data["Name"] + "_formatted" + ".json", "w") as tf:
            tf.write(formatted_json)
    except Exception as e:
        print(repr(e))

            
def main():
    getYTvideoName()
    seperateYtID()
    getYouTubeVideo(video_data["YouTubeLink"])
    getTranscript()
    processJSON()
    
if __name__== "__main__" :
    main()

