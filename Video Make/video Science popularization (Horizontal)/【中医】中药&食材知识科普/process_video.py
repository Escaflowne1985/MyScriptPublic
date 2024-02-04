# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '视频处理程序'

from moviepy.editor import *
import subprocess
from pyecharts import options as opts
from pyecharts.charts import Map
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot
import cv2
import numpy as np
from configs import *  # 工程配置数据
from process_text import *  # 处理工程需要的字符数据

# 加载配置文件
# 提取使用的字体路径 font_path
# 中英文对应的数据列名字典 column_en2cn_dict\column_cn2en_dict
font_path, column_en2cn_dict, column_cn2en_dict = config()


# 制作封面视频
def MakeCoverMp4(pic_name):
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

    name = pic_name

    Txt = (
        TextClip(name, font='./font/kaiti.ttf', fontsize=80, color='black', method='label')
            .set_position(("center", 420))
            .set_duration(1)  # 水印持续时间
    )

    path = "material_everypart/" + pic_name + "/" + "cover.mp4"
    video = VideoFileClip(path).resize((1280, 720))

    cvc = CompositeVideoClip([video, Txt], size=(1280, 720))
    cvc.write_videofile("./material_video/" + pic_name + "/" + "cover.mp4", fps=60, remove_temp=False, verbose=False)


# 第一部分
def FirstPart(pic_name, df, time_name_dict, column_en2cn_dict):
    # 选取第一部分的字段
    word_list = ["CnName", "LaiYuan", "YCBM", "YYLB"]
    data_list = []  # 选择有用的数据进行处理
    f_write = open('material_mp3/' + pic_name + "/" + '1st.mp3', 'wb')  # 处理有用数据的MP3

    for col in df[word_list].columns:
        if df[col][0] != "暂无数据":
            # 文本数据部分
            col_text = df[col]
            data_text = df[col][0]
            col_duration_time = time_name_dict[col + ".mp3"]
            one_dict = {col: {"text": data_text, "time": col_duration_time}}
            data_list.append(one_dict)

            # 语音数据部分
            f_read = open('material_mp3/' + pic_name + "/" + col + '.mp3', 'rb')
            f_write.write(f_read.read())
            f_read.close()
    f_write.flush()
    f_write.close()

    start_time = 0
    all_duration_time = sum([list(data_list[i].values())[0]["time"] for i in range(len(data_list))])

    # 文字的坐标参数
    title_y1 = 80
    title_y2 = 140
    title_y = 110

    result_list = []

    for i in range(len(data_list)):
        title = column_en2cn_dict[list(data_list[i].keys())[0]]
        content = list(data_list[i].values())[0]["text"]
        duration_time = list(data_list[i].values())[0]["time"]

        # 判断内容过去分行
        if len(content) > 15:
            words_len, words_result = clean_word(content)
            content = "\n".join(words_result.split("\n")[:-1])
        else:
            words_len = 1

        ## 将标题和文字融入到视频中
        txt_title = (
            TextClip(title, font=font_path, fontsize=50, color='black', method='label', align='West')
                .set_position((230, title_y1))
                .set_duration(all_duration_time - start_time)
                .set_start(start_time)
        )
        txt_content = (
            TextClip(content, font=font_path, fontsize=40, color='black', method='label', align='West')
                .set_position((260, title_y2))
                .set_duration(all_duration_time - start_time)
                .set_start(start_time)
        )

        result_list.append(txt_title)
        result_list.append(txt_content)

        start_time = start_time + duration_time
        title_y1 = title_y1 + title_y + (words_len - 1) * 50
        title_y2 = title_y2 + title_y + (words_len - 1) * 50

    # 添加该模块材料图片（药材图片）
    Image = (
        ImageClip("./material_jpg/" + pic_name + "/" + pic_name + ".jpg_no_bg.png")
            .set_duration(start_time)  # 水印持续时间
            .resize(height=300)  # 水印的高度，会等比缩放
            .set_pos((600, 90))  # 水印的位置
    )

    # 加入水印
    logo = (
        ImageClip("./material_jpg/base/logo.png")
            .set_duration(start_time)  # 水印持续时间
            .resize(height=50)  # 水印的高度，会等比缩放
            .set_pos(("right", "top"))  # 水印的位置
    )

    # 与背景进行合成
    L = []
    path = "material_base/1s.mp4"
    video = VideoFileClip(path)
    for i in range(int(all_duration_time) + 1):
        L.append(video)
    final_clip = concatenate_videoclips(L).set_duration(all_duration_time).resize((1280, 720))
    cvc = CompositeVideoClip([final_clip, Image, logo] + result_list, size=(1280, 720))
    cvc.write_videofile("./material_everypart/" + pic_name + "/" + "1st.mp4", fps=60, remove_temp=False)

    # 将对应的音频和视频进行合成
    outfile_name = 'material_video/' + pic_name + '/' + '1st.mp4'
    subprocess.call('ffmpeg -i ' + 'material_everypart/' + pic_name + '/' + '1st.mp4'
                    + ' -i ' + 'material_mp3/' + pic_name + '/' + '1st.mp3' + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)
    print("第一部分内容处理完毕，如果发现黑屏请调整改部分的clean_word")


