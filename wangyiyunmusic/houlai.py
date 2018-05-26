#！/user/bin/pytthon
# -*- coding:utf-8 -*-
# @Time: 2018/5/23 15:58
# @Author: lichexo
# @File: houlai.py

import requests
import json


url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_553310243?csrf_token=846f018c0d8662a03bc6f0016cdf7f67'

headers = {
'Host': 'music.163.com',
'Origin': 'http://music.163.com',
'Referer': 'http://music.163.com/song?id=553310243',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
              ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

# 因为是post提交，采用MD5或者其他算法加密过，但是我们可以直接使用加密后的数据，用于浏览器识别身份
User_Data = {
    'params': 'nUMvtApJ7WYkBgVTUGdhecvhjBsh0HbqJg6r0VvWTUfvTg7YN2wNXktF43ho0PVaiH9o7nf2IWGX2pqiMqD7SEKTydD3HY/'
              'sfShNexswo2+Rn4zVBoDS6oalcHGxEBr2aRRZddaM2A3Tr/ePgNtu7p/oCnHdrzOoyJ8IfrJ0K/drrD6N3xNpAYYQm7XzxCsgiI0hHTlF+y+EeLW5O5hwi11SYTZcMlkwfykhLtTcTKU=',
    'encSecKey': 'c9361204a87ab4bcd6f8690c16675c24c5458eab4348599354871643bdeeb8db52a33048ae036936e0a1fddc7a43ff7688'
                 'f38015a3b8a05b3db9087340a1be42303c56588a331f3e66a5c28255ae9b5f9140a96e6066689e'
                 '74be945fc5c395393de71d5d4adf6b093f577bbc7bc485235d37f613e57b6aec2a26ad06bb16db8f'
}

response = requests.post(url, headers=headers, data= User_Data)

data = json.loads(response.text)
hotcomments = []
for hotcomment in data['hotComments']:
    item ={
        'nickname':hotcomment['user']['nickname'],
        'content':hotcomment['content'],
        'likedCount':hotcomment['likedCount']
    }
    hotcomments.append(item)
# 获取评论用户名，内容，以及对应的点赞数
nickname_list = [content['content']for content in hotcomments]
content_list = [content['nickname']for content in hotcomments]
likedCount_list = [content['likedCount']for content in hotcomments]

from pyecharts import Bar
# 图表展示
bar = Bar('评论中点赞数显示图')
bar.add('点赞数',nickname_list,likedCount_list, is_stack=True, mark_line=['min', 'max'], mark_point=['average'] )
bar.render()

from wordcloud import WordCloud
import matplotlib.pyplot as plt
# 词云展示
content_text = " ".join(content_list)
wordcloud = WordCloud(font_path=r"F:\字体\21\YGY20070701.ttf",max_words=200).generate(content_text)
plt.figure()
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.show()