# coding:utf-8

# 2024/01/23 created
# python 3.10; Pymol 2.5
# @ Jun

# 注意事项
# 1. 后续使用的时候发现一个问题，pymol突变后的残基的H，amber的tleap不识别，会报例如“FATAL:  Atom .R<ALA 78>.A<1HB 11> does not have a type.”，因此该脚本进行突变完后会自动去掉该突变残基上所有氢，然后让tleap自动加氢

# TODO_global
# 2. 简单测试过了，但怎么做一个完整测试，以及如何去排除神奇操作导致的bug
# 3. 写一个序列对比互动脚本，方便检查和看
# 4. 写个对H突变的提醒
# 5. 批量突变的output要能输出一个.log
# 6. 把print内容带上颜色方便高亮，这点在sublime里应该没法测试，到时候看看vscode，以及pymol里会不会显示颜色(根据它cmd能挺多不同颜色，应该可以的)
# 7. 因为愚蠢的pymol命令栏(pymol可以用colorama，但这样需要安装，违背设计目的)和sublime的build是不能ansi转义打印出颜色的，所以warning和exit和error可以写记录然后直接print在log里，到时候方便用关键字(比如;31;)去查哪里有问题

from pymol import cmd
import sys
import os
# import argparse

# 氨基酸代号：[氨基酸简称, 氨基酸含氢个数(未脱水缩合)]
amino_acid_table = {'H':['HIS','HIP'], 'D':['ASP'], 'R':['ARG'], 'F':['PHE'], 'A':['ALA'],
                    'C':['CYS','CYM'], 'G':['GLY'], 'Q':['GLN'], 'E':['GLU','GLH'], 'K':['LYS'],
                    'L':['LEU'], 'M':['MET'], 'N':['ASN'], 'S':['SER'], 'Y':['TYR'],
                    'T':['THR'], 'I':['ILE'], 'W':['TRP'], 'P':['PRO'], 'V':['VAL'],
                    }
# E: GLU是脱质子羧基，GLH是质子化羧基

def pdb_name_process(pdb):
    # 因为不仅仅在batch_process中(batch_process中是有文件格式筛选的)，有时候会单独调用这个函数，所以依然需要做个必须是pdb的判断，否则cif的话，格式不一样。
    if os.path.splitext(pdb)[1].lower() == '.pdb':
        pdb_name = os.path.splitext(pdb)[0].split('\\')[-1]
        # 尝试下来基本确定pdb格式没有这一位，所以默认空，cif格式会有，暂时先不考虑cif格式的运行。
        gap1 = ''
        # with open(pdb, 'r') as f:
        #     data = f.readlines()
        # TODO:这个虽然很简单，但很烦，去读pdb的那一列，来决定gap2=ABCD...或者''；#反正都单链了，把这个AB直接干掉也很合适，但有没有方便的偷懒方法，不用管它的，读pdb然后判断好烦啊，还有各种解码错误又得utf8去了
        # gap2 = 'A'
        gap2 = ""
        # 分别对应selection时/pdb_name/gap1/gap2/amino`position
        # 比如'/ePro_1jpz-fix//A/Gly`46'，那么pdb_name就应该是'ePro_1jpz-fix'，gap1是''，gap2是'A'
    else:
        print('Please check the protein structure file format, this script currently could only deal ".pdb" files.')
        print('program exits with code 0')
        exit(0)
    return pdb_name, gap1, gap2


def mutation_seq_process(mutate):
    # 处理单个突变代号，比如'V78A'
    original_amino_list = amino_acid_table[mutate[0]]# 是个list
    position = mutate[1:-1]
    mutation_amion = amino_acid_table[mutate[-1]][0]# 是个string
    # 这里return的已经是大写三位字符代号，而不是单个字符的
    return original_amino_list, position, mutation_amion