# 第二部分
def SecondPart(pic_name, df, time_name_dict, column_en2cn_dict):
    # 选取第二部分的字段
    word_list = ["PinYin", "LaDing", "EnName", "LDWM"]

    data_list = []  # 选择有用的数据进行处理
    f_write = open('material_mp3/' + pic_name + "/" + '2nd.mp3', 'wb')  # 处理有用数据的MP3

    for col in df[word_list].columns:
        if df[col][0] != "暂无数据":
            # 文本数据部分
            col_text = df[col]
            data_text = df[col][0]
            col_duration_time = time_name_dict[col + ".mp3"]
            one_dict = {col: {"text": data_text, "time": col_duration_time}}
            data_list.append(one_dict)

            # 语音数据部分
            f_read = open('material_mp3/' + pic_name + "/" + col + '.mp3', 'rb')
            f_write.write(f_read.read())
            f_read.close()
    f_write.flush()
    f_write.close()

    start_time = 0
    all_duration_time = sum([list(data_list[i].values())[0]["time"] for i in range(len(data_list))])

    # 文字的坐标参数
    title_y1 = 80
    title_y2 = 140
    title_y = 110

    result_list = []

    for i in range(len(data_list)):
        title = column_en2cn_dict[list(data_list[i].keys())[0]]
        content = list(data_list[i].values())[0]["text"]
        duration_time = list(data_list[i].values())[0]["time"]

        ## 将标题和文字融入到视频中
        txt_title = (
            TextClip(title, font=font_path, fontsize=50, color='black', method='label', align='West')
                .set_position((230, title_y1))
                .set_duration(all_duration_time - start_time)
                .set_start(start_time)
        )
        txt_content = (
            TextClip(content, font=font_path, fontsize=40, color='black', method='label', align='West')
                .set_position((260, title_y2))
                .set_duration(all_duration_time - start_time)
                .set_start(start_time)
        )

        result_list.append(txt_title)
        result_list.append(txt_content)

        start_time = start_time + duration_time
        title_y1 = title_y1 + title_y
        title_y2 = title_y2 + title_y

    # 添加该模块材料图片（药材图片）
    Image = (
        ImageClip("./material_jpg/" + pic_name + "/" + pic_name + ".jpg_no_bg.png")
            .set_duration(start_time)  # 水印持续时间
            .resize(height=300)  # 水印的高度，会等比缩放
            .set_pos((600, 90))  # 水印的位置
    )

    # 加入水印
    logo = (
        ImageClip("./material_jpg/base/logo.png")
            .set_duration(start_time)  # 水印持续时间
            .resize(height=50)  # 水印的高度，会等比缩放
            .set_pos(("right", "top"))  # 水印的位置
    )

    # 与背景进行合成
    L = []
    path = "material_base/1s.mp4"
    video = VideoFileClip(path)
    for i in range(int(all_duration_time) + 1):
        L.append(video)
    final_clip = concatenate_videoclips(L).set_duration(all_duration_time).resize((1280, 720))
    cvc = CompositeVideoClip([final_clip, Image, logo] + result_list, size=(1280, 720))
    cvc.write_videofile("./material_everypart/" + pic_name + "/" + "2nd.mp4", fps=60, remove_temp=False)

    # 将对应的音频和视频进行合成
    outfile_name = 'material_video/' + pic_name + '/' + '2nd.mp4'
    subprocess.call('ffmpeg -i ' + 'material_everypart/' + pic_name + '/' + '2nd.mp4'
                    + ' -i ' + 'material_mp3/' + pic_name + '/' + '2nd.mp3' + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)
    print("第二部分内容处理完毕，如果发现黑屏请调整改部分的clean_word")


