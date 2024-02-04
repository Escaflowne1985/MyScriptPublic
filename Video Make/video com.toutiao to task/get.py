#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 任务链接

# https://mp.toutiao.com/xg-editor-api/ttv/query?task_id=


# In[15]:


import json
import requests
import pandas as pd
import os
import shutil

pathd=os.getcwd()+'\image'
if os.path.exists(pathd): #判断mydata文件夹是否存在
    for root, dirs, files in os.walk(pathd, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name)) #删除文件
        for name in dirs:
            os.rmdir(os.path.join(root, name)) #删除文件夹
    os.rmdir(pathd) #删除mydata文件夹
os.mkdir(pathd) #创建mydata文件夹

# # 生成需要文档的数据集

# In[ ]:


# 手动复制数据文件
# https://mp.toutiao.com/xg-editor-api/ttv/query?task_id=
with open("data.txt",encoding="utf8") as f:
    data = json.loads(f.read())

data_list = data["data"]["text_2_video_resp"]["sect_infos"]

# 下载图片和整合文字信息
df_list = []
for i in range(len(data_list)):
    id_ = str(i) + ".jpg"
    txt = data_list[i]["text"]
    time_start = data_list[i]["elems"][0]["time"]["start_offset"]
    time_end = data_list[i]["elems"][0]["time"]["end_offset"]
    image_url = data_list[i]["elems"][0]["cover_url"]

#     print(txt,time_start,time_end,image_url)
    html = requests.get(image_url)
    with open("image/{}".format(id_),"wb") as f:
        f.write(html.content)
    df_list.append((id_,txt,time_start,time_end,image_url))
        
df = pd.DataFrame(df_list,columns=["jpg","text","start","end","url"])

df


# In[ ]:





# # 配合剪映文档制作数据文件

# In[15]:


with open("_draft_content.json",encoding="utf8") as f:
    data = json.loads(f.read())
    
n = df.index.max() + 1

df["duration"] = df["end"] - df["start"]


# ## 生成画布的 canvases

# In[16]:


# 这里的数据结构 每次更换的是id
canvases = []
for i in range(n):
    canvases_dict = {
        'album_image': '',
        'blur': 0.0,
        'color': '',
        'id': '{}'.format("canvases-" + str(i)),
        'image': '',
        'image_id': '',
        'image_name': '',
        'type': 'canvas_color'
    }
    canvases.append(canvases_dict)
# canvases


# In[17]:


data["materials"]["canvases"] = canvases


# ## 生成画布动画 material_animations

# In[18]:


material_animations = []
for i in range(n):
    material_animations_dict = {
        'animations': [], 
        'id': '{}'.format("material_animations-" + str(i)),
        'type': 
        'sticker_animation'
    }
    material_animations.append(material_animations_dict)
# material_animations


# In[19]:


data["materials"]["material_animations"] = material_animations


# ## 生成 速度配置 speeds 

# In[20]:


speeds = []
for i in range(n):
    speeds_dict = {
        'curve_speed': None,
        'id': '{}'.format("speeds-" + str(i)),
        'mode': 0,
        'speed': 1.0,
        'type': 'speed'
    }
    speeds.append(speeds_dict)
# speeds


# In[21]:


data["materials"]["speeds"] = speeds


# ## 生成文本texts

# In[22]:


