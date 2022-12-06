#import os
#import sys
#BASE_DIR=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#sys.path.insert(0, BASE_DIR)
import json
import speech_judge
import utils

def getJudgeResult(result, answer, answer_pinyin_info=None, multipinyin=False, is_single_word=False, delimeter=None):
    p = speech_judge.Judge()
    if not answer_pinyin_info:
        pinyin_answerlist = utils.getPinyinAnswerList(answer, multipinyin, is_single_word, delimeter)
    else:
        pinyin_answerlist = utils.generatePinyinAnswerList(answer_pinyin_info)
    result_pinyin = utils.getResultPinyin(result)
    judge_res = p.getSingleJudge(pinyin_answerlist, result_pinyin)
    data = {
        'answer': answer,
        'answer_pinyin': pinyin_answerlist,
        'result': result,
        'result_pinyin': '-'.join(result_pinyin),
        'raw_judge': judge_res['judge'],
        'judge': judge_res['judge'] if judge_res['judge'] in [0, 1] else 0,
        'pinyin_distance': judge_res['min_dis'],
        'distance_threshold': p.left_thres
    }
    return json.dumps(data, indent=4, ensure_ascii=False)

def getSingleWordSpeechJudge(result, answer):
    return getJudgeResult(result, answer, answer_pinyin_info=None, multipinyin=True, is_single_word=True, delimeter=None)

def getPhraseSpeechJudge(result, answer, delimeter='，'):
    return getJudgeResult(result, answer, answer_pinyin_info=None, multipinyin=False, is_single_word=False, delimeter=delimeter)

def getMultiPinyinSpeechJudge(result, answer, pinyin, pinyin_num=0):
    answer_pinyin_info = {
        'pinyin': pinyin,
        'pinyin_num': pinyin_num
    }
    return getJudgeResult(result, answer, answer_pinyin_info=answer_pinyin_info, multipinyin=False, is_single_word=True, delimeter=None)