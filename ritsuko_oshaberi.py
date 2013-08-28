#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import ConfigParser

import Skype4Py
import datetime
import time

import csv

_DEBUG_ = False
ROOM = '12新卒会議'

CONFIG_DIR = '.appiritsko'
CONFIG_FILE = 'talk.ini'
TALK_COUNTER_SECTION = 'counter'
TALK_COUNTER_FILE = 'talk_counter.ini'
SKYPE_MEMBERS_FILE = 'members.tsv'

def fullName(skype_name):
    members = loadSkypeMembers()
    return members[skype_name] if members.has_key(skype_name) else skype_name

def loadSkypeMembers():
    try:
        members_tsv_path = os.path.join(os.path.dirname(__file__), SKYPE_MEMBERS_FILE)
        members_tsv = csv.reader(file(members_tsv_path), delimiter = '\t')
        return dict(members_tsv)
    except IOError:
        return {}

def createMaxCountMessage():
    result = ''
    counts_dict = loadCounts(TALK_COUNTER_SECTION)
    for key,value in sorted(counts_dict.items(), key=lambda x:int(x[1]), reverse=True):
        result = '今日のおしゃべりさんは ' + fullName(key) + 'さん(' + value + ') でしたー！'
        break
    deleteSection(TALK_COUNTER_SECTION)
    return result

def loadCounts(section = TALK_COUNTER_SECTION):
    config = getConfig()
    filepath = getConfigPath()
    config.read(filepath)
    result = {}
    for key in config.options(section):
        result[key] = config.get(section, key)
    return result


def getConfig():
    return ConfigParser.SafeConfigParser()

def getConfigPath():
    home = os.environ.get('HOME')
    return os.path.join(home, CONFIG_DIR, CONFIG_FILE)

def loadValue(key, section = 'DEFAULT'):
    config = getConfig()
    filepath = getConfigPath()
    config.read(filepath)
    if not section in config.sections():
        config.add_section(section)
    return config.get(section, key)

def saveValue(key, value, section = 'DEFAULT'):
    config = getConfig()
    filepath = getConfigPath()
    config.read(filepath)
    if not section in config.sections():
        config.add_section(section)
    result = config.set(section, key, value)
    with open(filepath, 'w') as fp:
        config.write(fp)
    return result

def deleteSection(section = 'DEFAULT'):
    config = getConfig()
    filepath = getConfigPath()
    config.read(filepath)
    result = False
    # backup file
    with open(filepath + todayPostfix(), 'w') as fp:
        config.write(fp)
    # delete section
    if section in config.sections():
        result = config.remove_section(section)
        with open(filepath, 'w') as fp:
            config.write(fp)
    return result

def todayPostfix():
    return '.' + datetime.date.today().strftime('%Y%m%d')

def selectChatFromBookmark(skype, topic):
    for bookmarkedChat in skype.BookmarkedChats:
        if bookmarkedChat.Topic == topic:
            return bookmarkedChat

def main():
    skype = Skype4Py.Skype()
    skype.Attach()
    topic = unicode(ROOM, 'utf-8')
    max_count_msg = unicode(createMaxCountMessage(), 'utf-8')
    chat = selectChatFromBookmark(skype, topic)
    if chat is None:
        print 'ブックマークが見つかりません'
    else:
        if _DEBUG_:
            print createMaxCountMessage()
        else:
            chat.SendMessage(max_count_msg)

if __name__ == '__main__':
    main()
