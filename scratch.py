import pandas as pd
import os

from smipy import Smi
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
#ffmpeg_extract_subclip("video1.mp4", start_time, end_time, targetname="test.mp4")


TESTL = 10

verbose = False

#######################################
#
#
#   처음 인덱싱할때 나머지정보 모두 추가할것
#   인덱싱 df 여러개 합쳐서 만들것
#   일단 이함수는 지금 빨리 해놔야함!  그래야 나중 노가다할때 편함.
#   코드네임 BB101 같은것도 생각해서 구현!
#
#
#
#######################################


smi1 = Smi('./bigbang/BB501.smi')
ret_text = smi1.export(start_time=1930, end_time=10000)
# if verbose:
#     sub = smi1.subtitles
#     for ind in range(min(TESTL, len(sub))):
#         print('{}th sub : {}~{}'.format(ind, sub[ind].start, sub[ind].end))
#         for lang in sub[ind].langs:
#             print('{} : {}'.format(lang, sub[ind].content[lang]))
#
#     print('upper displayed sample smi ')

with open('./bigbang/testout.smi', 'w') as f:
    f.write(ret_text)






eng_title_signal = ['ENCC', 'EnglishSC']

#자막인덱싱

#final_result.append(dict(
#   'base' = 'eat',
#   'derivative' = 'eating',
#   'code' = B101 #빅뱅시즌1-01
#   'sent_kor' = '먹어요 요거트를' #없으면 논
#   'sent_eng' = 'eating yogurt'
# ))
#
# def is_contain(word, sent_list):
#     contain = False
#     for sent in sent_list:
#         if word == sent:
#             contain = True
#     return contain
# #kor_list = [] # Korean list는 해도 쓸모없을듯
#
# nohan = re.compile('[a-zA-Z\'\"\s]+')
#
# sminame = 'bigsub (1).smi'
# smi3 = Smi(os.path.join('./', sminame))
#
# for smi in [smi3]:
#     eng_sig = None
#     indexing_result = []  # pd dataframe용
#     for ind, sub in enumerate(smi.subtitles):
#         if eng_sig is None:
#             #Deciding english signal flag
#             for _sig in eng_title_signal:
#                 if _sig.lower() in [k.lower() for k in sub.content.keys()]:
#                     eng_sig = _sig
#
#         eng_sentence = sub.content.get(eng_sig, None)
#         start_time = sub.start
#         end_time = sub.end
#
#
#         #eng_tokens랑 eng_sentence랑 노상관으로 할것
#         #분리는 해야겠다.
#         if eng_sentence is not None and 'nbsp' not in eng_sentence:
#             #only english should appear
#             eng_sentence = ''.join(nohan.findall(eng_sentence))
#             #eng_simple은 내가 찾고싶은 단어만 있게
#             eng_sentence_tokens = eng_sentence.lower().strip()
#
#             #고유명사제거 case insensetive replace?
#             for proper_noun in ['Cheesecake Factory', 'Big Bang Theory']:
#                 if proper_noun.lower() in eng_sentence_tokens:
#                     print(proper_noun.lower())
#                     print(eng_sentence_tokens)
#                     eng_sentence_tokens = eng_sentence_tokens.replace(proper_noun.lower(), '')
#
#             sent_list = eng_sentence_tokens.split(' ')
#             for word in sent_list:
#                 if word.lower() not in ['a', 'an', 'the']:
#                     indexing_result.append(dict(
#                         word=word, ind=ind, eng_sentence=eng_sentence, videoname = sminame,
#                         start = start_time, end = end_time
#                     ))
#
#     df = pd.DataFrame(indexing_result)
#     df.to_csv('testcsv2.csv')







    # # for token in derivatives:
    # #     if is_contain(token, sent_list):
    #
    #
    #
    #
    #     engtitles = [sub.content.get(sig, None) for sig in eng_title_signal]
    #     for title in engtitles:
    #         if title is not None:
    #             sentence_list = title.split[' ']
    #             for word in derivatives:



# originals = ['laugh', 'eat', 'alike']
# ori_to_der = {
#     'laugh' : ['laughs', 'laugh'],
#     'eat' : ['eating', 'ate', 'eat'],
#     'alike' : ['alike']
# }
#
# ori_to_index = {}
# for index, original in enumerate(originals):
#     ori_to_index[original] = index
#
# der_to_index = {}
# #알고리즘변경!
# for index, original in enumerate(originals):
#     ders = ori_to_der[original]
#     for der in ders:
#         der_to_index[der] = index
#
# derivative_to_word = {}
# derivatives = []
#
# for k,v in ori_to_der.items():
#     for der in v:
#         derivatives.append(der)
#         derivative_to_word[der] = k
#
#
# res_list = []
# for csvname in ['./smi/testbig.csv']:
#     df = pd.read_csv(os.path.join('./', csvname))
#     for derivative in derivatives:
#         df_sel = df[df['word'] == derivative]
#         original = derivative_to_word[derivative]
#         word_index = der_to_index[der]
#         # df구조
#         # dict(word=word, ind=ind, eng_sentence=eng_sentence,
#         #     videoname=''.join(sminame.split('.')[:-1]),
#         #     start=start_time, end=end_time, tokens=' '.join(token_list))
#
#         for _i in range(len(df_sel)):
#             row = df_sel.iloc[_i]
#             d = dict(row)
#
#             d['word_index'] = der_to_index[derivative]
#             print(d)
#             res_list.append(d)
#     df = pd.DataFrame.from_dict(res_list)
#
#
# for ind, word in enumerate(originals):
#     df_i = df[df['word_index'] == ind]
#     no_occur = len(df_i)
#     print('word {} : {}'.format(word, no_occur))
