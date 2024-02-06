# env inference.py/py
# -*- coding: UTF-8 -*-
'''
@Project ：inference.py 
@File    ：视频补帧.py
@IDE     ：PyCharm 
@Author  ：Mr数据杨
@Date    ：2023/8/8 10:13 
'''

import os
import random
import shutil
import os
import shutil
import random
import os
import subprocess
from moviepy.editor import VideoFileClip

video_path = "demo.mp4"
output_video = "output_video.mp4"

# 1. 使用ffmpeg将视频分解成帧
os.system('mkdir frames')
os.system('ffmpeg -i demo.mp4 frames/frame%04d.png')

frame_files = sorted(os.listdir('frames'))


def copy_and_rename_random_images(source_folder, destination_folder, min_count=10, max_count=30):
    image_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    # 计算要复制的图片数量
    num_images_to_copy = random.randint(min_count, max_count)

    n = 0
    # 随机选择并复制图片
    selected_images = random.sample(image_files, num_images_to_copy)
    for image in selected_images:
        source_path = os.path.join(source_folder, image)
        destination_path = os.path.join(destination_folder, f"{image}_copy.png")
        shutil.copy(source_path, destination_path)
        n = n + 1
    print("复制出来 {} 帧".format(str(n)))


source_folder = "frames"
destination_folder = "frames"

# 调用函数进行复制和重命名操作
copy_and_rename_random_images(source_folder, destination_folder)

# 3. 重新命名所有帧以保持连续性
all_frames = sorted(os.listdir('frames'))
for idx, frame in enumerate(all_frames, start=1):
    os.rename(f'frames\\{frame}', f'frames\\new_frame{idx:04d}.png')

# 3. 使用ffmpeg将所有帧重新组合成视频
frame_files = sorted(os.listdir('frames'))
os.system('ffmpeg -y -framerate 30 -i frames/new_frame%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4')


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
    ffmpeg_speed_command = f'ffmpeg -y -i demo.mp4 -filter:v "setpts={speed_change}*PTS" temp.mp4'
    subprocess.run(ffmpeg_speed_command, shell=True)
else:
    speed_change = output_audio_duration / input_audio_duration
    ffmpeg_speed_command = f'ffmpeg -y -i demo.mp4 -filter:v "setpts={speed_change}*PTS" temp.mp4'
    subprocess.run(ffmpeg_speed_command, shell=True)


# 将原视频的音频合并到新视频中
merge_audio_cmd = f"ffmpeg -y -i temp.mp4 -i {video_path} -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -shortest {output_video[:-4]}_add.mp4"
subprocess.run(merge_audio_cmd, shell=True)

# 删除临时文件
subprocess.run("del temp.mp4", shell=True)
subprocess.run("del output.mp4", shell=True)


