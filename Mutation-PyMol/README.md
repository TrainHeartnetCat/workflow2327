批量突变脚本



load 文件路径

注意这弱智东西就只检查后缀，比如我把readme.md改成.pdb，它也不会报错，直接load readme.md会报Error: unsupported file type: md



wizard-mutagensis

PyMOL>cmd.get_wizard().do_select('/FL62///GLU`358/')

注意这个弱智东西如果名字不对也是会成功selected，只是选不出东西

比如cmd.get_wizard().do_select('/FL62///E`358/')，把GLU改成对应代号E，它是选不到的，也不会报错

再离谱点cmd.get_wizard().do_select('/FL62///ALA`358/')，把GLU改成错误的，同样如此

仅仅是个字符串识别处理，没有任何保护措施，所以要注意大小写问题





路径里不能中文

将脚本文件放置于pymol当前路径

pymol当前路径可用pwd查看，一般默认个人文件夹位置比如(C:\Users\TrainHeartnetCat\Documents)

或者cd进入脚本所在目录，我肯定喜欢这样



做两种脚本吧，一种可以pymol直接跑，直接命令栏里run a.py b.pdb c.txt就行；另一种if name==main，不知道能不能合在一起

可以的 name==pymol就行，

两种用法





![image-20240124181258892](C:/Users/TrainHeartnetCat/AppData/Roaming/Typora/typora-user-images/image-20240124181258892.png)

save另外个名字是不会影响原来那个



VAL
ePro_1jpz-fix.pdb
Selected!
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=23.32
 ExecutiveRMSPairs: RMSD =    0.030 (4 to 4 atoms)
 Mutagenesis: no rotamers found in library.
PHE
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.045 (4 to 4 atoms)
 Mutagenesis: no rotamers found in library.
 ExecutiveRMSPairs: RMSD =    0.028 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=19.03
ALA
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.022 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 2/3, strain=31.96
 ExecutiveRMSPairs: RMSD =    0.027 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 2/3, strain=47.45
PHE
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.031 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 3/3, strain=30.49
 ExecutiveRMSPairs: RMSD =    0.031 (4 to 4 atoms)
 Mutagenesis: no rotamers found in library.
PRO
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.029 (4 to 4 atoms)
 Mutagenesis: no rotamers found in library.
 ExecutiveRMSPairs: RMSD =    0.053 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=42.22
THR
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.013 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=27.00
 ExecutiveRMSPairs: RMSD =    0.028 (4 to 4 atoms)
 Mutagenesis: 4 rotamers loaded.
 Rotamer 2/4, strain=33.20
ALA
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.032 (4 to 4 atoms)
 Mutagenesis: 2 rotamers loaded.
 Rotamer 2/2, strain=25.11
 ExecutiveRMSPairs: RMSD =    0.019 (4 to 4 atoms)
 Mutagenesis: 2 rotamers loaded.
 Rotamer 1/2, strain=18.18
ALA
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.013 (4 to 4 atoms)
 Mutagenesis: 2 rotamers loaded.
 Rotamer 2/2, strain=26.35
 ExecutiveRMSPairs: RMSD =    0.015 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=20.95
ALA
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.029 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 2/3, strain=22.48
 ExecutiveRMSPairs: RMSD =    0.029 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 2/3, strain=22.48
PHE
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.026 (4 to 4 atoms)
 Mutagenesis: 2 rotamers loaded.
 Rotamer 1/2, strain=44.67
 ExecutiveRMSPairs: RMSD =    0.018 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 2/3, strain=45.64
SER
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.027 (4 to 4 atoms)
 Mutagenesis: 2 rotamers loaded.
 Rotamer 2/2, strain=29.04
 ExecutiveRMSPairs: RMSD =    0.024 (4 to 4 atoms)
 Mutagenesis: 23 rotamers loaded.
 Rotamer 16/23, strain=15.59
HIS
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.021 (4 to 4 atoms)
 Mutagenesis: 24 rotamers loaded.
 Rotamer 23/24, strain=17.43
 ExecutiveRMSPairs: RMSD =    0.020 (4 to 4 atoms)
 Mutagenesis: 16 rotamers loaded.
 Rotamer 12/16, strain=17.39
GLU
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.020 (4 to 4 atoms)
 Mutagenesis: 16 rotamers loaded.
 Rotamer 14/16, strain=17.76
 ExecutiveRMSPairs: RMSD =    0.008 (3 to 3 atoms)
 Mutagenesis: no rotamers found in library.
ARG
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.010 (3 to 3 atoms)
 Mutagenesis: no rotamers found in library.
 ExecutiveRMSPairs: RMSD =    0.012 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=20.01
ALA
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.020 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=15.42
 ExecutiveRMSPairs: RMSD =    0.026 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 2/3, strain=21.33
LEU
ePro_1jpz-fix.pdb
Selected!
 ExecutiveRMSPairs: RMSD =    0.046 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=15.95
 ExecutiveRMSPairs: RMSD =    0.046 (4 to 4 atoms)
 Mutagenesis: 3 rotamers loaded.
 Rotamer 1/3, strain=15.95
[Finished in 2.5s]