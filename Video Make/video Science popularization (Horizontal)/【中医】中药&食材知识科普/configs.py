# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '配置参数文件'


def config():
    # 字体配置文件
    font_path = './font/kaiti.ttf'
    # 字段英文_中文字典
    column_en2cn_dict = {
        "CnName": "药材名称",
        "PinYin": "汉语拼音",
        "LaiYuan": "文件原文",
        "LaDing": "原拉丁植物动物矿物名",
        "YCJY": "药材基原",
        "YWGJ": "性味归经",
        "GNZZ": "功能主治",
        "QYFB": "地理分布",
        "SS": "省市",
        "EnName": "英文名",
        "YCBM": "药材别名",
        "HXCF": "化学成分",
        "MJLS": "名家论述",
        "LDWM": "拉丁文名",
        "YLZY": "药理作用",
        "FF": "附方",
        "XDLCYJ": "现代临床研究",
        "ZYSX": "注意事项",
        "YYLB": "药用类别",
        "XDHYJ": "现代化研究",
    }
    # 字段中文_英文字典
    column_cn2en_dict = {
        '药材名称': "CnName",
        '汉语拼音': "PinYin",
        '文件原文': "LaiYuan",
        '原拉丁植物动物矿物名': "LaDing",
        '药材基原': "YCJY",
        '性味归经': "YWGJ",
        '功能主治': "GNZZ",
        '地理分布': "QYFB",
        '省市': "SS",
        '英文名': "EnName",
        '药材别名': "YCBM",
        '化学成分': "HXCF",
        '名家论述': "MJLS",
        '拉丁文名': "LDWM",
        '药理作用': "YLZY",
        '附方': "FF",
        '现代临床研究': "XDLCYJ",
        '注意事项': "ZYSX",
        '药用类别': "YYLB",
        '现代化研究': "XDHYJ"}

    return font_path, column_en2cn_dict, column_cn2en_dict
