#!/usr/bin/env python

import os
from moviepy.editor import *
import pytube

''' Script to download YouTube videoa and convert to .mp3'''


''' convert video to audio (moviepy), write out the  audio file '''

def convert_to_mp3(video, name) -> None:
    video = VideoFileClip(os.path.join(video))
    name = video.audio.write_audiofile(os.path.join(name))

''' get the video from YT URL, extract the title, rename to the title, covert to 
.mp3 then delete the original .mp4'''

def get_vid(link) -> None:
    save_path = "."
    try:
        yt = pytube.YouTube(link)
    except: 
        print("Connection Error, unable to reach YouTube")
    title = yt.streams[0].title
    video_name = title + ".mp4"
    stream = yt.streams.first()
    try:
        stream.download(save_path)
    except: 
        print("Unable to download the YouTube video") 
    os.rename(yt.streams.first().default_filename, video_name)
    convert_to_mp3(video_name, title + ".mp3")
    os.remove(video_name)

get_vid("place YT_link_here")

