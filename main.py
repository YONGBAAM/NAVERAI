import os
from prepare import make_indexing, make_word_list, make_clip
import smipy as smipy
import pandas as pd

#################################################
#
#   구현한 함수들을 실제 사용하는 예제
#   smiparser에서 파싱하는 함수,
#   우리가 필요한 단어만 뽑는 함수를 실제 이용함
#
###################################################
bb = './bigbang'
Encoding = 'cp949'

smilist = [name for name in os.listdir(bb) if name.split('.')[-1] == 'smi']

# for n in smilist:
#     smi = smipy.Smi(os.path.join(bb, n ), debug = False)
#     smi.to_csv(title = n, output_path= bb, all= True)
#
# make_indexing(smilist, movie_dir=bb, output_name='bigbang', verbose = False)



df = pd.read_csv(os.path.join(bb, 'bigbang.csv'), encoding = Encoding)

originals = ['_','end', 'wonder' ]
ori_to_der = {
    '_' : ['_'],
    'end' : ['end', 'ended'],
              'wonder' : ['wonder', 'wondered']
}

make_word_list(originals, ori_to_der, 'bigbang.csv', 'wordlist_raw')

make_clip('wordlist_mod.csv', title = 'clips_db', pad = 1000)