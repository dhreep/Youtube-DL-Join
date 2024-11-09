from pytubefix import YouTube
from pytubefix.cli import on_progress
import pandas as pd
import moviepy.editor as mp
import os

#save path
SAVE_PATH = r"C:\Users\Dhruv Bajaj\Desktop\ytdl\Youtube-DL-Join\dl_path"

def trim_vid(input_name:str,begin:int,fin:int,num:int):
    file = fr".\dl_path\{input_name}"
    # print(file)
    clip = mp.VideoFileClip(filename=file)
    clip = clip.subclip(begin,fin)
    #remove verbose and logger to show the building process
    clip.write_videofile(fr".\dl_path\{num}_{input_name}",verbose=False,logger=None)
    return clip


def dl_vid(link,name_vid):
    yt = YouTube(url=link,on_progress_callback=on_progress)
    print("Downloading "+ name_vid)
    vid = yt.streams.filter(file_extension="mp4",progressive=True).order_by("resolution").desc().first()
    vid.download(output_path=SAVE_PATH,filename=f"{name_vid}.mp4")
    print("\n")
    return f"{name_vid}.mp4"


def main():
    data = pd.read_csv(r"C:\Users\Dhruv Bajaj\Desktop\ytdl\Youtube-DL-Join\list.csv")
    ds = data.iloc[:].values
    #array to store all the clips
    final_merge = []
    for count,i in enumerate(ds):
        link = i[0]
        start = i[1]
        end = i[2]
        name = i[3]
        # print(link,start,end,name)
        input_name = dl_vid(link=link,name_vid=name)
        output = trim_vid(input_name=input_name,begin = int(start),fin = int(end),num=count)
        # print("input:"+input_name+"\n\noutput:"+output)
        final_merge.append(output)
    final_clip = mp.concatenate(final_merge)
    final_clip.write_videofile(fr".\dl_path\Final_Output.mp4")




if __name__ == "__main__":
    main()