# 备注：字符串暂时没弄
texts = []
for i in range(n):
    texts_dict = {
        'add_type': 0,
        'alignment': 1,
        'background_alpha': 1.0,
        'background_color': '',
        'background_height': 1.0,
        'background_horizontal_offset': 0.0,
        'background_round_radius': 0.0,
        'background_vertical_offset': 0.0,
        'background_width': 1.0,
        'bold_width': 0.0,
        'border_color': '#ffffff',
        'border_width': 0.08,
        'check_flag': 15,
        'content': '<outline color=(1,1,1,1) width=0.08><size=11><color=(0,0,0,1)><font id="" path="D:/MyTools/JianyingPro/3.4.1.9179/Resources/Font/SystemFont/zh-hans.ttf">[{}]</font></color></size></outline>'.format(df["text"][i]),
        'font_category_id': '',
        'font_category_name': '',
        'font_id': '',
        'font_name': '',
        'font_path': 'D:/MyTools/JianyingPro/3.4.1.9179/Resources/Font/SystemFont/zh-hans.ttf',
        'font_resource_id': '',
        'font_size': 11.0,
        'font_title': 'none',
        'font_url': '',
        'fonts': [],
        'global_alpha': 1.0,
        'has_shadow': False,
        'id': '{}'.format("texts-" + str(i)),
        'initial_scale': 1.0,
        'is_rich_text': False,
        'italic_degree': 0,
        'ktv_color': '',
        'layer_weight': 1,
        'letter_spacing': 0.0,
        'line_spacing': 0.02,
        'recognize_type': 0,
        'shadow_alpha': 0.0,
        'shadow_angle': -45.0,
        'shadow_color': '#000000',
        'shadow_distance': 8.0,
        'shadow_point': {'x': 1.0182337649086284, 'y': -1.0182337649086284},
        'shadow_smoothing': 0.99,
        'shape_clip_x': False,
        'shape_clip_y': False,
        'style_name': '黑字白边',
        'sub_type': 0,
        'text_alpha': 1.0,
        'text_color': '#000000',
        'text_size': 30,
        'text_to_audio_ids': [],
        'type': 'text',
        'typesetting': 0,
        'underline': False,
        'underline_offset': 0.22,
        'underline_width': 0.05,
        'use_effect_default_color': False
    }
    texts.append(texts_dict)
# texts


# In[23]:


data["materials"]["texts"] = texts


# ## 视频轨道video_trackings

# In[24]:


video_trackings = []
for i in range(n):
    video_trackings_dict = {
        'config': {'center_x': 0.0,
        'center_y': 0.0,
        'height': 0.0,
        'rotation': 0.0,
        'width': 0.0},
        'enable_scale': False,
        'enable_video_tracking': True,
        'id': '{}'.format("video_trackings-" + str(i)),
        'map_path': '',
        'result_path': '',
        'tracker_type': 0,
        'trackers': [],
        'tracking_time_range': 0,
        'type': 'video_tracking',
        'version': ''
    }
    video_trackings.append(video_trackings_dict)
# video_trackings


# In[25]:


data["materials"]["video_trackings"] = video_trackings


# ## 视频 videos

# In[26]:


videos = []
for i in range(n):
    videos_dict = {
        'audio_fade': None,
        'cartoon_path': '',
        'category_id': '',
        'category_name': 'local',
        'check_flag': 30719,
        'crop': {'lower_left_x': 0.0,
        'lower_left_y': 1.0,
        'lower_right_x': 1.0,
        'lower_right_y': 1.0,
        'upper_left_x': 0.0,
        'upper_left_y': 0.0,
        'upper_right_x': 1.0,
        'upper_right_y': 0.0},
        'crop_ratio': 'free',
        'crop_scale': 1.0,
        'duration': 10800000000,
        'extra_type_option': 0,
        'formula_id': '',
        'gameplay': None,
        'has_audio': False,
        'height': 1080,
        'id': '{}'.format("videos-" + str(i)),
        'intensifies_audio_path': '',
        'intensifies_path': '',
        'is_unified_beauty_mode': False,
        'material_id': '',
        'material_name': '{}.jpg'.format(i),
        'material_url': '',
        'matting': {'flag': 0, 'interactiveTime': [], 'path': ''},
        'path': 'F:/PythonWorkProject/07.新媒体内容创作/02.AI视频创作/（横版）头条图文转视频转换/image/{}.jpg'.format(i),
        'reverse_intensifies_path': '',
        'reverse_path': '',
        'source_platform': 0,
        'stable': None,
        'type': 'photo',
        'video_algorithm': {'algorithms': [], 'path': '', 'time_range': None},
        'width': 1920
    }
    videos.append(videos_dict)
# videos


# In[27]:


data["materials"]["videos"] = videos


# ## tracks 轨道主线

# In[28]:


false = False
true = True
null = None

# source_timerange,target_timerange 需要再定义


# In[29]:


