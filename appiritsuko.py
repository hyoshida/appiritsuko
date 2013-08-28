#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import Skype4Py

import re
import random
import amasakas
import subprocess
import os
import ConfigParser

import csv
from urllib import urlopen

# for Support multi-byte message
import sys
import codecs
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)


class Oshaberisan:

    config_dir           = '.appiritsko'
    config_file          = 'talk.ini'
    talk_counter_section = 'counter'
    talk_counter_file    = 'talk_counter.ini'
    members_file         = 'members.tsv'

    def __init__(self):
        self.config = self._get_config()
        self.config_path = self._get_config_path()
        self.members = self._load_members()

    def build_count_message(self):
        result = ''
        count_map = self._load_count_map(self.talk_counter_section)
        for key, value in sorted(count_map.items(), key=lambda x:int(x[1]), reverse=True):
            result += u'%sさん: %s回\n' % ( self.__full_name(key), value )
        return result

    def save_count(self, name):
        value = 0
        try:
            value = self._load_value(name, self.talk_counter_section)
            if not value: value = 0
        except:
            value = 0
        return self._save_value(name, str(int(value) + 1), self.talk_counter_section)

    def _get_config(self):
        return ConfigParser.SafeConfigParser()

    def _get_config_path(self):
        home = os.environ.get('HOME')
        return os.path.join(home, self.config_dir, self.config_file)

    def _save_value(self, key, value, section = 'DEFAULT'):
        self.config.read(self.config_path)
        if not section in self.config.sections():
            self.config.add_section(section)
        result = self.config.set(section, key, value)
        with open(self.config_path, 'w') as fp:
            self.config.write(fp)
        return result

    def _load_value(self, key, section = 'DEFAULT'):
        self.config.read(self.config_path)
        if not section in self.config.sections():
            self.config.add_section(section)
        return self.config.get(section, key)

    def _load_count_map(self, section = 'DEFAULT'):
        self.config.read(self.config_path)
        result = {}
        for key in self.config.options(self.talk_counter_section):
            result[key] = self.config.get(self.talk_counter_section, key)
        return result

    def _load_members(self):
        try:
            members_tsv_path = os.path.join(os.path.dirname(__file__),  self.members_file)
            members_tsv = csv.reader(file(members_tsv_path), delimiter = '\t')
            return dict([ id, unicode(name, 'utf-8') ] for id, name in members_tsv)
        except IOError:
            return {}

    def __full_name(self, name):
        return self.members[name] if self.members.has_key(name) else name


class NormalChat:

    def  __init__(self, Message, Status):
        self.Message = Message
        self.Status = Status
        self.MessageHandler()

    def MessageHandler(self):
        if self.apio(): return
        if self.weather(): return
        if self.guess(): return

    def apio(self):
        if not re.search(r'[^a-zA-Z]?apio[^a-zA-Z]?', self.Message.Body):
            return False
        self._send(u'それは「りっつ=あぴお」のことですね…！')
        return True

    def weather(self):
        if not re.match(r'^o?tenki(yoho|yohou)?[-~!?]?$', self.Message.Body):
            return False
        self._send(u'いまのお天気は「%s」みたいですよ！' % self.__exec_weather())
        return True

    def guess(self):
        if not re.match(r'[-~!?\[(A-Za-z]{6,}$', self.Message.Body):
            return False
        hiragana = amasakas.romaji2hiragana(self.Message.Body)
        self._send(u'もしかして「%s」ですか？' % hiragana)
        return True

    def _popen(self, command):
        pipe = subprocess.PIPE
        return subprocess.Popen(command, shell=True, stdin=pipe, stdout=pipe, stderr=pipe)

    def _send(self, message):
        self.Message.Chat.SendMessage(message)

    def __exec_weather(self):
        proc = self._popen('weather')
        stdout, stderr = proc.communicate()
        return unicode(stdout.rstrip('\n'), 'utf-8')


