# coding:utf-8
__author__ = 'Mr.数据杨'
__explain__ = '文字处理程序'


# 文字处理对应方法 20个字符换行 常规使用
def clean_word(word):
    n = 20
    word_len = int(len(word) / n)
    word_num = 0
    while word_num <= word_len:
        if word_num == 0:
            strs = word[:(word_num + 1) * n] + "\n"
        else:
            #             strs = word[:(word_num + 1) * 8] + "..."
            strs = strs + word[word_num * n:(word_num + 1) * n] + "\n"
        word_num = word_num + 1
    return word_len, strs
