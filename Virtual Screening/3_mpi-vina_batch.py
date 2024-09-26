import os
import subprocess
import time
from multiprocessing import Pool
from tqdm import tqdm
from functools import partial

def run_vina(ligand, receptor, GAruns, outputpdbqt_dir, outputlog_dir):
    # cmd = 'vina --receptor ' + receptor + ' --ligand ' + ligand + ' --config grid.txt --num_modes ' + run + ' --out ' + outputpdbqt_dir + mol_id + '_out.pdbqt' + ' > ' + outputlog_dir + mol_id + '_output.txt'
    lig_name = os.path.basename(ligand)
    lig_result = lig_name.replace(".pdbqt", "_out.pdbqt")
    lig_log = lig_name.replace(".pdbqt", "_out.txt")
    outputpdbqt = outputpdbqt_dir + '/' + lig_result
    outputlog = outputlog_dir + '/' + lig_log

    command = [
        "vina",
        "--receptor", receptor,
        "--ligand", ligand,
        "--config", "grid.txt",
        "--num_modes", GAruns,
        "--out", outputpdbqt,
    ]

    subprocess.run(command)
    print("Running command:", " ".join(command))
    with open(outputlog, 'a') as log:  # 追加模式打开日志文件
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)

    return result

def format_time(seconds):
    # eg: 3600s = 1 hour and 0 min and 0 second
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return hours, minutes, seconds

def mpi_run(lig_pdbqt_dir, receptor, GAruns, outputpdbqt_dir, outputlog_dir, cn=1):
    try:
        os.mkdir(outputpdbqt_dir)
        os.mkdir(outputlog_dir)
    except FileExistsError:
        pass
        
    ligand_path = []
    for i in os.listdir(lig_pdbqt_dir):
        path = lig_pdbqt_dir + '/' + i
        ligand_path.append(path)

    start_time = time.time()

    # use partial to fix args or use tuple to convey args
    # tuple eg:
    # args_list = [(file, GAruns) for file in ligand_files]
    # with Pool(processes=os.cpu_count()) as pool:
    #     list(tqdm(pool.imap(run_vina, args_list), total=len(args_list)))
    # partial eg:
    with Pool(processes=cn) as pool: # processes=os.cpu_count()
        run_vina_partial = partial(run_vina, receptor=receptor, GAruns=GAruns, outputpdbqt_dir=outputpdbqt_dir, outputlog_dir=outputlog_dir)
        list(tqdm(pool.imap(run_vina_partial, ligand_path), total=len(ligand_path)))

    end_time = time.time()
    total_sec = end_time - start_time
    total_hour = total_sec / 3600
    print(str(len(ligand_path)) + ' ligands have been docked.')
    print(f"Finished in {total_sec:.2f} seconds, namely {total_hour:.2f} hours.")

if __name__ == '__main__':
    pdbqt_dir = "./ligandpdbqt/"
    outputpdbqt_dir = "./outputpdbqt/"
    outputlog_dir = "./outputlog/"
    receptor = '5g0r.pdbqt'
    run = '200'
    mpi_c = 32

    mpi_run(pdbqt_dir, receptor, run, outputpdbqt_dir, outputlog_dir, mpi_c)