# 第三部分
def ThirdPart(pic_name, df, time_name_dict, column_en2cn_dict):
    # 选取第三部分的字段
    word_list = ["YCJY", "YWGJ", "GNZZ", "ZYSX", "YLZY"]
    data_list = []  # 选择有用的数据进行处理
    f_write = open('material_mp3/' + pic_name + "/" + '3rd.mp3', 'wb')  # 处理有用数据的MP3

    for col in df[word_list].columns:
        if df[col][0] != "暂无数据":
            # 文本数据部分
            col_text = df[col]
            data_text = df[col][0]
            col_duration_time = time_name_dict[col + ".mp3"]
            one_dict = {col: {"text": data_text, "time": col_duration_time}}
            data_list.append(one_dict)

            # 语音数据部分
            f_read = open('material_mp3/' + pic_name + "/" + col + '.mp3', 'rb')
            f_write.write(f_read.read())
            f_read.close()
    f_write.flush()
    f_write.close()

    start_time = 0
    result_list = []
    all_duration_time = sum([list(data_list[i].values())[0]["time"] for i in range(len(data_list))])

    for i in range(len(data_list)):
        title = column_en2cn_dict[list(data_list[i].keys())[0]]
        content = list(data_list[i].values())[0]["text"]
        duration_time = list(data_list[i].values())[0]["time"]

        # 获得文字长度
        words_len, words_result = clean_word(content)
        # 构建切换的字幕方法
        str_list = words_result.split("\n")[:-1]
        allstrs = []  # 分组切分后的汉字放在这里
        every_list = []
        for i in range(len(str_list)):
            every_list.append((str_list[i] + "\n"))
            if i == 0:
                allstrs.append(every_list)
            if i % 2 == 0 and i != 0:
                every_list = []
                allstrs.append(every_list)
            # 分多少页、和时长，由于切分音频是要 1|1|1|1 这么切分
        allstrs = [i for i in allstrs if i != []]  # 去除无用的空list避免报错
        allstrs = [i for i in allstrs if i != ['\n']]  # 去除无用的空list避免报错
        page_num, every_page_time = len(allstrs), duration_time / len(allstrs)
        #     print(len(allstrs),page_num , every_page_time)
        #     print("起始时间：{}".format(start_time),"持续时间：{}".format(duration_time),"下段开始时间：{}".format(start_time + duration_time))
        #     print("字段内容段落数：{}".format(page_num),"每段持续时间：{}".format(every_page_time))

        # 标题位置
        txt_title = (
            TextClip(title, font=font_path, fontsize=50, color='black', method='label', align='West')
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
        Image = (
            ImageClip("./material_jpg/" + pic_name + "/" + pic_name + ".jpg_no_bg.png")
                .set_duration(all_duration_time)  # 水印持续时间
                .resize(height=250)  # 水印的高度，会等比缩放
                .set_pos(("center", 90))  # 水印的位置
        )

        # 每个部分
        txt_list = []
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

        result_list.append(txt_title)
        result_list = result_list + txt_list

    L = []
    path = "material_base/1s.mp4"
    video = VideoFileClip(path)
    for i in range(int(start_time) + 1):
        L.append(video)
    final_clip = concatenate_videoclips(L).set_duration(start_time).resize((1280, 720))
    cvc = CompositeVideoClip([final_clip, Image, logo] + result_list, size=(1280, 720))
    cvc.write_videofile("./material_everypart/" + pic_name + "/" + "3rd.mp4", fps=60, remove_temp=False, verbose=True)

    # 将对应的音频和视频进行合成
    outfile_name = 'material_video/' + pic_name + '/' + '3rd.mp4'
    subprocess.call('ffmpeg -i ' + 'material_everypart/' + pic_name + '/' + '3rd.mp4'
                    + ' -i ' + 'material_mp3/' + pic_name + '/' + '3rd.mp3' + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)
    print("第三部分内容处理完毕，如果发现黑屏请调整改部分的clean_word")


# 第四部分
def FourthPart(pic_name, df, time_name_dict, column_en2cn_dict):
    # 选取第四部分的字段
    word_list = ["QYFB", "SS"]

    data_list = []  # 选择有用的数据进行处理
    f_write = open('material_mp3/' + pic_name + "/" + '4th.mp3', 'wb')  # 处理有用数据的MP3

    for col in [df[word_list].columns[0]]:
        if df[col][0] != "暂无数据":
            # 文本数据部分
            col_text = df[col]
            data_text = df[col][0]
            col_duration_time = time_name_dict[col + ".mp3"]
            one_dict = {col: {"text": data_text, "time": col_duration_time, "area": eval(df["SS"][0])}}
            data_list.append(one_dict)

            # 语音数据部分
            f_read = open('material_mp3/' + pic_name + "/" + col + '.mp3', 'rb')
            f_write.write(f_read.read())
            f_read.close()
    f_write.flush()
    f_write.close()

    start_time = 0
    result_list = []
    all_duration_time = sum([list(data_list[i].values())[0]["time"] for i in range(len(data_list))])

    for i in range(len(data_list)):
        title = column_en2cn_dict[list(data_list[i].keys())[0]]
        content = list(data_list[i].values())[0]["text"]
        duration_time = list(data_list[i].values())[0]["time"]
        area = list(data_list[i].values())[0]["area"]

        # 获得文字长度
        words_len, words_result = clean_word(content)
        # 构建切换的字幕方法
        str_list = words_result.split("\n")[:-1]
        allstrs = []  # 分组切分后的汉字放在这里
        every_list = []
        for i in range(len(str_list)):
            every_list.append((str_list[i] + "\n"))
            if i == 0:
                allstrs.append(every_list)
            if i % 2 == 0 and i != 0:
                every_list = []
                allstrs.append(every_list)
            # 分多少页、和时长，由于切分音频是要 1|1|1|1 这么切分
        allstrs = [i for i in allstrs if i != []]  # 去除无用的空list避免报错
        allstrs = [i for i in allstrs if i != ['\n']]  # 去除无用的空list避免报错
        page_num, every_page_time = len(allstrs), duration_time / len(allstrs)
        #     print(len(allstrs),page_num , every_page_time)
        #     print("起始时间：{}".format(start_time),"持续时间：{}".format(duration_time),"下段开始时间：{}".format(start_time + duration_time))
        #     print("字段内容段落数：{}".format(page_num),"每段持续时间：{}".format(every_page_time))

        # 标题位置
        txt_title = (
            TextClip(title, font=font_path, fontsize=50, color='black', method='label', align='West')
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
        # 根据地域信息生成png图
        # 制作省市显示图标数据bar
        n = 1
        list_data = []
        while n <= len(df["SS"][0]):
            list_data.append(1)
            n = n + 1
        name = pic_name + "的生长区域分布"

        # 制作背景图fuction
        def every_map():
            c = (
                Map()
                    .add(name, [list(z) for z in zip(area, list_data)], "china")
                    .set_global_opts(
                    visualmap_opts=opts.VisualMapOpts(max_=1),
                )
            )
            return c

        make_snapshot(snapshot, every_map().render(), "./material_jpg/" + pic_name + "/area.png")

        # 将图片进行裁剪
        from PIL import Image

        img = Image.open("./material_jpg/" + pic_name + "/area.png")
        img_size = img.size
        h = img_size[1]  # 图片高度
        w = img_size[0]  # 图片宽度
        x = 0.2 * w
        y = 0
        w = 0.8 * w
        h = h
        # 开始截取
        region = img.crop((x, y, x + w, y + h))
        region.save("./material_jpg/" + pic_name + "/area_cut.png")

        Image = (
            ImageClip("./material_jpg/" + pic_name + "/area_cut.png")
                .set_duration(all_duration_time)  # 水印持续时间
                .resize(height=500)  # 水印的高度，会等比缩放
                .set_pos((600, 90))  # 水印的位置
        )

        # 每个部分
        txt_list = []
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

        result_list.append(txt_title)
        result_list = result_list + txt_list

    L = []
    path = "material_base/1s.mp4"
    video = VideoFileClip(path)
    for i in range(int(start_time) + 1):
        L.append(video)
    final_clip = concatenate_videoclips(L).set_duration(start_time).resize((1280, 720))
    cvc = CompositeVideoClip([final_clip, Image, logo] + result_list, size=(1280, 720))
    cvc.write_videofile("./material_everypart/" + pic_name + "/" + "4th.mp4", fps=60, remove_temp=False, verbose=True)

    # 将对应的音频和视频进行合成
    outfile_name = 'material_video/' + pic_name + '/' + '4th.mp4'
    subprocess.call('ffmpeg -i ' + 'material_everypart/' + pic_name + '/' + '4th.mp4'
                    + ' -i ' + 'material_mp3/' + pic_name + '/' + '4th.mp3' + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)
    print("第四部分内容处理完毕，如果发现黑屏请调整改部分的clean_word")


# 第五部分
def FifthPart(pic_name, df, time_name_dict, column_en2cn_dict):
    # 选取第五部分的字段
    word_list = ["MJLS", "HXCF", "XDLCYJ", "XDHYJ"]
    data_list = []  # 选择有用的数据进行处理
    f_write = open('material_mp3/' + pic_name + "/" + '5th.mp3', 'wb')  # 处理有用数据的MP3

    for col in df[word_list].columns:
        if df[col][0] != "暂无数据":
            # 文本数据部分
            col_text = df[col]
            data_text = df[col][0]
            col_duration_time = time_name_dict[col + ".mp3"]
            one_dict = {col: {"text": data_text, "time": col_duration_time}}
            data_list.append(one_dict)

            # 语音数据部分
            f_read = open('material_mp3/' + pic_name + "/" + col + '.mp3', 'rb')
            f_write.write(f_read.read())
            f_read.close()
    f_write.flush()
    f_write.close()

    start_time = 0
    result_list = []
    all_duration_time = sum([list(data_list[i].values())[0]["time"] for i in range(len(data_list))])

    for i in range(len(data_list)):
        title = column_en2cn_dict[list(data_list[i].keys())[0]]
        content = list(data_list[i].values())[0]["text"]
        duration_time = list(data_list[i].values())[0]["time"]

        # 获得文字长度
        words_len, words_result = clean_word(content)
        # 构建切换的字幕方法
        str_list = words_result.split("\n")[:-1]
        allstrs = []  # 分组切分后的汉字放在这里
        every_list = []
        for i in range(len(str_list)):
            every_list.append((str_list[i] + "\n"))
            if i == 0:
                allstrs.append(every_list)
            if i % 2 == 0 and i != 0:
                every_list = []
                allstrs.append(every_list)
            # 分多少页、和时长，由于切分音频是要 1|1|1|1 这么切分
        allstrs = [i for i in allstrs if i != []]  # 去除无用的空list避免报错
        allstrs = [i for i in allstrs if i != ['\n']]  # 去除无用的空list避免报错
        page_num, every_page_time = len(allstrs), duration_time / len(allstrs)
        #     print(len(allstrs),page_num , every_page_time)
        #     print("起始时间：{}".format(start_time),"持续时间：{}".format(duration_time),"下段开始时间：{}".format(start_time + duration_time))
        #     print("字段内容段落数：{}".format(page_num),"每段持续时间：{}".format(every_page_time))

        # 标题位置
        txt_title = (
            TextClip(title, font=font_path, fontsize=50, color='black', method='label', align='West')
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
        Image = (
            ImageClip("./material_jpg/base/yanjiu.jpg")
                .set_duration(all_duration_time)  # 水印持续时间
                .resize(height=250)  # 水印的高度，会等比缩放
                .set_pos(("center", 90))  # 水印的位置
        )

        # 每个部分
        txt_list = []
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

        result_list.append(txt_title)
        result_list = result_list + txt_list

    L = []
    path = "material_base/1s.mp4"
    video = VideoFileClip(path)
    for i in range(int(start_time) + 1):
        L.append(video)
    final_clip = concatenate_videoclips(L).set_duration(start_time).resize((1280, 720))
    cvc = CompositeVideoClip([final_clip, Image, logo] + result_list, size=(1280, 720))
    cvc.write_videofile("./material_everypart/" + pic_name + "/" + "5th.mp4", fps=60, remove_temp=False, verbose=True)

    # 将对应的音频和视频进行合成
    outfile_name = 'material_video/' + pic_name + '/' + '5th.mp4'
    subprocess.call('ffmpeg -i ' + 'material_everypart/' + pic_name + '/' + '5th.mp4'
                    + ' -i ' + 'material_mp3/' + pic_name + '/' + '5th.mp3' + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)
    print("第五部分内容处理完毕，如果发现黑屏请调整改部分的clean_word")


# 第六部分
def SixthPart(pic_name, df, time_name_dict, column_en2cn_dict):
    # 选取第五部分的字段
    word_list = ["FF"]
    data_list = []  # 选择有用的数据进行处理
    f_write = open('material_mp3/' + pic_name + "/" + '6th.mp3', 'wb')  # 处理有用数据的MP3

    for col in df[word_list].columns:
        if df[col][0] != "暂无数据":
            # 文本数据部分
            col_text = df[col]
            data_text = df[col][0]
            col_duration_time = time_name_dict[col + ".mp3"]
            one_dict = {col: {"text": data_text, "time": col_duration_time}}
            data_list.append(one_dict)

            # 语音数据部分
            f_read = open('material_mp3/' + pic_name + "/" + col + '.mp3', 'rb')
            f_write.write(f_read.read())
            f_read.close()
    f_write.flush()
    f_write.close()

    start_time = 0
    result_list = []
    all_duration_time = sum([list(data_list[i].values())[0]["time"] for i in range(len(data_list))])

    for i in range(len(data_list)):
        title = column_en2cn_dict[list(data_list[i].keys())[0]]
        content = list(data_list[i].values())[0]["text"]
        duration_time = list(data_list[i].values())[0]["time"]

        # 获得文字长度
        words_len, words_result = clean_word(content)
        # 构建切换的字幕方法
        str_list = words_result.split("\n")[:-1]
        allstrs = []  # 分组切分后的汉字放在这里
        every_list = []
        for i in range(len(str_list)):
            every_list.append((str_list[i] + "\n"))
            if i == 0:
                allstrs.append(every_list)
            if i % 2 == 0 and i != 0:
                every_list = []
                allstrs.append(every_list)
            # 分多少页、和时长，由于切分音频是要 1|1|1|1 这么切分
        allstrs = [i for i in allstrs if i != []]  # 去除无用的空list避免报错
        allstrs = [i for i in allstrs if i != ['\n']]  # 去除无用的空list避免报错
        page_num, every_page_time = len(allstrs), duration_time / len(allstrs)
        #     print(len(allstrs),page_num , every_page_time)
        #     print("起始时间：{}".format(start_time),"持续时间：{}".format(duration_time),"下段开始时间：{}".format(start_time + duration_time))
        #     print("字段内容段落数：{}".format(page_num),"每段持续时间：{}".format(every_page_time))

        # 标题位置
        txt_title = (
            TextClip(title, font=font_path, fontsize=50, color='black', method='label', align='West')
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
        Image = (
            ImageClip("./material_jpg/base/fufang.jpg")
                .set_duration(all_duration_time)  # 水印持续时间
                .resize(height=250)  # 水印的高度，会等比缩放
                .set_pos(("center", 90))  # 水印的位置
        )

        # 每个部分
        txt_list = []
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

        result_list.append(txt_title)
        result_list = result_list + txt_list

    L = []
    path = "material_base/1s.mp4"
    video = VideoFileClip(path)
    for i in range(int(start_time) + 1):
        L.append(video)
    final_clip = concatenate_videoclips(L).set_duration(start_time).resize((1280, 720))
    cvc = CompositeVideoClip([final_clip, Image, logo] + result_list, size=(1280, 720))
    cvc.write_videofile("./material_everypart/" + pic_name + "/" + "6th.mp4", fps=60, remove_temp=False, verbose=True)

    # 将对应的音频和视频进行合成
    outfile_name = 'material_video/' + pic_name + '/' + '6th.mp4'
    subprocess.call('ffmpeg -i ' + 'material_everypart/' + pic_name + '/' + '6th.mp4'
                    + ' -i ' + 'material_mp3/' + pic_name + '/' + '6th.mp3' + ' -strict -2 -f mp4 '
                    + outfile_name, shell=True)
    print("第六部分内容处理完毕，如果发现黑屏请调整改部分的clean_word")
