# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '文件目录说明：' \
              'data：用于存放视频中生成内容的excel表格数据，以及AI抠图的日志文件' \
              'font：用于存放字体文件' \
              'material_base：用于存放视频素材片头、片尾、片中、过场的MP4' \
              'material_everypart：根据不同的内容存放算法生成的无语音part素材和封面' \
              'material_jpg：用于存放视频用使用的水印、封面、不同的内容按照规则生成的图片' \
              'material_mp3：用于存放百度AI生成的MP3文件' \
              'material_result：用于存放最终视频生成的结果文件，如果生成同样的内容需要将源文件删除' \
              'material_video：根据不同的内容存放算法生成的合成语音后part素材和封面、总合成的结果' \
              '备份脚本：该项目Debug的过程' \
              '' \
              '使用说明：' \
              '1.在material_jpg中创建内容的文件夹，名称为对应pic_name的名称' \
              '2.在互联网上采集对应内容的图片，改名pic_name.jpg格式' \
              '3.无脑启动脚本等material_result出结果' \
              '4.代码423行处，根据material_jpg的base的文件夹下fuyong、zhongzhi进行随机切换图片生成不同的内容，素材自行搞定' \
              '5.水印根据material_jpg的base下的logo.png进行更换' \
              '6.封面根据material_jpg的base下的cover.pptx进行操作生成base.jpg进行更换'

import pandas as pd
import librosa
import cv2
import numpy as np
from PIL import Image
from moviepy.editor import *
import subprocess
import os
import glob
from removebg import RemoveBg
from aip import AipSpeech

"""读取制作内容数据，提前在excel表中修改好内容"""
df = pd.read_excel("data/data.xlsx")
row = 2
df = df.loc[row:row, :]
df.reset_index(drop=True, inplace=True)
pic_name = df["name"][0]
print("本次制作内容：", pic_name)

"""加载配置内容"""
# 加载字体配置文件
font_path = './font/kaiti.ttf'
# 文件对应中文名称配置
text_dict = {
    "ddyg": "药品来源",
    "dosage_and_administration": "服用方法",
    "drug_properties": "草本性状",
    "flavor_and_meridian_tropism": "性味归经",
    "functions_of_curing": "用途功效",
    "latin": "拉丁文",
    "medicinal_parts": "药用部分",
    "name": "名称",
    "nmedicinal_partsame": "医用部分",
    "other_name": "别名",
    "pinyin": "拼音",
    "plant": "种植方法",
    "process": "处理方法",
    "production_place": "生长环境",
    "taboos": "使用禁忌",
    "type_": "药品类型",
}


# 文字处理对应方法
def clean_word(word):
    word_len = int(len(word) / 20)
    word_num = 0
    while word_num <= word_len:
        if word_num == 0:
            strs = word[:(word_num + 1) * 20] + "\n"
        else:
            #             strs = word[:(word_num + 1) * 8] + "..."
            strs = strs + word[word_num * 20:(word_num + 1) * 20] + "\n"
        word_num = word_num + 1
    return word_len, strs

def clean_word8(word):
    word_len = int(len(word) / 8)
    word_num = 0
    while word_num <= word_len:
        if word_num == 0:
            strs = word[:(word_num + 1) * 8] + "\n"
        else:
            #             strs = word[:(word_num + 1) * 8] + "..."
            strs = strs + word[word_num * 8:(word_num + 1) * 8] + "\n"
        word_num = word_num + 1
    return word_len, strs

"""制作前删除合成语音的文件，否则无法继续"""
path = "./material_video/" + pic_name
try:
    for infile in glob.glob(os.path.join(path, '*.mp4')):
        os.remove(infile)
    print("素材已删除")
except:
    print("没有可以删除的素材")

"""药材图片进行抠图生成素材"""
# 图片抠图处理
rmbg = RemoveBg("ypWN2SE5p57qKMk6jtaaSXRq", "data/error.log")  # 把你的`API Key`填进去
# 判断如果没有该数据的文件夹就创建
dirs = 'material_jpg/' + pic_name
if not os.path.exists(dirs):
    os.makedirs(dirs)
# 判断视频图片是否存在，若存在则跳过
png_name = "./material_jpg/" + pic_name + "/" + pic_name + ".jpg_no_bg.png"
if not os.path.exists(png_name):
    rmbg.remove_background_from_img_file("./material_jpg/" + pic_name + "/" + pic_name + ".jpg")
