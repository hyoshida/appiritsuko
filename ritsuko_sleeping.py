#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Skype4Py
import os
import time
import random

HOUR_TO_SLEEP = 1
ROOM = '12新卒会議'
CONFIG_DIR = '.appiritsko'
CONFIG_FILE = 'talk.ini'
_DEBUG_ = False
MESSAGE = [
    'ふわぁ〜ぁ・・・・・・ぁ、ね、ね、寝てませんよっ',
    '・・・・・・・・・Zzz・・・',
    '・・・・・・Zzz・・・・・・',
    '・・・Zzz・・・・・・・・・'
]

def touch(filepath, times=None):
    f = file(filepath, 'a')
    try:
        os.utime(filepath, times)
    finally:
        f.close()

def getConfigPath():
    home = os.environ.get('HOME')
    return os.path.join(home, CONFIG_DIR, CONFIG_FILE)

def isSleeping():
    filepath = getConfigPath()
    stat = os.stat(filepath)
    past_time = time.mktime(time.localtime(stat.st_mtime))
    now = time.mktime(time.localtime())
    return (now - past_time) >= (60 * 60 * HOUR_TO_SLEEP)

def message():
    size = len(MESSAGE)
    index = random.randrange(size)
    return MESSAGE[index]

def sleeping():
    filepath = getConfigPath()
    touch(filepath)
    return message()

def selectChatFromBookmark(skype, topic):
    for bookmarkedChat in skype.BookmarkedChats:
        if bookmarkedChat.Topic == topic:
            return bookmarkedChat

def main():
    if not isSleeping():
        return
    skype = Skype4Py.Skype()
    skype.Attach()
    topic = unicode(ROOM, 'utf-8')
    chat = selectChatFromBookmark(skype, topic)
    if chat is None:
        print 'ブックマークが見つかりません'
    else:
        if _DEBUG_:
            print sleeping()
        else:
            chat.SendMessage(unicode(sleeping(), 'utf-8'))

if __name__ == '__main__':
    main()
