# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '抓取文章正文内容' \
              '1.DateTimeProcess_Str 处理日期内容，如果始终没有日期可以抓取默认当天日期' \
              '2.ProcessContent 处理正文内容' \
              '3.提取unHtmlContent（无格式的文字内容）' \
              '4.提取content（含有CSS样式的内容）'

import re
from gerapy_auto_extractor.extractors import extract_detail
import time


# 处理日期数据函数
def DateTimeProcess_Str(text):
    try:
        time_text = str(text)
    except:
        time_text = time.strftime('%Y-%m-%d')

    if ("年" or "月" or "日") in str(text):
        time_text = re.findall('\d{4}年\d{2}月\d{2}', time_text)[0]
        time_text = re.sub(r'[年月]', '-', time_text)
        time_text = re.sub(r'[日]', '', time_text)
        return time_text
    elif "-" in time_text:
        time_text = re.findall('\d{4}-\d{2}-\d{2}', time_text)[0]
        return time_text
    else:
        return time.strftime('%Y-%m-%d')


# 判断内容是否None
def None2Str(text):
    if text is None:
        return ''
    else:
        return text


# 根据具体情况进行改变
# len(item['content']) < 5  替换成 len(None2Str(item['content'])) < 5
def ProcessContent(self, response):
    # 设置详情页的内容
    item = response.meta['item']

    data = extract_detail(response.text)

    # 处理详情页的时间,如果始终没有获取到时间默认当天日期
    if data["datetime"] is None:
        item['publishTime'] = DateTimeProcess_Str(item['publishTime'])
    else:
        item['publishTime'] = DateTimeProcess_Str(data["datetime"])

    # 处理详情页带格式，这里整个页面进行抓取
    item['content'] = ""
    if item['web_name'] == "中国煤炭市场":
        if 'class="news_show"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="news_show"]').extract_first()
        if 'id="Zoom"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="Zoom"]').extract_first()
    elif item['web_name'] == "中国煤炭新闻网":
        if 'class="newsContent"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//td[@class="newsContent"]').extract_first()
        if 'class="content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="content"]').extract_first()
        if 'class="entry"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="entry"]').extract_first()
    elif item['web_name'] == "国家煤炭工业网":
        if 'class="content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="content"]').extract_first()
    elif item['web_name'] == "39健康网":
        if 'id="contentText"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="contentText"]').extract_first()
        if 'class="art_content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="art_content"]').extract_first()
        if 'class="art_con"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="art_con"]').extract_first()
        if 'class="wrap"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="wrap"]').extract_first()
    elif item['web_name'] == "99健康网":
        if 'class="new_cont detail_con"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="new_cont detail_con"]').extract_first()
        if 'class="dt_left"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="dt_left"]').extract_first()
        if 'class="list_left"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="list_left"]').extract_first()
    elif item['web_name'] == "北京中医协会":
        if 'class="g-content m-main-info"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="g-content m-main-info"]').extract_first()
        if 'class="g-common"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="g-common"]').extract_first()
    elif item['web_name'] == "中国农网":
        if 'class="content-main fl"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="content-main fl"]').extract_first()
    elif item['web_name'] == "快科技":
        if 'class="news_info"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="news_info"]').extract_first()
    elif item['web_name'] == "36氪":
        if 'class="article-content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="article-content"]').extract_first()
    elif item['web_name'] == "中国甘肃网":
        if 'class="artical"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="artical"]').extract_first()
    elif item['web_name'] == "中安在线":
        if 'house.anhuinews.com' in response.url and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//table[@width="100%"]').get().encode(response.encoding).decode('gb18030')
        if 'class="info"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="info"]').extract_first()
        if 'class="shipin_info"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="shipin_info"]').extract_first()
        if 'align="center"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@align="center"]').extract_first()
        if 'class="con"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="con"]').extract_first()
        if 'valign="top"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//td[@valign="top"]').extract_first()
        if 'id="Zoom"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="Zoom"]').extract_first()
        if 'class="dicontent_left2"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="dicontent_left2"]').extract_first()
        if 'class="dicontent mt5"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="dicontent mt5"]').extract_first()
        if 'class="dicontent_left"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="dicontent_left"]').extract_first()
        if 'class="left new_left Nes_text"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="left new_left Nes_text"]').extract_first()
        if 'class="main_xq"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="main_xq"]').extract_first()
        if 'class="wm_xl_content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="wm_xl_content"]').extract_first()
    elif item['web_name'] == "长江网":
        if 'class="make"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="make"]').extract_first()
    elif item['web_name'] == "荆楚网":
        if 'class="artibody"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="artibody"]').extract_first()
        if 'class="article_w"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="article_w"]').extract_first()
    elif item['web_name'] == "中国宁波网":
        if 'id="Zoom"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="Zoom"]').extract_first()
        if 'id="contentText"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="contentText"]').extract_first()
        if 'class="content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="content"]').extract_first()
    elif item['web_name'] == "西部网":
        if 'class="con-detail"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="con-detail"]').extract_first()
    elif item['web_name'] == "北京旅游网":
        if 'class="mod-content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="mod-content"]').extract_first()
        if 'id="Article"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="Article"]').extract_first()
    elif item['web_name'] == "中国经济网":
        if 'class="content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="content"]').extract_first()
        if 'tbody' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//tbody').extract_first()
        if 'body' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//body').extract_first()
    elif item['web_name'] == "中国网":
        if 'class="list"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="list"]').extract_first()
        if 'class="fl w650"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="fl w650"]').extract_first()
        if 'class="leftBox"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="leftBox"]').extract_first()
        if 'class="content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="content"]').extract_first()
        if 'class="center_box"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="center_box"]').extract_first()
        if 'class="video-left"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="video-left"]').extract_first()
        if 'class="detailsPBox"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="detailsPBox"]').extract_first()
        if 'class="List"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="List"]').extract_first()
        if 'class="entry"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="entry"]').extract_first()
        if 'class="fl navl"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="fl navl"]').extract_first()
        if 'class="xwzw"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="xwzw"]').extract_first()
        if 'class="center_photo"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="center_photo"]').extract_first()
        if 'class="text"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="text"]').extract_first()
        if 'id="chan_newsDetail"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="chan_newsDetail"]').extract_first()
        if 'class="article-detail-inner article-relevance w660 ov"' in response.text and len(
                None2Str(item['content'])) < 5:
            item['content'] = response.xpath(
                '//div[@class="article-detail-inner article-relevance w660 ov"]').extract_first()
        if 'class="article-detail-inner article-relevance ov"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath(
                '//div[@class="article-detail-inner article-relevance ov"]').extract_first()
        if 'class="artCon"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="artCon"]').extract_first()
        if 'class="c_content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="c_content"]').extract_first()
        if 'class="main_c"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="main_c"]').extract_first()
        if 'class="artbody"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="artbody"]').extract_first()
        if 'class="post__PostWrapper-sc-1gspif5-0 aeDQn"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="post__PostWrapper-sc-1gspif5-0 aeDQn"]').extract_first()
        if 'id="fontzoom"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="fontzoom"]').extract_first()
        if 'class="cp"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="cp"]').extract_first()
        if 'class="detailText"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="detailText"]').extract_first()
        if 'id="menucontainer0_10"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="menucontainer0_10"]').extract_first()
        if 'id="main"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@id="main"]').extract_first()
        if 'class="Left"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="Left"]').extract_first()
        if 'class="center"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="center"]').extract_first()
        if 'class="d3_left_text"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="d3_left_text"]').extract_first()
        if 'class="big_img"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="big_img"]').extract_first()
        if 'class="main_l"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="main_l"]').extract_first()
        if 'class="box_con"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="box_con"]').extract_first()
        if 'class="inner-left"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="inner-left"]').extract_first()
        if 'align="left"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//td[@align="left"]').extract_first()
        if 'class="Content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="Content"]').extract_first()
        if 'class="main"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="main"]').extract_first()
    elif item['web_name'] == "中国质量新闻网":
        if 'class="content"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="content"]').extract_first()
        if 'class="pageLeft fl"' in response.text and len(None2Str(item['content'])) < 5:
            item['content'] = response.xpath('//div[@class="pageLeft fl"]').extract_first()
    # 通用的方法页面数据无法采集默认抓取整个页面
    if len(item['content']) < 5:
        item['content'] = response.xpath('//body').extract_first()

    return item