else:
    print("该图片的内容抠图已经存在")

"""合成封面图片"""
# 加载背景图片
base_img = Image.open('material_jpg/base/base.jpg')
# 转换图片色到分别表示RGBA的值
target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
# 选择png图片显示的区域
box = (800, 400, 1260, 690)
# 加载PNG图片
region = Image.open('material_jpg/' + pic_name + '/' + pic_name + '.jpg_no_bg.png')
# 确保图片是RGBA格式，大小和box区域一样
region = region.convert("RGBA")
region = region.resize((box[2] - box[0], box[3] - box[1]))
# 将素材图片合成道底板图上
target.paste(region, box)
# 将背景图上假如生成号的素材地板透明背景图
base_img.paste(target, (0, 0), target)  # 第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
# base_img.show()
base_img.save('material_jpg/' + pic_name + '/result.jpg')  # 保存图片

"""读取文字转语音"""
# 加载百度AIP账号
APP_ID = '22577460'
API_KEY = 'Q7aI5ALdYHbHzDGestq4trF8'
SECRET_KEY = 'h850Sj1g3eoLKDEwNAj6yVNyGx5GbXht'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


# 把文字转换成语音 将生成的音频文件保存到material_mp3下
def str_to_mp3(dataframe):
    # 判断如果没有该数据的文件夹就创建
    dirs = 'material_mp3/' + dataframe["name"][0]
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    # 遍历该条df数据每列文字进行语音MP3转换
    for col in dataframe.columns:
        result = client.synthesis(text_dict[col] + dataframe[col][0], 'zh', 1, {'vol': 12, 'spd': 6, 'per': 0})
        if not isinstance(result, dict):
            with open('material_mp3/' + dataframe["name"][0] + "/" + col + '.mp3', 'wb') as f:
                f.write(result)


# 执行函数生成文字对应MP3文件
str_to_mp3(df)


# 获取MP3的文件列表
def file_name(file_dir):
    list_ = [files for files in os.walk(file_dir)][0][2]
    filelist = [i for i in list_ if os.path.splitext(i)[1] == '.mp3']
    return filelist


filelist = file_name("./material_mp3/" + df["name"][0])


# 读取文字转语音的MP3 并计算时长
def get_mp3_duration(audio_path):
    duration = librosa.get_duration(filename=audio_path)
    return duration


time_name_dict = {}
time_num_all = 0  # 总音频的秒数
for i in filelist:
    time_num = get_mp3_duration("material_mp3/" + df["name"][0] + "/" + i)
    time_num_all = time_num_all + time_num
    time_name_dict[i] = time_num
"""
拼接顺序制作
- name	名称（pinyin	拼音）
- type_	药品类型
- ddyg	药品来源
- latin	拉丁文
- other_name	别名

- drug_properties 草本性状（内容较多暂时丢弃）

- medicinal_parts 药用部分
- flavor_and_meridian_tropism 性味归经

- production_place 生长环境
- plant 种植方法

- process 处理方法
- dosage_and_administration 服用方法
- functions_of_curing 用途功效
- taboos 使用禁忌
"""

""" 制作第一部分（单页面显示5个字段内容数据）"""
# 创建该内容的文件夹，用于保存算法合成的每个部分无声音的MP4视频
dirs = 'material_everypart/' + pic_name
if not os.path.exists(dirs):
    os.makedirs(dirs)

# 选取第一部分的字段
word_list = ["name", "type_", "ddyg", "other_name", "latin"]

# 获取该单元格的文字 单元格对应时长
name = df['name'][0]
name_len, name_result = clean_word(name)
name_time = time_name_dict["name.mp3"]
type_ = df['type_'][0]
type_len, type_result = clean_word(type_)
type_time = time_name_dict["type_.mp3"]
ddyg = df['ddyg'][0]
ddyg_len, ddyg_result = 1, df['ddyg'][0]
ddyg_time = time_name_dict["ddyg.mp3"]
latin = df['latin'][0]
latin_len, latin_result = 1, df['latin'][0]
latin_time = time_name_dict["latin.mp3"]
other_name = df['other_name'][0]
other_name_len, other_name_result = clean_word8(other_name)
other_name_time = time_name_dict["other_name.mp3"]

