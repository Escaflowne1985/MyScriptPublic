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

# 加载使用的三方安装包
import pandas as pd

# 加载自定义py方法
from configs import *  # 工程配置数据
from ready_work import *  # 工程启动准备工作
from process_images import *  # 处理工程需要的图片数据
from process_audio import *  # 处理工程需要的音频数据
from process_video import *  # 处理工程需要的视频数据

"""
    拼接顺序制作
    "CnName":"药材名称"
    "LaiYuan":"文件原文"
    "YCBM":"药材别名",
    "YYLB":"药用类别",
    "PinYin":"汉语拼音",
    "LaDing":"原拉丁植物动物矿物名",
    "EnName":"英文名",
    "LDWM":"拉丁文名",
    "YCJY":"药材基原",
    "YWGJ":"性味归经",
    "GNZZ":"功能主治",
    "ZYSX":"注意事项",
    "YLZY":"药理作用",
    "QYFB":"地理分布",
    "SS":"省市", # 自定义生成图表使用
    "MJLS":"名家论述",
    "HXCF":"化学成分",
    "XDLCYJ":"现代临床研究",
    "XDHYJ":"现代化研究",
    "FF":"附方",
"""


# 按照顺序将视频进行拼接
def StitchingVideo(pic_name):
    file_dir = "material_video/" + pic_name + "/"
    video_list = [files for files in os.walk(file_dir)][0][2]

    # 素材路径
    path_material = "material_video/" + pic_name + "/"
    # 切换过场路径
    path_chanege = "material_base/change.mp4"
    # 封面文件路径
    path_cover = "./material_video/" + pic_name + "/" + "cover.mp4"
    # 结尾文件路径
    path_end = "material_base/end.mp4"

    L = []
    video = VideoFileClip(path_cover).resize((1280, 720))
    L.append(video)
    if "1st.mp4" in video_list:
        video = VideoFileClip(path_material + "1st.mp4").resize((1280, 720)).fadein(2, (1, 1, 1))
        L.append(video)
    if "2nd.mp4" in video_list:
        video = VideoFileClip(path_chanege).resize((1280, 720))
        L.append(video)
        video = VideoFileClip(path_material + "2nd.mp4").resize((1280, 720))
        video = video.set_duration(video.duration - 0.5)
        L.append(video)
    if "3rd.mp4" in video_list:
        video = VideoFileClip(path_chanege).resize((1280, 720))
        L.append(video)
        video = VideoFileClip(path_material + "3rd.mp4").resize((1280, 720))
        video = video.set_duration(video.duration - 0.5)
        L.append(video)
    if "4th.mp4" in video_list:
        video = VideoFileClip(path_chanege).resize((1280, 720))
        L.append(video)
        video = VideoFileClip(path_material + "4th.mp4").resize((1280, 720))
        video = video.set_duration(video.duration - 0.5)
        L.append(video)
    if "5th.mp4" in video_list:
        video = VideoFileClip(path_chanege).resize((1280, 720))
        L.append(video)
        video = VideoFileClip(path_material + "5th.mp4").resize((1280, 720))
        video = video.set_duration(video.duration - 0.5)
        L.append(video)
    if "6th.mp4" in video_list:
        video = VideoFileClip(path_chanege).resize((1280, 720))
        L.append(video)
        video = VideoFileClip(path_material + "6th.mp4").resize((1280, 720))
        video = video.set_duration(video.duration - 0.5)
        L.append(video)

    video = VideoFileClip(path_end).resize((1280, 720)).fadein(2, (1, 1, 1))
    L.append(video)

    final_clip = concatenate_videoclips(L)

    # 生成目标视频文件
    final_clip.to_videofile(path_material + "result.mp4", fps=60, remove_temp=False)

    # 将配乐和视频进行合成
    inmp4 = 'material_video/' + pic_name + '/' + 'result.mp4'
    inmp3 = 'material_mp3/music.mp3'
    outmp4 = 'material_result/【每日学中药】' + pic_name + '.mp4'

    cmd = 'ffmpeg -y -i ' + inmp4 + ' -i ' + inmp3 + ' -filter_complex \
    "[0:a]volume=10dB[a0]; \
    [1:a]volume=-10dB[a1]; \
    [a0][a1]amix=inputs=2[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -shortest ' + outmp4

    p = subprocess.call(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("合成最终文件和背景音乐完毕")

    ### 删除无用文件
    # 删除目录下生成的MP3文件
    path = "./"
    for infile in glob.glob(os.path.join(path, '*.mp3')):
        os.remove(infile)
    for infile in glob.glob(os.path.join(path, '*.html')):
        os.remove(infile)


if __name__ == '__main__':
    # 读取基础Excel数据基础信息
    df = pd.read_excel("data/data.xlsx")
    # 选择Excel中第num个数据进行制作，起始数据是2
    num = 20
    # 设置索引数字
    row = num - 1
    # 提取需要制作的行数据，并重置索引
    df = df.loc[row:row, :]
    df.reset_index(drop=True, inplace=True)
    # 提取本次制作内容的主题药材名称
    pic_name = df["药材名称"][0].replace("?", "")
    print("本次制作内容：", pic_name)

    # 加载配置文件
    # 提取使用的字体路径 font_path
    # 中英文对应的数据列名字典 column_en2cn_dict\column_cn2en_dict
    font_path, column_en2cn_dict, column_cn2en_dict = config()
    # 重命名列位英文好处理
    df = df.rename(columns=column_cn2en_dict)
    # 删除数据的无用字段
    df.drop(["_id"], inplace=True, axis=1)
    df.drop(["url"], inplace=True, axis=1)
    # 用replace替换掉数据中已经发现的无用部分,发现即追加
    df["QYFB"][0] = df["QYFB"][0]. \
        replace(" ", ""). \
        replace("生态环境", ""). \
        replace("资源分布", "")
    # 填充无数据的部分内容
    df = df.fillna("暂无数据")
    # 创建单词视频会使用的制作目录，对应目录以药材名称pic_name为顶级目录
    # 1.单条视频每个部分素材的目录 material_everypart
    # 2.合成每个部分素材的目录以及素材全部合并的目录 material_video
    # 3.单条视频使用的图片素材的目录 material_jpg
    # 4.单条视频使用的音频素材的目录 material_mp3
    MakeMaterialDir(pic_name)
    # 避免重复制作素材数据发生错误，每次都清空原有旧的数据
    # 1.清空单条视频每个部分素材目录 material_everypart
    # 2.清空合成每个部分素材目录 material_video
    # 3.清空单条视频使用的音频素材目录 material_mp3
    CleanFiles(pic_name)
    # 从百度百科抓取图片，如果错误需要更换
    # 未来尝试再wiki百科抓取
    RequestGetImage(pic_name)
    # 抓取的药材图片用算法自动去背景扣图
    CutoutJPG(pic_name)
    # 使用基础的背景图片合成抠图的影像合成图片到封面
    CompositeCoverJPG(pic_name)
    # 音频文件数据处理
    # 使用API接口生成字幕对应的音频文件保存到material_mp3的对应的目录下
    ChangeWordsToMp3(df)
    time_name_dict = Mp3Info(df)
    # 正文部分1-6
    try:
        FirstPart(pic_name, df, time_name_dict, column_en2cn_dict)
    except:
        pass
    try:
        SecondPart(pic_name, df, time_name_dict, column_en2cn_dict)
    except:
        pass
    try:
        ThirdPart(pic_name, df, time_name_dict, column_en2cn_dict)
    except:
        pass
    try:
        FourthPart(pic_name, df, time_name_dict, column_en2cn_dict)
    except:
        pass
    try:
        FifthPart(pic_name, df, time_name_dict, column_en2cn_dict)
    except:
        pass
    try:
        SixthPart(pic_name, df, time_name_dict, column_en2cn_dict)
    except:
        pass
    # 合成封面MP4文件
    MakeCoverMp4(pic_name)
    # 拼接视频合成背景音乐
    StitchingVideo(pic_name)
