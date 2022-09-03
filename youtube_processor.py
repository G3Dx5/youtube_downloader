#!/usr/bin/env python3

import argparse
import json
from moviepy.editor import *
from mutagen.mp3 import MP3
import os
import pytube
from youtube_transcript_api import YouTubeTranscriptApi

'''
Code to download YouTube video, extract audio and convert to mp3.  After that go back to YouTube 
and get transcript. Then format into a more readbale version of JSON and provide cumulative duration
of mp3 audio in the nominated mp3 directory. 

Author: G3Dx5
Version: 0.0.2

TODO

[-] Make record of files 
[-] Add better error handling
[-] Improve JSON formatting 
Usage:  python3 youtube_processor -l "https://youtube.com/your_yt_video"

'''

''' Process input arguments '''
parser = argparse.ArgumentParser(description='YouTube Dowloader, extractor and transcript processor')
parser.add_argument("-l", "--YouTubeLink", help="YouTube Link")
args = parser.parse_args()

class Youtubeprocessor:
    ''' Dictionary for link, ID and output JSON file '''    
    video_data = {"YouTubeLink":[args.YouTubeLink],"Name":[],"ID":[], "JSONFile":[]}
    
    print("Querying YouTube....")

    @classmethod
    def getYTvideoName(cls) -> str:
        ''' Get YouTube Video name for naming the output files '''
        link: str = str(cls.video_data["YouTubeLink"])
        video_name: str = pytube.YouTube(link)
        title: str = video_name.streams[0].title
        cls.video_data["Name"] = title

    @classmethod
    def seperateYtID(cls) -> str:
        ''' Extract ID from the YouTube link and populate the dictionary '''
        raw_ID = str(cls.video_data["YouTubeLink"])
        ID = raw_ID.split("=")[1].split("&")[0].replace("'","").replace("]","")
        cls.video_data["ID"] = ID
    
    def convert_to_mp3(video, name) -> None:
        ''' convert YT video to mp3 '''
        video = VideoFileClip(os.path.join(video))
        name = video.audio.write_audiofile(os.path.join(name))

    @classmethod
    def getYouTubeVideo(cls,link) -> None:
        save_path = "."
        try:
            video = pytube.YouTube(str(link))
        except: 
            print("Connection Error, unable to reach YouTube")
        video_name = str(cls.video_data["Name"]) + ".mp4"
        stream = video.streams.first()
        try:
            stream.download(save_path)
        except: 
            print("Unable to download YouTube video") 
        os.rename(video.streams.first().default_filename, video_name)
        cls.convert_to_mp3(video_name, cls.video_data["Name"] + ".mp3")

    @classmethod
    def getTranscript(cls) -> None:
        ''' Get YouTube transcript '''
        ytID = cls.video_data["ID"]
        transcript = YouTubeTranscriptApi.get_transcript(ytID)
        JSON_name = cls.video_data["Name"]
        JSONFile = JSON_name + ".json"
        cls.video_data["JSONFile"] = JSONFile
        with open(JSONFile, 'w', encoding='utf-8') as json_file:
            json.dump(transcript, json_file)

    @classmethod
    def processJSON(cls):
        ''' Take JSON transcript from YouTube and reformat '''
        JSON_string = None
        with open(cls.video_data["JSONFile"]) as f:
            JSON_string = f.read()
        try:
            parsed_json = json.loads(JSON_string)
            formatted_json = json.dumps(parsed_json, indent = 4,sort_keys=True)
            with open(cls.video_data["Name"] + "_formatted" + ".json", "w") as tf:
                tf.write(formatted_json)
        except Exception as e:
            print(repr(e))


    def convertSeconds(seconds):
        ''' convert seconds to minute / hour units'''
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    @classmethod
    def getDuration(cls, path):
        ''' get mp3 video length '''
        tot_length = 0
        for root, dir, files in os.walk(os.path.abspath(path)):
            for file in files:
                if file.endswith(".mp3"):
                    audio = MP3(os.path.join(root, file))
                    length = audio.info.length
                    tot_length += length
            hours, minutes, seconds = cls.convertSeconds(tot_length).split(":")
        print("Total Duration in folder: " + str(int(hours)) + ':' + str(int(minutes)) + ':' + str(int(seconds)))

            
def main():
    Youtubeprocessor.getYTvideoName()
    Youtubeprocessor.seperateYtID()
    Youtubeprocessor.getYouTubeVideo(args.YouTubeLink)
    Youtubeprocessor.getTranscript()
    Youtubeprocessor.processJSON()
    #Youtubeprocessor.getDuration(".")
    
if __name__== "__main__" :
    main()