class PrivateChat(NormalChat):

    def __init__(self, Message, Status):
        self.Oshaberisan = Oshaberisan()
        NormalChat.__init__(self, Message, Status)

    def MessageHandler(self):
        NormalChat.MessageHandler(self)
        if self.who(): return
        if self.source(): return
        if self.oshaberisan(): return
        if self.oshaberisan_log(): return

    def who(self):
        if not re.match(r'(あなた|貴方)は(だれ|誰)ですか(？|\?)?', self.Message.Body.encode('utf-8')):
            return False
        self._send(u'私はアピ=りつ子です')
        return True

    def source(self):
        if not re.match(r'(もっと)?(あなた|貴方|きみ|君|おまえ|お前|りつ子)(の(こと|亊))?(が|を)知りたい', self.Message.Body.encode('utf-8')):
            return False
        self._send(u"仕方ないですね、少しだけですよ…？\n" + self.__source_code())
        return True

    def oshaberisan(self):
        if not self.Message.Body == u'おしゃべりさん':
            return False
        self._send(self.Oshaberisan.build_count_message() + u'\nいまのところこんな感じですね')
        return True

    def oshaberisan_log(self):
        if not self.Message.Body == u'かころぐ':
            return False
        url = urlopen('http://whatismyip.akamai.com').read()
        self._send('ここにありますよ！\n' + 'http://' + url + ':4567/')
        return True

    def __source_code(self):
        fp = open(__file__)
        source_code = unicode(fp.read(), 'utf-8')
        fp.close()
        return source_code


class ShinsotsuChat(NormalChat):

    def __init__(self, Message, Status):
        self.Oshaberisan = Oshaberisan()
        NormalChat.__init__(self, Message, Status)

    def MessageHandler(self):
        self.update_oshaberisan()
        NormalChat.MessageHandler(self)
        if self.ruby(): return
        if self.talk_to_ito(): return

    def update_oshaberisan(self):
        return self.Oshaberisan.save_count(self.Message.Sender.Handle)

    def ruby(self):
        if not re.match(r'^!', self.Message.Body):
            return False
        stdout_value, stderr_value = self.__exec_ruby(self.Message.Body[1:])
        stdout_value = self.__strip_ruby_output(stdout_value)
        if len(stdout_value.strip()) != 0:
            self._send(u'結果は「%s」です' % stdout_value)
        if len(stderr_value.strip()) != 0:
            self._send(u'エラーみたいですね…')
        return True

    def talk_to_ito(self):
        if not re.match(r'ito', self.Message.Sender.Handle):
            return False
        if not re.search("(http://[A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+)", self.Message.Body):
            return False
        messages = None
        if re.search("(http://[A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+)/([A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+).jpg", self.Message.Body):
            messages = [ u'この画像は慎重に開いてくださいね' ]
        else:
            messages = [
                u'午前中のitoさんは危険なので注意してくださいね！',
                u'この URL から危険な匂いがしますよ…！',
            ]
        self._send(self.__choice(messages))
        return True

    def __choice(self, array):
        index = random.randrange(len(array))
        return array[index]

    def __exec_ruby(self, code):
        proc = self._popen('ssh ritsuko@pierrot ruby')
        return proc.communicate(code.encode('utf-8'))

    def __strip_ruby_output(self, output):
        lines = output.split('\n')
        while '' in lines:
            lines.remove('')
        if len(lines) <= 0:
            return ''
        formatted_output = lines[0]
        if len(formatted_output) > 150:
            formatted_output = formatted_output[:150] + '...'
        elif len(lines) > 2 and lines[1] != None and len(lines[1].strip()) > 0:
            formatted_output += '...'
        return formatted_output


class Appiritsuko:

    chat_names = {
        u'12新卒会議' : ShinsotsuChat,
    }

    def __init__(self):
        self.connect()

    def connect(self):
        self.skype = Skype4Py.Skype(Events=self)
        self.skype.Attach()

    ## Skype Events

    def MessageStatus(self, Message, Status):
        if Status != 'RECEIVED':
            return
        if len(Message.Chat.Members) <= 2:
            PrivateChat(Message, Status)
            return
        try:
            klass = self.chat_names[Message.Chat.Topic]
            klass(Message, Status)
        except KeyError:
            NormalChat(Message, Status)


Appiritsuko();

while True:
    time.sleep(1)
