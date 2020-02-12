#후에 제공할 것
단어 리스트와 단어-파생형 쌍 딕셔너리
바로 만들어서 제출하겠음
딕셔너리형 변수의 경우 df로 만들기가 어려우므로
단어 리스트와 단어-파생형 쌍 딕셔너리는
pickle object로도 제공

#기본사항
csv파일은 pd.Dataframe.to_csv로 제작하였으며
**중요**encoding은 cp949
리눅스에서는 utf-8이 기본 인코딩
윈도우는 cp949나 euc-kr이 기본 인코딩


# clips_db 설명
이 파일은 앱 내에 존재하는 db역할을 하도록 만들어졌음.
Api 제작 시에도 이 파일을 참고해서 만들 수 있음.
필요한 데이터는 모두 이 파일에 넣어놨음. 기타 필요한 데이터가 있다면 문의할 것!

-column 값 설명
첫칼럼(빈칸) : 무시하셈
word_ind : word의 인덱스, 1부터 시작, 자세한건 word_list 참조
clip_code : 해당 클립 자막의 이름
	만드는 방식은 1(word_ind 3자리)(subindex 3자리) 
eng_sent : english sentence
kor_sent : korean sentence
sent_start[end] : 해당 클립에서 몇 ms 후에 eng_sent가 시작하는지[끝나는지]
word_loc : 문장에서 몇번째 단어에 어휘가 나오는지, 어휘 구분은 스페이스바' ' (-1은 자동감지 안된 것)
line_loc : whole_eng에서 몇번째 문장에서 해당 eng_sent가 나오는지, 문장구분은 '\n'
whole_eng : 해당 클립 전체 스크립트
whole_kor : 해당 클립 전체 스크립트 한글본
_로 시작하는 변수는 디버그용, 무시할 것!