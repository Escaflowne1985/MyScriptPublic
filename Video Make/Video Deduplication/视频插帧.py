# env inference.py/py
# -*- coding: UTF-8 -*-
'''
@Project ：inference.py 
@File    ：视频插帧.py
@IDE     ：PyCharm 
@Author  ：Mr数据杨
@Date    ：2023/8/8 10:13 
'''

# 插帧
import os
import random
from PIL import Image
import cv2
import subprocess
from moviepy.editor import VideoFileClip

video_path = "demo.mp4"
output_video = "output_video.mp4"

# 1. 使用ffmpeg将视频分解成帧
os.system('mkdir frames')
os.system('ffmpeg -i {} frames\\frame%04d.png'.format(video_path))

# 2. 获取视频分辨率
width, height = cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_WIDTH), cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_HEIGHT)
# print(width, height)

# 获取水印素材文件
image_files = os.listdir("image")

# 排序画面帧
frame_files = sorted(os.listdir('frames'))

for i, frame_file in enumerate(frame_files[::40], start=1):
    # 底片原始图片
    random_image = random.choice(image_files)
    frame_files_path = os.path.join("frames", frame_file)
    image1 = Image.open(frame_files_path).convert("RGBA")
    # 透明素材图片
    random_image_path = os.path.join("image", random_image)
    image2 = Image.open(random_image_path).convert("RGBA")
    image2 = image2.resize((int(width), int(height)))

    # 调整image2的透明度
    image2 = Image.blend(image1, image2, 0.1)
    # 保存融合后的图像
    image2.save(frame_files_path, "PNG")

# 3. 使用ffmpeg将所有帧重新组合成视频
os.system('ffmpeg -y -framerate 30 -i frames\\frame%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4')


def get_audio_duration(video):
    video_clip = VideoFileClip(video)
    duration = video_clip.duration
    return duration


input_audio_duration = get_audio_duration(video_path)
output_audio_duration = get_audio_duration("output.mp4")
print(input_audio_duration)
print(output_audio_duration)

# 根据音频长度判断是否加速或减速
if input_audio_duration < output_audio_duration:
    speed_change = input_audio_duration / output_audio_duration
    ffmpeg_speed_command = f'ffmpeg -y -i output.mp4 -filter:v "setpts={speed_change}*PTS" temp.mp4'
    subprocess.run(ffmpeg_speed_command, shell=True)
else:
    speed_change = output_audio_duration / input_audio_duration
    ffmpeg_speed_command = f'ffmpeg -y -i output.mp4 -filter:v "setpts={speed_change}*PTS" temp.mp4'
    subprocess.run(ffmpeg_speed_command, shell=True)

# 将原视频的音频合并到新视频中
merge_audio_cmd = f"ffmpeg -i temp.mp4 -i {video_path} -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -shortest {output_video[:-4]}_insert.mp4"
subprocess.run(merge_audio_cmd, shell=True)

# 删除临时文件
subprocess.run("del temp.mp4", shell=True)
subprocess.run("del output.mp4", shell=True)