# 计算文字的时长
t_s1 = 0
t_d1 = name_time + type_time + ddyg_time + latin_time + other_name_time
t_s2 = name_time
t_d2 = type_time + ddyg_time + latin_time + other_name_time
t_s3 = name_time + type_time
t_d3 = ddyg_time + latin_time + other_name_time
t_s4 = name_time + type_time + ddyg_time
t_d4 = latin_time + other_name_time
t_s5 = name_time + type_time + ddyg_time + latin_time
t_d5 = other_name_time

# 添加该模块材料图片（药材图片）
Image = (
    ImageClip("./material_jpg/" + pic_name + "/" + pic_name + ".jpg_no_bg.png")
        .set_duration(t_d1)  # 水印持续时间
        .resize(height=300)  # 水印的高度，会等比缩放
        .set_pos((600, 90))  # 水印的位置
)

# 加入水印
logo = (
    ImageClip("./material_jpg/base/logo.png")
        .set_duration(t_d1)  # 水印持续时间
        .resize(height=50)  # 水印的高度，会等比缩放
        .set_pos(("right", "top"))  # 水印的位置
)

## 将标题和文字融入到视频中
txt_clip1 = (
    TextClip("中药名称", font=font_path, fontsize=50, color='black', method='label', align='West')
        .set_position((230, 80))
        .set_duration(t_d1)
        .set_start(t_s1)
)
txt_clip2 = (
    TextClip(name_result, font=font_path, fontsize=40, color='black', method='label', align='West')
        .set_position((260, 140))
        .set_duration(t_d1)
        .set_start(t_s1)
)

## 将标题和文字融入到视频中
txt_clip3 = (
    TextClip("药品类型", font=font_path, fontsize=50, color='black', method='label', align='West')
        .set_position((230, 190))
        .set_duration(t_d2)
        .set_start(t_s2)
)
txt_clip4 = (
    TextClip(type_result, font=font_path, fontsize=40, color='black', method='label', align='West')
        .set_position((260, 260))
        .set_duration(t_d2)
        .set_start(t_s2)
)

## 将标题和文字融入到视频中
txt_clip5 = (
    TextClip("药品来源", font=font_path, fontsize=50, color='black', method='label', align='West')
        .set_position((230, 310))
        .set_duration(t_d3)
        .set_start(t_s3)
)
txt_clip6 = (
    TextClip(ddyg_result, font=font_path, fontsize=40, color='black', method='label', align='West')
        .set_position((260, 370))
        .set_duration(t_d3)
        .set_start(t_s3)
)

## 将标题和文字融入到视频中
txt_clip7 = (
    TextClip("别名", font=font_path, fontsize=50, color='black', method='label', align='West')
        .set_position((230, 430))
        .set_duration(t_d4)
        .set_start(t_s4)
)
txt_clip8 = (
    TextClip(other_name_result, font=font_path, fontsize=40, color='black', method='label', align='West')
        .set_position((260, 480))
        .set_duration(t_d4)
        .set_start(t_s4)
)

## 将标题和文字融入到视频中
txt_clip9 = (
    TextClip("拉丁文", font=font_path, fontsize=50, color='black', method='label', align='West')
        .set_position((630, 430))
        .set_duration(t_d5)
        .set_start(t_s5)
)
txt_clip10 = (
    TextClip(latin_result, font=font_path, fontsize=40, color='black', method='label', align='West')
        .set_position((660, 480))
        .set_duration(t_d5)
        .set_start(t_s5)
)

# 与背景进行合成
L = []
path = "material_base/1s.mp4"
video = VideoFileClip(path)
for i in range(int(t_d1) + 1):
    L.append(video)
final_clip = concatenate_videoclips(L).set_duration(t_d1).resize((1280, 720))
cvc = CompositeVideoClip(
    [final_clip, Image, logo, txt_clip1, txt_clip2, txt_clip3, txt_clip4, txt_clip5, txt_clip6, txt_clip7, txt_clip8,
     txt_clip9, txt_clip10], size=(1280, 720))
cvc.write_videofile("./material_everypart/" + pic_name + "/" + "1st.mp4", fps=60, remove_temp=False)

# 合并音频、写入MP4
f_write = open('material_mp3/' + pic_name + "/" + '1st.mp3', 'wb')
for i in word_list:
    f_read = open('material_mp3/' + pic_name + "/" + i + '.mp3', 'rb')
    f_write.write(f_read.read())
    f_read.close()
f_write.flush()
f_write.close()

# 如果没有文件夹自动创建
dirs = 'material_video/' + pic_name
if not os.path.exists(dirs):
    os.makedirs(dirs)

