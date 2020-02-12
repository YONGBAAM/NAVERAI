# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

import os
import re
import codecs
import subprocess


def _ms_to_stamp(ms):
    try:
        ms = int(ms)
    except:
        ms = 0
    s = int(ms / 1000)
    ms = ms % 1000
    m = int(s / 60) % 60
    h = int(s / 3600)
    s = s % 60
    return "%02d:%02d:%02d.%03d" % (h, m, s, ms)


def _tplit(s, tag):
    delimiter = '<' + tag
    try:
        return [(delimiter + item).strip().replace('\n', ' ') for item in re.split(delimiter, s, flags=re.I)][1:]
    except:
        return []


def _lookup(s, pattern):
    return re.search(pattern, s, flags=re.I)


def _plang(item):
    lang = _lookup(item, '<p(.+)class=([a-z]+)').group(2)
    content = item[_lookup(item, '<p(.+)>').end():]
    content = content.replace('\n', '')
    content = re.sub('<br ?/?>', '\n', content, flags=re.I)
    content = re.sub('<.*?>', '', content)
    content = content.strip()
    return [lang, content]


class SamitizeError(Exception):

    messages = (
        "Cannot access to the input file.",
        "Cannot find correct encoding for the input file.",
        "Cannot parse the input file. It seems not to be a valid SAMI file.\n(Verbose option may show you the position the error occured in)",
        "Cannot convert into the specified format. (Suppored formats : vtt, plain)",
        "Unknown error occured."
    )

    def __init__(self, code):
        try:
            code = int(code)
            if code > -1 or code < -5:
                code = -5
        except:
            code = -5
        self.code = code
        self.message = self.messages[-(code + 1)]

    def __repr__(self):
        return "{} ({})".format(self.message, self.code)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__str__()


class Subtitle:

    def __init__(self, content, start, end=0):
        self.content = content
        self.start = start
        self.end = end
        self.langs = list(self.content.keys())
        self.candidate_key = self.langs[0] if len(self.langs) else None
        self.representative = self.content[self.candidate_key] if self.candidate_key else ""

    def is_valid(self, lang):
        return lang in self.content and self.content[lang] != '&nbsp;'

    def format_to(self, target, lang='ENCC'):
        if lang not in self.content:
            return self.summary()
        if target == 'vtt':
            return "{} --> {}\n{}".format(_ms_to_stamp(self.start), _ms_to_stamp(self.end), self.content[lang])
        elif target == 'plain':
            return "{}".format(self.content[lang])
        return self.summary()

    def summary(self):
        text = "[{}:{}] {}".format(self.start, self.end, self.representative)
        try:
            return text.encode('utf-8')
        except:
            return text

    def __repr__(self):
        return self.summary()

    def __str__(self):
        return self.summary()

    def __unicode__(self):
        return self.summary()


class Smi:

    PADDING = 60000

    def __init__(self, filepath, encoding=None):
        self.raw_text = ""
        self.subtitles = []

        self.languages = set([])

        if not os.path.isfile(filepath):
            raise SamitizeError(-1)

        if encoding:
            try:
                file = codecs.open(filepath, encoding=encoding)
                self.raw_text = file.read()
                file.close()
            except:
                raise SamitizeError(-2)
        else:
            # detector = ['/usr/bin/env', 'uchardet', filepath]
            # encoding_detected = subprocess.check_output(detector).decode('utf-8').strip().lower()
            try:
                file = codecs.open(filepath, encoding='EUC-KR')
                self.raw_text = file.read()
                file.close()
            except:
                try:
                    file = codecs.open(filepath, encoding='cp949')
                    self.raw_text = file.read()
                    file.close()
                except:
                    try:
                        file = codecs.open(filepath, encoding='UTF-8')
                        self.raw_text = file.read()
                        file.close()
                    except:
                        raise SamitizeError(-2)
        self.raw_text = self.raw_text.replace('\r\n', '\n')
        self.raw_text = self.raw_text.replace('\n\r', '\n')

        initial = True
        for item in _tplit(self.raw_text, 'sync'):
            timecode = int(_lookup(item, '<sync start=([0-9]+)').group(1))
            content = dict(map(_plang, _tplit(item, 'p'))) #'EnglishSc' : '&nbsp' 이렇게

            #검사 후 버퍼를 저장할것인지 결정
            #저장하기 전에 할당
            if initial:
                sub_buffer = Subtitle(content, start=timecode)
            else:
                if not timecode == sub_buffer.start:
                    sub_buffer.end = timecode
                    for lang in sub_buffer.content.keys():
                        self.languages.add(lang)
                    self.subtitles.append(sub_buffer)
                    sub_buffer = Subtitle(content, start=timecode)
                else:
                    #시작시간이 같으면 넘기기
                    before_content = sub_buffer.content
                    for k,v in content.items():
                        before_content[k] = v
                    sub_buffer = Subtitle(before_content, start = timecode)

            initial = False

        #마지막 버퍼 넣기
        sub_buffer.end = sub_buffer.start + self.PADDING
        for lang in sub_buffer.content.keys():
            self.languages.add(lang)
        self.subtitles.append(sub_buffer)

    def convert(self, target, lang='ENCC'):
        results = []
        if target == 'vtt':
            results.append("WEBVTT")
            index = 1
            for subtitle in self.subtitles:
                if subtitle.is_valid(lang):
                    results.append("{}\n{}".format(index, subtitle.format_to(target, lang)))
                    index += 1
            result = "\n\n".join(results)
        elif target == 'plain':
            for subtitle in self.subtitles:
                if subtitle.is_valid(lang):
                    results.append(subtitle.format_to(target, lang))
            result = "\n".join(results)
        else:
            raise SamitizeError(-4)
        return result if result[-1] == "\n" else result + "\n"

    #time은 ms단위로
    def export(self, start_time, end_time ):
        textlist = ['<SAMI>', '<BODY>']
        sentences = []
        for sent in self.subtitles:
            if sent.start >start_time and sent.end <end_time:
                sentences.append(sent)

        eng_signal = 'EnglishSC'
        for sent in sentences:
            if eng_signal in sent.content.keys():
                textlist.append('<SYNC Start={}><P Class={}>\n{}'.format(sent.start - start_time,eng_signal, sent.content[eng_signal]))
        textlist.append('</BODY>')
        textlist.append('</SAMI>')
        return '\n'.join(textlist)