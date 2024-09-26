import os
import sys
from tqdm import trange
import pickle
import re
from datetime import datetime

def dockedata_extract(directory_path, mode='batch'):
    # TODO: PubMed 用的cid，但如果其他database来的数据就又得改了，到时候看看怎么改写; 提取名字那步另写一个函数
    # {'cid':['cid', Scoring function, Grid center, Grid size, Grid space, Random seed, {mode1:[score, RMSD1, RMSD2]}]}
    if mode == 'single':
        dic = {}
        # TODO: 加一个检查是否是文件还是文件夹路径
        with (directory_path, 'r') as f:
            data = f.read()
        pass
    if mode == 'batch':
        dic = {}
        temp = {}
        for step in trange(len(os.listdir(directory_path))):
            i = os.listdir(directory_path)[step]
            fname = i.split(".")[0]
            cid = re.findall(r'\d+', fname)
            if len(cid) != 1:
                report = 'Multiple possible id in filename, please check this file: "' + i + '".\n'
                print(report)
                with open('dockedata_extract-error.log', 'w') as f:
                    f.write(report)
                sys.exit(1)
            with open(directory_path + '/' + i, 'r') as f:
                data = f.read()
            scoref = 'Scoring function : '
            rept = 'receptor: '
            gridce = 'Grid center: '
            gridse = 'Grid size  : '
            gridsp = 'Grid space : '
            randsd = 'random seed:'
            out = r'-----\+------------\+----------\+----------\n'
            end = '\n'
            # end2 = '...'
            pattern = rf"{scoref}(.*?){end}|{rept}(.*?){end}|{gridce}(.*?){end}|{gridse}(.*?){end}|{gridsp}(.*?){end}|{randsd}\s*(-?\d+)|{out}\s*(.*)"
            matches = re.findall(pattern, data, re.DOTALL)
            out_dic = {}
            work_list = []
            work_list.append(cid[0])
            # attention that adding more patterns will change the order
            for match in matches:
                if match[0]:
                    # scoring function
                    work_list.append(match[0])
                elif match[1]:
                    # receptor
                    work_list.append(match[1])
                elif match[2]:
                    # grid center
                    work_list.append(match[2])
                elif match[3]:
                    # grid size
                    work_list.append(match[3])
                elif match[4]:
                    # grid space
                    work_list.append(match[4])
                elif match[5]:
                    # random seed
                    work_list.append(match[5])
                elif match[6]:
                    # docking result
                    dk = match[6].split('\n')
                    dk_dic = {}
                    for i in dk:
                        i = i.split()
                        if i:
                            mode = i.pop(0)
                            dk_dic[mode] = i
                    work_list.append(dk_dic)
            dic[cid[0]] = work_list
            # TODO: 临时提取每个的第一个分数，以后写完善
            temp[cid[0]] = dk_dic['1'][0]
        with open('temp', 'w') as f:
            f.write(str(temp))
    return dic

def pickle3_write(dic, optional_name=''):
    if optional_name == '':
        print('')
        print(str(len(dic)) + ' data are extracted.')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"extracted_DockingData_{timestamp}.pickle"
        with open(filename,'wb') as f:
            pickle.dump(dic, f)
        with open('log.txt', 'w') as f:
            f.write(str(dic))
        print('Writing to pickle.')
    else:
        print('')
        print(str(len(dic)) + ' data are extracted.')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = optional_name + f"_{timestamp}.pickle"
        with open(filename,'wb') as f:
            pickle.dump(dic, f)
        with open('log.txt', 'w') as f:
            f.write(str(dic))
        print('Writing to pickle.')

def PubMedinfo_extract(csv, title):
    pass

if __name__ == '__main__':
    log_dir = "./outputlog/" # autodock result files path
    extract_mode = 'batch' # 'batch' or 'single'
    info_csv = './PubChem_compound_smiles_similarity_3d_O=[N+]([O-])OCCCO-3DAll1302.csv'
    PubMed_title = ('cid', 'cmpdname', 'isosmiles', )
    pickle3_write(dockedata_extract(log_dir, extract_mode))
    PubMedinfo_extract(info_csv, PubMed_title)







# 先做一个整表csv: id, 小分子名字, SMILES, score1~n
# tit = 'cid, cmpdname, isosmiles, '
# score_top = 10
# w = ''
# for i in range(score_top):
#     w = w + 'Score_' + str(i+1) + ', '
# title = tit + w

# 做两种排序方式