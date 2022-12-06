import pypinyin

punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！【】（）、。：；’‘……￥·"""
dicts = {i:'' for i in punctuation}
punc_table = str.maketrans(dicts)

def word2pinyin_list(word, multi_mode=False, is_single_word=False, is_recognize=True):
    if word == 'error':
        return word
    pinyin_str = pypinyin.slug(word, heteronym=multi_mode, style=pypinyin.Style.TONE3, separator='-', errors='default', strict=True)
    if is_single_word or is_recognize:
        return pinyin_str.split('-') # list for recognize: ['zhe4', 'shi4', 'ya2', 'chi3'], list for single_word_answer ['le4', 'yue4']
    else:
        return pinyin_str # string for answer phrase: 'ya2-chi3'

def getResultPinyin(result):
    return word2pinyin_list(result.translate(punc_table), multi_mode=False, is_single_word=False, is_recognize=True)

def getPinyinAnswerList(answer, multi_mode=True, is_single_word=False, delimeter=None):
    if is_single_word:
        return word2pinyin_list(answer, multi_mode=multi_mode, is_single_word=True, is_recognize=False)
    else:
        res = []
        answer_list = answer.split(delimeter)
        for current_ans in answer_list:
            res.append(word2pinyin_list(current_ans, multi_mode=multi_mode, is_single_word=False, is_recognize=False))
        return res

def generatePinyinAnswerList(answer_pinyin_info):
    pinyin = answer_pinyin_info['pinyin']
    pinyin_num = str(answer_pinyin_info['pinyin_num'])
    return [pinyin + pinyin_num]