tracks_0_segments = []
for i in range(n):
    tracks_0_segments_dict = {
          "cartoon": false,
          "clip": {
            "alpha": 1.0,
            "flip": {
              "horizontal": false,
              "vertical": false
            },
            "rotation": 0.0,
            "scale": {
              "x": 1.0,
              "y": 1.0
            },
            "transform": {
              "x": 0.0,
              "y": 0.0
            }
          },
          "enable_adjust": true,
          "enable_color_curves": true,
          "enable_color_wheels": true,
          "enable_lut": true,
          "extra_material_refs": [
            "speeds-{}".format(i),
            "canvases-{}".format(i),
            "video_trackings-{}".format(i)
          ],
          "group_id": "",
          "hdr_settings": {
            "intensity": 1.0,
            "mode": 1,
            "nits": 1000
          },
          'id': '{}'.format("tracks_0_segments-" + str(i)),
          "intensifies_audio": false,
          "is_tone_modify": false,
          "keyframe_refs": [],
          "last_nonzero_volume": 1.0,
          "material_id": "videos-{}".format(i),
          "render_index": 0,
          "reverse": false,
          "source_timerange": {
            "duration": int(df["duration"][i] * 1000000),
            "start": 0
          },
          "speed": 1.0,
          "target_timerange": {
            "duration": int(df["duration"][i] * 1000000),
            "start": int(df["start"][i] * 1000000)
          },
          "track_attribute": 0,
          "track_render_index": 0,
          "visible": true,
          "volume": 1.0
        }
    tracks_0_segments.append(tracks_0_segments_dict)
# tracks_0_segments


# In[30]:


data["tracks"][0]["segments"] = tracks_0_segments


# In[31]:


tracks_1_segments = []
for i in range(n):
    tracks_1_segments_dict = {
          "cartoon": false,
          "clip": {
            "alpha": 1.0,
            "flip": {
              "horizontal": false,
              "vertical": false
            },
            "rotation": 0.0,
            "scale": {
              "x": 0.7322295026571091,
              "y": 0.7322295026571091
            },
            "transform": {
              "x": 0.0,
              "y": -0.8020681595802306
            }
          },
          "enable_adjust": false,
          "enable_color_curves": true,
          "enable_color_wheels": true,
          "enable_lut": false,
          "extra_material_refs": [
            "material_animations-{}".format(i)
          ],
          "group_id": "",
          "hdr_settings": null,
          'id': '{}'.format("tracks_1_segments-" + str(i)),
          "intensifies_audio": false,
          "is_tone_modify": false,
          "keyframe_refs": [],
          "last_nonzero_volume": 1.0,
          "material_id": "texts-{}".format(i),
          "render_index": 14000,
          "reverse": false,
          "source_timerange": null,
          "speed": 1.0,
          "target_timerange": {
            "duration": int(df["duration"][i]*1000000),
            "start": int(df["start"][i]*1000000)
          },
          "track_attribute": 0,
          "track_render_index": 0,
          "visible": true,
          "volume": 1.0
        }
    tracks_1_segments.append(tracks_1_segments_dict)
# tracks_1_segments


# In[32]:


data["tracks"][1]["segments"] = tracks_1_segments


# ## 保存结果文件

# In[33]:


result_txt = json.dumps(data)
# result_txt = result_txt.replace()

with open("draft_content.json",'w+',encoding="utf8") as f:
    f.write(result_txt)


with open("data.txt",encoding="utf8") as f:
    data = json.loads(f.read())
    title = data["data"]["text_2_video_resp"]["video_title"]
    
# 桌面创建文件夹
dir_name = r'C:\Users\pc\Desktop\{}'.format(title)
os.mkdir(dir_name)

# 移动制作好的draft_content.json和image到创建的文件夹下
shutil.copy("draft_content.json",dir_name)  
shutil.copy("draft_content.json",r"F:\PythonWorkProject\07.新媒体内容创作\JianyingPro Drafts\AI新闻说")  

# 创建image文件夹
dir_name = r'C:\Users\pc\Desktop\{}\image'.format(title)
os.mkdir(dir_name)

# 移动image下面的文件夹
for i in os.listdir("image/"):
    shutil.copy("image/"+i ,dir_name)
    
    
result_str = "。".join(df["text"].tolist())
with open("content.txt",'w+') as f:
    f.write(result_str)