# 将对应的音频和视频进行合成
outfile_name = 'material_video/' + pic_name + '/' + '1st.mp4'
subprocess.call('ffmpeg -i ' + 'material_everypart/' + pic_name + '/' + '1st.mp4'
                + ' -i ' + 'material_mp3/' + pic_name + '/' + '1st.mp3' + ' -strict -2 -f mp4 '
                + outfile_name, shell=True)

"""制作非第一部分（根据字段内容生成）"""
every_part = {
    "2nd": {
        "col_list": ["medicinal_parts", "flavor_and_meridian_tropism"],
        "jpg_path": "./"
    },
    "3rd": {
        "col_list": ["production_place", "plant"],
        "jpg_path": "zhongzhi"
    },
    "4th": {
        "col_list": ["process", "dosage_and_administration", "functions_of_curing", "taboos"],
        "jpg_path": "fuyong"
    }
}
# 遍历字段进行生成
for part in every_part.keys():
    word_list = every_part[part]['col_list']
    jpg_path = every_part[part]['jpg_path']
    # 起始时间
    start_time = 0
    result_list = []
    for num in range(len(word_list)):
        # 获取该字段字符串
        words = df[word_list[num]][0]
        # 获得文字长度
        words_len, words_result = clean_word(words)

        # 持续时间
        duration_time = time_name_dict[word_list[num] + ".mp3"]

        # 构建切换的字幕方法
        str_list = words_result.split("\n")[:-1]
        allstrs = []  # 分组切分后的汉字放在这里
        every_list = []
        for i in range(len(str_list)):
            every_list.append((str_list[i] + "\n"))
            if i == 0:
                allstrs.append(every_list)
            if i % 3 == 0 and i != 0:
                every_list = []
                allstrs.append(every_list)
        # 分多少页、和时长，由于切分音频是要 1|1|1|1 这么切分，所以(len(allstrs)-1)
        try:
            page_num, every_page_time = len(allstrs), duration_time / (len(allstrs) - 1)
        except:
            page_num, every_page_time = 1, duration_time
        #     print("起始时间：{}".format(start_time),"持续时间：{}".format(duration_time),"下段开始时间：{}".format(start_time + duration_time))
        #     print("字段内容段落数：{}".format(page_num),"每段持续时间：{}".format(every_page_time))

        # 标题位置
        title_clip = (
            TextClip(text_dict[word_list[num]], font=font_path, fontsize=50, color='black', method='label',
                     align='West')
                .set_position((210, 320))
                .set_duration(duration_time)
                .set_start(start_time)
        )
        logo = (
            ImageClip("./material_jpg/base/logo.png")
                .set_duration(duration_time)  # 水印持续时间
                .resize(height=50)  # 水印的高度，会等比缩放
                .set_pos(("right", "top"))  # 水印的位置
        )

        # 每个部分
        txt_list = []
        allstrs = [i for i in allstrs if i != []]  # 去除无用的空list避免报错
        allstrs = [i for i in allstrs if i != ['\n']]  # 去除无用的空list避免报错
        #     print(allstrs)
        start_every = start_time

        for i in range(len(allstrs)):
            txt_every = (
                TextClip("".join(allstrs[i]), font=font_path, fontsize=40, color='black', method='label', align='West')
                    .set_position((230, 390))
                    .set_duration(every_page_time)
                    .set_start(start_every + every_page_time * i)
            )
            #         print(start_every + every_page_time * i)
            txt_list.append(txt_every)
        #         print("".join(allstrs[i]),start_time + every_page_time)
        start_time = start_time + duration_time

        result_list.append(title_clip)
        result_list = result_list + txt_list

    # 该栏目使用图片位置
    if part == "2nd":
        path_jpg = "./material_jpg/" + pic_name + "/" + pic_name + ".jpg_no_bg.png"
    else:
        path_jpg = "./material_jpg/base/" + jpg_path + "/" + str(np.random.randint(1, 2, 1)[0]) + ".jpg"
    Image = (
        ImageClip(path_jpg)
            .set_duration(start_time)  # 水印持续时间
            .resize(height=250)  # 水印的高度，会等比缩放
            .set_pos(("center", 90))  # 水印的位置
    )

    L = []
    path = "material_base/1s.mp4"
    video = VideoFileClip(path)
    for i in range(int(start_time) + 1):
        L.append(video)
    final_clip = concatenate_videoclips(L).set_duration(start_time).resize((1280, 720))
    cvc = CompositeVideoClip([final_clip, Image, logo] + result_list, size=(1280, 720))
    cvc.write_videofile("./material_everypart/" + pic_name + "/" + part + ".mp4", fps=60, remove_temp=False,
                        verbose=True)

    """合并音频、写入MP4"""
    f_write = open('material_mp3/' + pic_name + "/" + part + '.mp3', 'wb')
    for i in word_list:
        f_read = open('material_mp3/' + pic_name + "/" + i + '.mp3', 'rb')
        f_write.write(f_read.read())
        f_read.close()
    f_write.flush()
    f_write.close()

    # 如果没有文件夹自动创建
    dirs = 'material_video/' + pic_name
    if not os.path.exists(dirs):
        os.makedirs(dirs)

    # 将对应的音频和视频进行合成
    outfile_name = 'material_video/' + pic_name + '/' + part + '.mp4'
    subprocess.call('ffmpeg -i ' + 'material_everypart/' + pic_name + '/' + part + '.mp4'
                    + ' -i ' + 'material_mp3/' + pic_name + '/' + part + '.mp3' + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)

