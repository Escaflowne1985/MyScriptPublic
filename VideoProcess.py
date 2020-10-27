#coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '合成视频的处理方法'
from moviepy.editor import *
import subprocess
import cv2
import numpy as np



# 将图片按照顺序逐一放入movei模板中
def AddImageInBase(jpg_list,mp3_duration,title):
    # 判断如果没有该数据的文件夹就创建
    start_time = 0
    image_list = []
    for num in range(len(jpg_list)):
        # 获取该字段字符串
        words = jpg_list[num]
        # 每段字幕时长
        every_part_duration_time = mp3_duration / len(jpg_list)
        # 图片数据
        jpg_path = "./materials/" + title + "/clean_jpg/" + jpg_list[num]
        image_clip = (
            ImageClip(jpg_path)
                .set_duration(every_part_duration_time)  # 水印持续时间
                .resize(height=650)  # 水印的高度，会等比缩放
                .set_pos(("center", 0))  # 水印的位置
                .set_start(start_time)
        )
        start_time = start_time + every_part_duration_time
        image_list.append(image_clip)

    # 载入背景视频
    path = "materials_base/base.mp4"
    video = VideoFileClip(path).resize((1280, 720)).set_duration(mp3_duration)
    cvc = CompositeVideoClip([video] + image_list, size=(1280, 720))
    cvc.write_videofile("./materials/" + title + "/data/jpg.mp4", fps=60, remove_temp=False, verbose=True)
    print("图片和背景视频合成完毕，保存目录：","./materials/" + title + "/data/")

# 将字幕按照顺序逐一放入movei模板中
def AddStrsAndMp3InBase(strs_list,mp3_duration,title,font_path):
    # 合成字幕到模板视频中
    # 判断如果没有该数据的文件夹就创建
    start_time = 0
    result_list = []
    for num in range(len(strs_list)):
        # 获取该字段字符串
        words = strs_list[num]
        # 每段字幕时长
        every_part_duration_time = mp3_duration / len(strs_list)
        # 字幕数据
        title_clip = (
            TextClip(strs_list[num], font=font_path, fontsize=50, color='white', method='label')
                .set_position(("center", "bottom"))
                .set_duration(every_part_duration_time)
                .set_start(start_time)
        )
        start_time = start_time + every_part_duration_time
        result_list.append(title_clip)

    # 载入背景视频
    path = "./materials/" + title + "/data/jpg.mp4"
    video = VideoFileClip(path).resize((1280, 720)).set_duration(mp3_duration)
    cvc = CompositeVideoClip([video] + result_list, size=(1280, 720))
    cvc.write_videofile("./materials/" + title + "/data/strs.mp4", fps=60, remove_temp=False, verbose=True)
    # 将MP3合成到视频中
    subprocess.call('ffmpeg -i ' + "./materials/" + title + "/data/strs.mp4"
                    + ' -i ' + 'materials/' + title + '/data/' + title + '.mp3' + ' -strict -2 -f mp4 '
                    + 'materials/' + title + '/data/result.mp4', shell=True)
    print("字幕、解说和背景视频合成完毕，保存目录：","./materials/" + title + "/data/")

# 生成封面视频
def MakeCoverVideo(title):
    from PIL import Image
    # 将制作的封面图片生成视频
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    size = (1280, 720)
    vw = cv2.VideoWriter('{}'.format("./materials/" + title + "/data/cover.mp4"), fourcc=fourcc, fps=10, frameSize=size)
    f_read = cv2.imdecode(np.fromfile("./materials/" + title + "/clean_jpg/cover.jpg", dtype=np.uint8),
                          cv2.IMREAD_COLOR)
    f_img = Image.fromarray(f_read)
    f_rs = f_img.resize([1280, 720], resample=Image.NONE)
    f_out = np.array(f_rs)
    vw.write(f_out)
    vw.release()

    print("封面视频制作完毕，保存目录：","./materials/" + title + "/data/")

# 封面视频添加title
def CoverImageAddTitle(title,font_path):
    # 封面视频添加title
    # 将字幕处理成2行
    title_len = int(len(title) / 15)
    title_num = 0
    while title_num <= title_len:
        if title_num == 0:
            strs = title[:(title_num + 1) * 15] + "\n"
        else:
            strs = strs + title[title_num * 15:(title_num + 1) * 15] + "\n"
        title_num = title_num + 1
    title_result = strs

    # 视频添加文字
    txt_clip1 = (
        TextClip(title_result, font=font_path, fontsize=55, color='white', method='label')
            .set_position(("center", "top"))
            .set_duration(0.1)
            .set_start(0)
    )
    video_path = "./materials/" + title + "/data/cover.mp4"
    video = VideoFileClip(video_path)
    cvc = CompositeVideoClip([video, txt_clip1], size=(1280, 720))
    cvc.write_videofile("./materials/" + title + "/data/title.mp4", fps=60, remove_temp=False)

    print("封面视频添加Title完毕")

# 拼接所有视频
def StitchingAllVideo(path_cover,path_end,title_mp4,title):
    L = []
    video = VideoFileClip(title_mp4).resize((1280, 720))
    L.append(video)
    video = VideoFileClip(path_cover).resize((1280, 720))
    L.append(video)
    video = VideoFileClip("./materials/" + title + "/data/result.mp4").resize((1280, 720)).fadein(2, (1, 1, 1))
    L.append(video)
    video = VideoFileClip(path_end).resize((1280, 720))
    video = video.set_duration(video.duration - 0.5)
    L.append(video)
    final_clip = concatenate_videoclips(L)
    # 生成目标视频文件
    final_clip.to_videofile('materials/' + title + '/data/' + title + '.mp4', fps=60, remove_temp=False)

# 增加水印
def AddLogo(title,logo_path):
    # 增加水印
    video = VideoFileClip('materials/' + title + '/data/' + title + '.mp4')
    logo = (ImageClip(logo_path)
            .set_duration(video.duration)  # 水印持续时间
            .resize(height=100)  # 水印的高度，会等比缩放
            # .margin(right=8, top=8, opacity=1) # 水印边距和透明度
            .set_pos(("right", "top")))  # 水印的位置

    final = CompositeVideoClip([video, logo])
    # mp4文件默认用libx264编码， 比特率单位bps
    final.write_videofile('materials/' + title + '/' + title + '.mp4')

    print("全部合成完毕文件目录：",'materials/' + title + '/')