import re
import os
import codecs
import codecs
import pandas as pd
import prepare

SMI_PADDING = 60000

class Smi:
    def __init__(self, filepath = None, **kwargs):
        self.eng_signal = None
        self.kor_signal = None
        self.raw_text = ''
        self.subtitles = []#dict(start=timestamp, end=None, kor='', eng=text)
        self._korsub = []
        self._engsub = []
        self.sinc_verification = False


        if filepath is not None:
            self.load(filepath = filepath, **kwargs)

    def load(self, filepath, eng_signal = None, kor_signal = None, encoding = None, debug = False):
        ####    Loading raw text
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

        # Detecting smi information
        # Detecting signal for sinc verification
        #주석 <!--~-->
        re_comment = re.compile('<!--\n+(.+)\n+-->')
        re_sinc = re.compile('sinc =(.+)')
        cms = re_comment.findall(self.raw_text)
        if cms is not None:
            for cm in cms:
                if 'true' in re_sinc.findall(cm)[0].lower():
                    self.sinc_verification = True

        # Detect Korean / English key
        re_sig = re.compile('Class=(.*)>')
        signals = set(re_sig.findall(self.raw_text))
        for sig in signals:
            if eng_signal is None:
                if 'english' in sig.lower():
                    self.eng_signal = sig
                elif 'en' in sig.lower():
                    self.eng_signal = sig
            if kor_signal is None:
                if 'korean' in sig.lower():
                    self.kor_signal = sig

                elif 'kr' in sig.lower():
                    self.kor_signal = sig

        # 시그널 2개가 아닐경우 예외 처리

        # Greedy compile
        re_line = re.compile('<SYNC Start=([0-9]+)><P Class=(\w+)>\n?(.*)\n')
        #패턴 : <SYNC Start=(1258654)><P Class=EnglishSC> 하고 (문자1이상) + \n<, greedy compile

        lines = re_line.findall(self.raw_text)

        if debug == True:
            re_line2 = re.compile('<SYNC Start=[0-9]+><P Class=\w+>\n?.*\n')
            lines2 = re_line2.findall(self.raw_text)
            print(''.join(lines2[:50]))

        #한글 영어 따로해서 합치자
        eng_buffer = None
        kor_buffer = None
        for line in lines:

            timestamp, channel, text = line
            timestamp = int(timestamp)

            if channel == self.eng_signal:
                if eng_buffer is None:
                    if not 'nbsp' in text:
                        text = prepare.to_sentence(text)
                        eng_buffer = dict(start=timestamp, end=None, kor='', eng=text)
                else:
                    eng_buffer['end'] = timestamp
                    self._engsub.append(eng_buffer)
                    if 'nbsp' in text:
                        eng_buffer = None
                    else:
                        text = prepare.to_sentence(text)
                        eng_buffer = dict(start=timestamp, end=None, kor='', eng=text)

            if channel == self.kor_signal:
                if kor_buffer is None:
                    if not 'nbsp' in text:
                        text = prepare.to_sentence(text)
                        kor_buffer = dict(start=timestamp, end=None, kor=text, eng='')
                else:
                    kor_buffer['end'] = timestamp
                    self._korsub.append(kor_buffer)
                    if 'nbsp' in text:
                        kor_buffer = None
                    else:
                        text = prepare.to_sentence(text)
                        kor_buffer = dict(start=timestamp, end=None, kor=text, eng='')
        #끝날때는
        if len(self._korsub) >0:
            self._korsub[-1]['end'] = self._korsub[-1]['start'] + SMI_PADDING
        if len(self._engsub) >0:
            self._engsub[-1]['end'] = self._engsub[-1]['start'] + SMI_PADDING

        #두 채널 합치기
        if len(self._engsub) ==0:
            for s in self._korsub:
                self.subtitles.append(s)

        it_kor = iter(self._korsub)
        i_k = 0
        korlen = len(self._korsub)
        for engsub in self._engsub:
            #한글자막 끝났으면 영어자막만 추가
            if i_k == korlen:
                self.subtitles.append(engsub)
            #뒤지는 한글자막은 다 추가
            else:
                while i_k < korlen and self._korsub[i_k]['start'] < engsub['start']:
                    self.subtitles.append(self._korsub[i_k])
                    i_k += 1
                    if i_k == korlen: break

                if i_k < korlen and engsub['start'] == self._korsub[i_k]['start']:
                    s = engsub.copy()
                    s['kor'] = self._korsub[i_k]['kor']
                    self.subtitles.append(s)
                    i_k +=1

    def to_csv(self, title ,output_path = './', all = False, encoding = 'EUC-KR'):
        subdf = pd.DataFrame.from_dict(self.subtitles)
        sub_path = prepare.get_save_path(output_path, title, format ='.csv')
        print('Saving to {}'.format(sub_path))
        subdf.to_csv(sub_path, encoding=encoding)
        if all:
            kordf = pd.DataFrame.from_dict(self._korsub)
            kor_path = prepare.get_save_path(output_path, title + '_k', format='.csv')
            print('Saving to {}'.format(kor_path))
            kordf.to_csv(kor_path, encoding=encoding)

            engdf = pd.DataFrame.from_dict(self._engsub)
            eng_path = prepare.get_save_path(output_path, title + '_e', format='.csv')
            print('Saving to {}'.format(eng_path))
            engdf.to_csv(eng_path, encoding=encoding)

    def slice(self, start_time, end_time, slice_only = False):
        sent_list = []
        ind_list = []

        for ind, sent in enumerate(self.subtitles):
            if sent['start'] > start_time and sent['end'] < end_time:
                sent_list.append(sent)
                ind_list.append(ind)
        if slice_only:
            return sent_list
        else:
            return sent_list, ind_list


    def export(self, start_time = None, end_time = None, slice_manual = None):
        textlist = ['<SAMI>', '<BODY>']
        if slice_manual is not None:
            sentences = slice_manual
        else:
            sentences = [sent for sent in self.subtitles if sent['start'] >start_time and sent['end'] <end_time]


        engsig_out = 'EnglishSC'
        korsig_out = 'KoreanSC'
        for sent in sentences:
            if len(sent['kor']) >= 1:
                textlist.append('<SYNC Start={}><P Class={}>\n{}'.format(
                    sent['start'] - start_time, korsig_out, sent['kor']))

            if len(sent['eng']) >=1:
                textlist.append('<SYNC Start={}><P Class={}>\n{}'.format(
                    sent['start'] - start_time, engsig_out, sent['eng']))

            if len(sent['kor']) >= 1:
                textlist.append('<SYNC Start={}><P Class={}>\n{}'.format(
                    sent['end'] - start_time, korsig_out, '&nbsp;'))

            if len(sent['eng']) >=1:
                textlist.append('<SYNC Start={}><P Class={}>\n{}'.format(
                    sent['end'] - start_time, engsig_out, '&nbsp;'))


        textlist.append('</BODY>')
        textlist.append('</SAMI>')
        return '\n'.join(textlist)

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





