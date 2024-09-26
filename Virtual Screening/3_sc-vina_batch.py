import os
import sys
from tqdm import trange
import time

pdbqt_dir = "./ligandpdbqt/"
outputpdbqt_dir = "./outputpdbqt/"
outputlog_dir = "./outputlog/"
receptor = '5g0r.pdbqt'
run = '200'
# cmd = 'vina --receptor 5g0r.pdbqt --ligand 3NOP.pdbqt --config grid.txt --num_modes 200 --out out.pdbqt > output.txt'

try:
    os.mkdir(outputpdbqt_dir)
    os.mkdir(outputlog_dir)
except FileExistsError:
    pass

start_time = time.time()

count = 0
work_list = os.listdir(pdbqt_dir)
for step in trange(len(work_list)):
    i = work_list[step]
    count += 1
    ligand = pdbqt_dir + i
    mol_id = i.split(".")[0]
    cmd = 'vina --receptor ' + receptor + ' --ligand ' + ligand + ' --config grid.txt --num_modes ' + run + ' --out ' + outputpdbqt_dir + mol_id + '_out.pdbqt' + ' > ' + outputlog_dir + mol_id + '_output.txt'
    print(cmd)
    os.system(cmd)

end_time = time.time()
total_sec = end_time - start_time
total_hour = total_sec / 3600
print(str(count) + ' ligands have been docked.')
print(f"Finished in {total_sec:.2f} seconds, namely {total_hour:.2f} hours.")

