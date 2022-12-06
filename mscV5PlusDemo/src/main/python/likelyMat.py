import os
import xlrd

class likelyMat:
    def __init__(self):
        self.mat = {
            'sheng': {
                'b':{}, 'p':{}, 'm':{}, 'f':{}, 'd':{}, 't':{},
                'n':{}, 'l':{}, 'g':{}, 'k':{}, 'h':{}, 'j':{},
                'q':{}, 'x':{}, 'r':{}, 'z':{}, 'c':{}, 's':{},
                'y':{}, 'w':{}, 'zh':{}, 'ch':{}, 'sh':{}
            },
            'yun':{
                'a':{}, 'e':{}, 'i':{}, 'o':{}, 'u':{}, 'v':{},
                'ai':{}, 'ao':{}, 'an':{}, 'ang':{},
                'ou':{}, 'ong':{},
                'ei':{}, 'er':{}, 'en':{}, 'eng':{},
                'iu':{}, 'ie':{}, 'in':{}, 'ing':{}, 'ia':{}, 'iao':{}, 'ian':{}, 'iang':{}, 'iong':{},
                'ui':{}, 'un':{}, 'ua':{}, 'uai':{}, 'uan':{}, 'uang':{}, 'uo':{}, 'ue':{}, 'vn': {}, 'van': {}
            }
        }

    def getMat(self, filename, matType='sheng'):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        wb = xlrd.open_workbook(filepath)
        sh = wb.sheet_by_name('Sheet1')
        for i in range(1, sh.nrows):
            for j in range(1, sh.ncols):
                x = sh.cell(i, 0).value
                y = sh.cell(0, j).value
                if sh.cell(i, j).value == '':
                    self.mat[matType][x][y] = 1
                else:
                    self.mat[matType][x][y] = sh.cell(i, j).value

        return self.mat[matType]

if __name__ == '__main__':
    p = likelyMat()
    print(p.getMat('mat_sheng.xlsx', 'sheng'))
    print(p.getMat('mat_yun.xlsx', 'yun'))

