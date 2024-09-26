import os
import sys

sdf_dir="./ligandsdf/"
output_dir="./ligandpdbqt/"
# cmd = 'mk_prepare_ligand.py -i CID_5447.sdf -o CID_5447.pdbqt'
# print(os.listdir(sdf_dir))
count = 0
for i in os.listdir(sdf_dir):
    count += 1
    sdf = sdf_dir + i
    pdbqt = i.split(".")[0]
    cmd = 'mk_prepare_ligand.py -i ' + sdf + ' -o ' + output_dir + pdbqt + '.pdbqt'
    print(cmd)
    os.system(cmd)
print(count)