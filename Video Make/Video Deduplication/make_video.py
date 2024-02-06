# ffmpeg 命令

import os
import sys
import random

# eq: 用于调整亮度、对比度和饱和度。
# brightness=0.2将亮度增加 0.2
# saturation=1.5将饱和度增加 1.5，
# contrast=1.2将对比度增加 1.2。
# unsharp: 用于锐化。这里的参数5:5:1.0:5:5:0.0表示锐化的强度和半径。
# hqdn3d: 用于降噪。这里的参数1.5:1.5:6:6表示降噪的强度。

fps = 25  # 导出视频帧率

# 亮度，饱和度，对比度方法
brightness_num = 0.2  # 将亮度增加 [-1 - 1]
saturation_num = 1.5  # 将饱和度增加 [0 - 3]
contrast_num = 1.2  # 将对比度增加 [-2 - 2]
function_eq = "eq=brightness={}:saturation={}:contrast={}".format(brightness_num, saturation_num, contrast_num)

# 锐化
unsharp_l_msize_x = 5  # X方向的锐化半径 [3 - 23]
unsharp_l_msize_y = 5  # Y方向的锐化半径 [3 - 23]
unsharp_l_amount = 5  # 锐化强度 [-2 - 5]
function_eunsharp = "unsharp={}:{}:{}".format(unsharp_l_msize_x, unsharp_l_msize_y, unsharp_l_amount)

# 降噪
hqdn3d_luma_spatial = 1.5  # 空间降噪强度，较大的值会增加降噪效果。
hqdn3d_chroma_spatial = 1.5  # 色度通道空间降噪强度，较大的值会增加降噪效果。
hqdn3d_luma_tmp = 6  # 时间降噪强度，较大的值会增加降噪效果。
hqdn3d_chroma_tmp = 6  # 色度通道时间降噪强度，较大的值会增加降噪效果。
function_hqdn3d = "hqdn3d={}:{}:{}:{}".format(hqdn3d_luma_spatial, hqdn3d_chroma_spatial, hqdn3d_luma_tmp, hqdn3d_chroma_tmp)

# 分辨率处理
scale_dict = {
    "480P": {"scale_x": "854", "scale_y": "480"},
    "720P": {"scale_x": "1280", "scale_y": "720"},
    "1080P": {"scale_x": "1920", "scale_y": "1080"},
    "横竖互换": {"scale_x": "ih", "scale_y": "iw"},
}
scale_480 = "scale={}:{}".format(scale_dict["480P"]["scale_x"], scale_dict["480P"]["scale_y"])  # 480P
scale_720 = "scale={}:{}".format(scale_dict["720P"]["scale_x"], scale_dict["720P"]["scale_y"])  # 720P
scale_1080 = "scale={}:{}".format(scale_dict["1080P"]["scale_x"], scale_dict["1080P"]["scale_y"])  # 1080P
scale_transpose = "scale={}:{}".format(scale_dict["横竖互换"]["scale_x"], scale_dict["横竖互换"]["scale_y"])  # 横竖转换
function_scale = scale_480

# 视频拉伸
function_setdar = "setsar=1"

# 视频旋转
transpose_dict = {
    "逆时针旋转90度": "transpose=1",
    "顺时针旋转90度": "transpose=2",
    "水平旋转": "hflip",
    "垂直旋转": "vflip",
    "不操作": ""
}
function_transpose = transpose_dict["水平旋转"]

# 视频抽帧
frame_set = random.randint(20, 30)
function_select_v = "select='(mod(n\,{}))',setpts=N/FRAME_RATE/TB".format(frame_set)
function_select_a = "aselect='(mod(n\,{}))',asetpts=N/SR/TB".format(frame_set)

zoom_in = "zoompan=z='if(lte(on,100),zoom+0.01,1.5)':x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2':d=1, fade=in:st=0:d=1:alpha=1, fade=out:st=99:d=1:alpha=1"

function_vf = ", ".join([
    function_eq,  # 亮度，饱和度，对比度方法
    function_eunsharp,  # 锐化
    function_hqdn3d,  # 降噪
    function_scale,  # 分辨率处理
    function_setdar,  # 视频拉伸
    function_transpose,  # 视频旋转
    function_select_v,  # 视频抽帧
    # zoom_in,  # 逐帧放大
])
function_af = ",".join([
    function_select_a  # 视频抽帧保持原音频匹配
])

cmd = 'ffmpeg -i demo.mp4 -vf "{} " -af "{}" -r {}  result/video.mp4'.format(
    function_vf, function_af, fps
)
# os.system(cmd)
