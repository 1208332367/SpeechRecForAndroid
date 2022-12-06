import re
import likelyMat

class Judge:
    def __init__(self):
        mat = likelyMat.likelyMat()
        self.sheng = mat.getMat('mat_sheng.xlsx', 'sheng')
        self.yun = mat.getMat('mat_yun.xlsx', 'yun')
        self.left_thres = 0.5
        self.right_thres = 0.5


    def getSingleJudge(self, pinyinAnswerList, pinyin):
        res = {'nearest': None, 'min_dis': None, 'need_human': None, 'judge': -1}
        finalList = []
        min = 999999

        if not pinyin:
            return res

        if not re.search('[a-zA-Z0-9]', str(pinyin)):
            return res
        if '' in pinyin:
            pinyin.remove('')
        len2 = len(pinyin)

        for pinyinAnswer in pinyinAnswerList:
            standardList = pinyinAnswer.strip().split('-')
            if '' in standardList:
                standardList.remove('')
            len1 = len(standardList)

            if len1 > len2 or len1 == 0 or len2 == 0:
                continue
            for i in range(0, len2 - len1 + 1):
                score = self.complexCompare(standardList, pinyin[i: i + len1])
                if score < min:
                    min = score
                    finalList = pinyin[i: i + len1]

        res['nearest'] = finalList   #拼音最近匹配
        res['min_dis'] = min         #最小编辑距离均值

        judge = self.judgeByTwoDis(min)
        res['need_human'] = judge['need_human']
        res['judge'] = judge['judge']

        return res


    def judgeByTwoDis(self, dis):
        res = {}
        if dis == 0:
            res['judge'] = 1
            res['need_human'] = 0
            return res
        if dis < self.left_thres:
            res['judge'] = 1
            res['need_human'] = 0
            return res
        if dis >= self.right_thres:
            res['judge'] = 0
            res['need_human'] = 0
            return res
        res['judge'] = -1
        res['need_human'] = 1

        return res


    #距离分为声母、韵母，分别求 权值 * 编辑距离
    def complexCompare(self, list1, list2):
        score = 0
        num_weight = 0
        num_distance = 0
        sheng_weight = 4 # param to modified
        yun_weight = 4   # param to modified

        for i in range(0, len(list1)):
            pinyin1 = list1[i]
            pinyin2 = list2[i]
            pinyin1_with_num = re.search('[0-9]', str(pinyin1))
            pinyin2_with_num = re.search('[0-9]', str(pinyin2))
            pure_pinyin1 = pinyin1
            pure_pinyin2 = pinyin2
            if pinyin1_with_num:
                pure_pinyin1 = pinyin1[:-1]
            if pinyin2_with_num:
                pure_pinyin2 = pinyin2[:-1]
            if pinyin1_with_num and pinyin2_with_num:
                num_weight = 2 # param to modified
                num1 = pinyin1[-1]
                num2 = pinyin2[-1]
                if num1 == num2: # 如果音调相同，则音调距离为0
                    num_distance = 0
                else:
                    num_distance = 1
            res1 = self.dividePinyin(pure_pinyin1)
            res2 = self.dividePinyin(pure_pinyin2)

            if res1['sheng'] == '' or res2['sheng'] == '':
                disSheng = 1 # Levenshtein.distance(res1['sheng'], res2['sheng'])
            else:
                disSheng = self.sheng[res1['sheng']][res2['sheng']] # 2022/09/06 cancel multiple Levenshtein.distance(res1['sheng'], res2['sheng'])
            disYun = self.yun[res1['yun']][res2['yun']] # 2022/09/06 cancel multiple Levenshtein.distance(res1['yun'], res2['yun'])

            # 2022/09/06 update distance calculation
            total_rate = sheng_weight + yun_weight + num_weight
            score = score + (sheng_weight * disSheng + yun_weight * disYun + num_weight * num_distance) / total_rate
        return score / len(list1)


    #寻找拼音中的第一个元音字母（包括v）
    def getFirstYuanyinPos(self, pinyin):
        yuanyinList = ['a', 'e', 'i', 'o', 'u', 'v']
        for i in range(0, len(pinyin)):
            ch = pinyin[i]
            if ch in yuanyinList:
                return i
        return -1


    #分离拼音的声母和韵母
    def dividePinyin(self, pinyin):
        res = {'sheng': '', 'yun': ''}
        pos = self.getFirstYuanyinPos(pinyin)
        if pos < 0:
            return res
        if pos == 0:
            res['sheng'] = ''
        else:
            res['sheng'] = pinyin[0: pos]
        res['yun'] = pinyin[pos: len(pinyin)]
        return res