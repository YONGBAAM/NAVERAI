import pandas as pd
import os

from naverapi import slice_video, get_audio, stt

'''
이건 main함수같이 따로 def 안하고 모든걸 여기서!!


'''

if True:
    #video_names = slice_video('BB501.mkv', './stt')
    video_names = [_n for _n in os.listdir('./stt') if _n[-4:] == '.mkv' and '_' in _n]

    for n in video_names:
        get_audio(n, './stt')
    for n in video_names:
        audioname = ''.join(n.split('.')[:-1]) + '.mp3'
        stt(audioname, './stt')


    # clip = VideoFileClip(os.path.join('./stt', 'BB501.mkv'))
    # author = 'YB'#clip.duration = 1292.74
    # csv_loc = './translate'
    # csvnames = ['testbb501.csv']
    #
    # for csvname in csvnames:
    #     df = pd.read_csv(os.path.join(csv_loc, csvname), encoding=CSV_ENCODING)
    #     engsubs = ['{}'.format(str) for str in list(df['eng']) if type(str) == type('line')][:100]
    #     engsubs = '\n'.join(engsubs)
    #
    #     # get data
    #     kortexts = papago_translate(engsubs, verbose = True)
    #     korsubs = kortexts.split('\\n')
    #
    #     korsubs = pd.Series(korsubs)
    #     df.insert(loc=5, column='kor_trans', value=korsubs)
    #
    #     save_path = get_save_path(dir = csv_loc, name = csvname.split('.')[0] + '_t', format='csv', replace = False)
    #
    #
    #     df.to_csv(save_path, encoding=CSV_ENCODING)

# if __name__ == '__main__':
#     author = 'YB'
    # csv_loc = './translate'
    # csvnames = ['testbb501.csv']
    #
    # for csvname in csvnames:
    #     df = pd.read_csv(os.path.join(csv_loc, csvname), encoding=CSV_ENCODING)
    #     engsubs = ['{}'.format(str) for str in list(df['eng']) if type(str) == type('line')][:100]
    #     engsubs = '\n'.join(engsubs)
    #
    #     # get data
    #     kortexts = papago_translate(engsubs, verbose = True)
    #     korsubs = kortexts.split('\\n')
    #
    #     korsubs = pd.Series(korsubs)
    #     df.insert(loc=5, column='kor_trans', value=korsubs)
    #
    #     save_path = get_save_path(dir = csv_loc, name = csvname.split('.')[0] + '_t', format='csv', replace = False)
    #
    #
    #     df.to_csv(save_path, encoding=CSV_ENCODING)