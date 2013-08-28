#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Skype4Py
import datetime
import random
import time

ROOM = '12新卒会議'
MSG_HEAD = [
    'アピリッツ！ 今日も良い一日でしたね',
    'そろそろ定時になりますよ〜。お仕事ちゃんと終わってます？',
    '今日も一日、お疲れ様でした〜',
    'お疲れさまです。今日も夢いっぱいの一日でしたね'
]
MSG_BODY_WEEKDAY = [
    '明日も頑張っていきましょうね！',
    'それではまた明日！',
    '明日のためにも今日はゆっくり休んでくださいね',
    'みんなが幸せになる世界を目指して、明日も頑張りましょうね',
    '今日もこれでお別れですね…。さ、寂しくなんかないです！ もう帰ってください！'
]
MSG_BODY_HOLIDAY = [
    '明日は休日です。おウチに帰ったらゆっくり休んでくださいね',
    'それでは、また来週お会いしましょう',
    '２日間のお別れですね…。さ、寂しくなんかないですよ！ 早く帰ってください！'
]

def today():
    return datetime.datetime.now()

def nextday():
    return datetime.date.today() + datetime.timedelta(1)

def messageHead():
    size = len(MSG_HEAD)
    index = random.randrange(size)
    return MSG_HEAD[index]

def messageBody(day):
    weekday = day.weekday()
    messages = (weekday < 5 and MSG_BODY_WEEKDAY) or MSG_BODY_HOLIDAY
    size = len(messages)
    index = random.randrange(size)
    return messages[index]

def selectChatFromBookmark(skype, topic):
    for bookmarkedChat in skype.BookmarkedChats:
        if bookmarkedChat.Topic == topic:
            return bookmarkedChat

def main():
    skype = Skype4Py.Skype()
    skype.Attach()
    topic = unicode(ROOM, 'utf-8')
    msg_head = unicode(messageHead(), 'utf-8')
    msg_body = unicode(messageBody(nextday()), 'utf-8')
    chat = selectChatFromBookmark(skype, topic)
    if chat is None:
        print 'ブックマークが見つかりません'
    else:
        chat.SendMessage(msg_head)
        time.sleep(10)
        chat.SendMessage(msg_body)

if __name__ == '__main__':
    main()
