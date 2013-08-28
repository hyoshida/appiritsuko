#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Skype4Py
import datetime
import random
import time

ROOM = '12新卒会議'
MSG_HEAD = [
    'アピリッツ！',
    'おはようございます',
    '昨日はよく眠れましたか？',
    'おはよ〜ございま〜す…',
    'みなさん、遅刻なんてしてないですよね？'
]
MSG_BODY_WEEKDAY = [
    '今日も一日、頑張っていきましょうね！',
    '今日も夢に向かって頑張っていきましょうね！',
    '今日も良い日でありますように',
    'あの、べ、別にいつもみなさんのことを待ってるわけじゃないですからね！'
]
MSG_BODY_HOLIDAY = [
    '明日はお休みですからね。気合入れていきましょう！',
    '今週も今日で終わりですから、仕事を貯めないように気をつけてくださいね',
    '明日はお休みですから、今日は余裕を持った仕事ができると良いですね'
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