"""制作封面"""
# 将封面生成1秒的视频
from PIL import Image

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
size = (1280, 720)
vw = cv2.VideoWriter("./material_everypart/" + pic_name + "/" + "cover.mp4", fourcc=fourcc, fps=10, frameSize=size)
f_read = cv2.imdecode(np.fromfile("./material_jpg/" + pic_name + "/result.jpg", dtype=np.uint8), cv2.IMREAD_COLOR)
f_img = Image.fromarray(f_read)
f_rs = f_img.resize([1280, 720], resample=Image.NONE)
f_out = np.array(f_rs)
for i in range(10):
    vw.write(f_out)
vw.release()

Txt = (
    TextClip(pic_name, font='./font/fengmingshoushu.ttf', fontsize=120, color='black', method='label')
        .set_position(("center", 450))
        .set_duration(1)  # 水印持续时间
)

path = "material_everypart/" + pic_name + "/" + "cover.mp4"
video = VideoFileClip(path).resize((1280, 720))

cvc = CompositeVideoClip([video, Txt], size=(1280, 720))
cvc.write_videofile("./material_video/" + pic_name + "/" + "cover.mp4", fps=60, remove_temp=False, verbose=False)

"""按照顺序将视频进行拼接"""
L = []
path_material = "material_video/" + pic_name + "/"
path_chanege = "material_base/change.mp4"
path_cover = "./material_video/" + pic_name + "/" + "cover.mp4"
path_end = "material_base/end.mp4"

video = VideoFileClip(path_cover).resize((1280, 720))
L.append(video)
video = VideoFileClip(path_material + "1st.mp4").resize((1280, 720)).fadein(2, (1, 1, 1))
L.append(video)
video = VideoFileClip(path_chanege).resize((1280, 720))
L.append(video)
video = VideoFileClip(path_material + "2nd.mp4").resize((1280, 720))
video = video.set_duration(video.duration - 0.5)
L.append(video)
video = VideoFileClip(path_chanege).resize((1280, 720))
L.append(video)
video = VideoFileClip(path_material + "3rd.mp4").resize((1280, 720))
video = video.set_duration(video.duration - 0.5)
L.append(video)
video = VideoFileClip(path_chanege).resize((1280, 720))
L.append(video)
video = VideoFileClip(path_material + "4th.mp4").resize((1280, 720)).fadeout(2, (1, 1, 1))
video = video.set_duration(video.duration - 0.5)
L.append(video)
video = VideoFileClip(path_end).resize((1280, 720))
L.append(video)

final_clip = concatenate_videoclips(L)

# 生成目标视频文件
final_clip.to_videofile(path_material + "result.mp4", fps=60, remove_temp=False)

"""将配乐和视频进行合成"""
inmp4 = 'material_video/' + pic_name + '/' + 'result.mp4'
inmp3 = 'material_mp3/music.mp3'
outmp4 = 'material_result/' + pic_name + '.mp4'

cmd = 'ffmpeg -y -i ' + inmp4 + ' -i ' + inmp3 + ' -filter_complex \
"[0:a]volume=10dB[a0]; \
[1:a]volume=-10dB[a1]; \
[a0][a1]amix=inputs=2[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -shortest ' + outmp4

p = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 删除目录下生成的MP3文件
path = "./"
for infile in glob.glob(os.path.join(path, '*.mp3')):
    os.remove(infile)