def mutation(pdb_file, mutant_seq, mutation_codename, dir_path='.'):
    l_mutation = "".join(mutant_seq.split())
    l_mutation = l_mutation.split(',')
    H_number = 0

    cmd.load(pdb_file)
    print('')
    print(pdb_file)
    cmd.wizard("mutagenesis")
    cmd.refresh_wizard()
    for i in l_mutation:
        original_amino_list, position, mutation_amion = mutation_seq_process(i)
        # 由于pymol里同一种残基因为加氢情况会有不同名称，比如H可能有HIS和HIP
        for original_amino in original_amino_list:
            pdb_name, gap1, gap2 = pdb_name_process(pdb_file)
            # 比如'/FL62///GLU`358/', '/ePro_1jpz-fix//A/Gly`46'
            selection = '/' + pdb_name + '/' + gap1 + '/' + gap2 + '/' + original_amino + '`' + position + '/'
            # 留记录供检查对比selection位置是否正确
            print(selection + ' -> ' + mutation_amion)
            cmd.get_wizard().do_select(selection)
            cmd.get_wizard().set_mode(mutation_amion)
            cmd.get_wizard().apply()
            # 由于pymol加的氢代号amber不识别，tleap处理时会发生FATAL，因此可以消除突变时所加H，然后交由tleap自己加上氢
            # TODO: 做一个去H计算器，这样和tleap加氢数量如果能对上就是正确，如果不对就得手动检查
            cmd.select('resi ' + position + " and element H")
            cmd.remove('sele')
            cmd.delete('sele')
    cmd.set_wizard()
    cmd.save(dir_path + '/' + mutation_codename + '.pdb')
    cmd.delete('all')

def batch_process(dir_path):
    if not os.path.isdir(dir_path):  # 判断路径是否为文件夹
        print("Invalid directory/folder path, please check your input path.")
        print('program exits with code 0')
        exit(0)
    #输出文件直接在dir_path下，这样可以做逐步变异，比如蛋白1变异出2，在2基础上接着34567...
    else:
        pdb_dict = {}
        files = os.listdir(dir_path)
        for file in files:
            file_path = os.path.join(dir_path, file)# 获取文件的完整路径
            if os.path.isfile(file_path):# 判断路径是否为文件
                fi, fo = os.path.splitext(file_path)[0], os.path.splitext(file_path)[1]# 万一是绝对路径，需要处理出文件名
                if fo.lower() == '.pdb':
                    pdb_file = file_path
                    pdb_name = fi.split('\\')[-1]
                    pdb_dict[pdb_name] = pdb_file
                elif fo.lower() == '.txt':
                    with open(file_path, 'r') as f:
                        mutating_info = tuple(f.readlines())
                else:
                    print(file_path + ': ' + 'This file is not a ".pdb" file or mutating_info.txt.')
                    print('Attention: this script currently could only deal structure files with ".pdb".')
        for i in range(len(mutating_info)):
            work = mutating_info[i]
            work = work.replace('\n','')
            work = work.split('; ')
            pdb_file, mutant_seq, mutation_codename = pdb_dict[work[0]], work[2], work[1]
            mutation(pdb_file, mutant_seq, mutation_codename, dir_path)
            files = os.listdir(dir_path)# 因为会有新的pdb生成，所以得重新读一遍列表，以供连续逐步变异
            for file in files:
                file_path = os.path.join(dir_path, file)# 获取文件的完整路径
                if os.path.isfile(file_path):# 判断路径是否为文件
                    fi, fo = os.path.splitext(file_path)[0], os.path.splitext(file_path)[1]# 万一是绝对路径，需要处理出文件名
                    if fo.lower() == '.pdb':
                        pdb_file = file_path
                        pdb_name = fi.split('\\')[-1]
                        pdb_dict[pdb_name] = pdb_file



if __name__ == '__main__':
    # 模式选择: 批量处理或单pdb文件处理
    mode = 'batch'
    mode = 'test'

    # 批量完成空蛋白突变脚本，更多细节和使用教程请阅读README.md
    # 把脚本放置于对应文件夹下运行，或者dir_path使用绝对路径; 路径需全英文，否则pymol可能会无法识别。
    # 该脚本只会处理dir_path下的所有.pdb格式文件和mutating_info.txt文件，为了避免读取
    if mode == 'batch':
        dir_path = 'example_dir'
        batch_process(dir_path)
    # 以下是单个指定pdb文件的运行(可作为测试用)
    if mode == 'test':
        # 暂时需要修改A和''，不要忘记
        pdb_file = 'FL62.pdb'
        mutant_seq = 'A78N, S81F, V82A, T180A, L181A, V184S'
        mutation_codename = 'VII-H11'
        mutation(pdb_file, mutant_seq, mutation_codename)

if __name__ == 'pymol':
    # 用pymol命令行处理指定的某个pdb文件上的变异
    # TODO：要既能一行命令做batch，又能一行命令做单个，还能一行命令做pymol里已经打开的指定
    # 好像pymol的run命令没法加参数进去，甚至不能跑交互input，但用exec()也能一行解决，所以用exec()
    # 使用方法: 在pymol命令行中输入“cd 路径”进入脚本所在路径，然后输入“exec(open('mutation.py','r',encoding='utf-8').read(), globals(), {'a':10, 'b':20})”
    # 思考一下参数
    # {'mode':'batch'/'single'/'pymol', 'target':'dir_path'/'file_path'/'pdb_name', 'seq':'N/A'/'a1b,c2d,...'/'a1b,c2d,...', 'mutation':'N/A'/'name'/'name'}
    print('hi')

    print('a+b='+str(a+b))

    print(globals())
    exit(0)
    if mode == 'batch':
        pass

    if mode == 'single':
        pass

    if mode == 'pymol':
        pass

    # pdb, mutant_seq = sys.argv[1], sys.argv[2]
    # print(pdb, mutant_seq)
    # 写同时可以处理1. 我还没在pymol里打开pdb，直接run；还有一个是打开了我要的pdb，直接跑mutation
    #l=['V78A',...]
    #for i in l

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-g1", "--gap1", type=str, required=True, help="input the selection info, for example -g1 ''")
    # parser.add_argument("-g2", "--gap2", type=str, required=True, help="input the selection info, for example -g2 'A'")

    # args = parser.parse_args()
    # print(args.gap1, args.gap2)
    # test(args.name, args.age)

# exec()
# https://blog.51cto.com/u_16175430/8268668
# argv[]
# https://blog.csdn.net/fancynthia/article/details/126271660

# pymol
# https://pymol.org/pymol-command-ref.html#run
# https://blog.csdn.net/weixin_42486623/article/details/125093175
# http://pymol.chenzhaoqiang.com/intro/advanceManual.html

# Bash脚本批量突变蛋白并进行分子动力学模拟; 这个不清楚参考价值，没研究
# https://zhuanlan.zhihu.com/p/610552940?utm_id=0

# pdbtool; 这个不清楚参考价值，没研究
# https://github.com/harmslab/pdbtools/tree/master/pdbtools

'''
# Initialize
load yourProtein
cmd.wizard("mutagenesis")
cmd.do("refresh_wizard")

# To get an overview over the wizard API:
for i in dir(cmd.get_wizard(): print i

# lets mutate residue 104 to GLN
cmd.get_wizard().set_mode("GLN")
cmd.get_wizard().do_select("104/")

# Select the rotamer
cmd.frame(11)

# Apply the mutation
cmd.get_wizard().apply()


'''

'''
import pymol
from pymol import *
import os


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
        # 读取pdb文件
            if os.path.splitext(file)[1] == '.pdb':
                L.append(os.path.join(root , file))
        return L
# 读取本地文件夹下pdb文件（../gg/）
file_name_pdb=file_name('本地文件地址')
## 利用pymol处理本地pdb
for i in range(file_name_pdb.__len__()):
    print(i)
    # 读取本地pdb文件
    cmd.load(file_name_pdb[i]) 
    # pdb去除水分子
    cmd.remove('solvent')
    # 保存去除后的水分子
    cmd.save(file_name_pdb[i])
        # 删除当前运行，加载后续
    cmd.delete('all')
    # preset.publication(i, _self=cmd)

if __name__ == '__main__':
    print(1)
    pdb_file = ''
    mode = 'single'# single or batch
'''