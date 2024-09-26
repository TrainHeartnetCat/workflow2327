import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Pool
from functools import partial
import time
from tqdm import tqdm

def create_gpf(ligand_path, griding_dir, npts, gridcenter, receptor):
    lig = os.path.basename(ligand_path)
    lig_name = lig.replace('.pdbqt', '')
    gpf_dirpath = griding_dir + "/" + lig_name
    try:
        os.mkdir(gpf_dirpath)
    except FileExistsError:
        pass
    gpf_path = gpf_dirpath + "/" + "grid.gpf"
    npt = "npts=" + npts
    gridc = "gridcenter=" + gridcenter

    command = [
        "prepare_gpf.py",
        "-l", ligand_path, 
        "-r", receptor,
        "-p", npt,
        "-p", gridc,
        "-o", gpf_path,
    ]
    
    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Running command:", " ".join(command))
    except subprocess.CalledProcessError as e:
        print(f"Error generating gpf file with ligand {lig_name}: {e}")
        return None

    # modify .gpf with parameter_file path for the first line
    parameter_line = "parameter_file /home/Nye/soft/ADFRsuite-1.0/CCSBpckgs/AutoDockTools/AD4_parameters.dat\n"
    abspath_receptor = os.getcwd() + '/' + receptor
    
    with open(gpf_path, 'r+') as f:
        content = f.read()  # read all
        new_content = content.replace(f"receptor {receptor}", f"receptor {abspath_receptor}")
        f.seek(0, 0)        # locating to the head of the text
        f.write(parameter_line + new_content)

def run_autogrid(ligand_path, griding_dir):
    lig = os.path.basename(ligand_path)
    lig_name = lig.replace('.pdbqt', '')
    gpf_dirpath = griding_dir + "/" + lig_name
    original_dir = os.getcwd()
    try:
        os.chdir(gpf_dirpath)
        command = [
            "autogrid4", 
            "-p", "grid.gpf",
            "-l", "grid.glg"
        ]
        
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print("Running command:", " ".join(command))
        except subprocess.CalledProcessError as e:
            print(f"Error generating glg file with ligand {lig_name}: {e}")
            return None
    finally:
        os.chdir(original_dir)


def run_adg(adg, ligand_path, griding_dir, receptor, run, outputlog_dir):
    lig = os.path.basename(ligand_path)
    lig_name = lig.replace('.pdbqt', '')
    output_log = outputlog_dir + "/" + lig_name + "_out"
    maps_name = receptor.replace('.pdbqt', '.maps.fld')
    maps_path = griding_dir + "/" + lig_name + '/' + maps_name
    
    command = [
        adg, 
        "--ffile", maps_path,
        "--lfile", ligand_path,
        "--nrun", run,         
        "--resnam", output_log, 
    ]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Running command:", " ".join(command))
        return (ligand_path, result.returncode, result.stdout.decode(), result.stderr.decode())
    except Exception as e:
        return (ligand_path, -1, "", str(e))


def parallel_docking(pdbqt_dir, griding_dir, npts, gridcenter, outputlog_dir, receptor, run, adg, cpu_core=8, max_parallel=4):
    try:
        os.mkdir(griding_dir)
        os.mkdir(outputlog_dir)
    except FileExistsError:
        pass

    start_time = time.time()

    ligand_path = []
    for i in os.listdir(pdbqt_dir):
        path = pdbqt_dir + '/' + i
        ligand_path.append(path)

    with Pool(processes=cpu_core) as pool: # processes=os.cpu_count()
        create_gpf_partial = partial(create_gpf, griding_dir=griding_dir, npts=npts, gridcenter=gridcenter, receptor=receptor)
        list(tqdm(pool.imap(create_gpf_partial, ligand_path), total=len(ligand_path), desc="gpf generating progress"))

    with Pool(processes=cpu_core) as pool: # processes=os.cpu_count()
        run_autogrid_partial = partial(run_autogrid, griding_dir=griding_dir)
        list(tqdm(pool.imap(run_autogrid_partial, ligand_path), total=len(ligand_path), desc="glg generating progress"))

    with ProcessPoolExecutor(max_workers=max_parallel) as executor:
        # task submission
        futures = [executor.submit(run_adg, adg=adg, ligand_path=ligand, griding_dir=griding_dir, receptor=receptor, run=run, outputlog_dir=outputlog_dir) for ligand in ligand_path]
        
        with tqdm(total=len(futures), desc="docking progress") as pbar:
            for future in as_completed(futures):
                ligand_file, returncode, stdout, stderr = future.result()
                if returncode == 0:
                    print(f"No error of gpu-mpi running with {ligand_file}, if there is no autodock output log file, error probably happened during docking.")
                else:
                    print(f"Error of gpu-mpi running with {ligand_file}, Error: {stderr}")
                pbar.update(1)  # update tqdm bar
                
    total_seconds = time.time() - start_time
    total_hours = total_seconds / 3600
    print(f"Finished in {total_seconds:.2f} seconds, namely {total_hours:.2f} hours.")

if __name__ == "__main__":
    pdbqt_dir = "./ligandpdbqt/"
    griding_dir = "./griding/"
    npts = '34,40,32'
    gridcenter = '33.375,39.059,-55.535'
    # AD4 is different with ADVina, the output log contains pdbqt and scroing
    # outputpdbqt_dir = "./outputpdbqt/"
    outputlog_dir = "./outputlog/"
    receptor = '5g0r.pdbqt'
    run = '200'
    # autodock-gpu command
    # alias is defined in shell, subprocess and multiprocessing can not use alias unless open a shell which could be risky.
    # eg: command = "ad4_g128 -p input_file -l output_file"
    #     subprocess.run(command, shell=True)
    # or: command = "source ~/.bashrc && ad4_g128 -p input_file -l output_file"
    #     subprocess.run(command, shell=True)
    # adg = 'ad4_g128'
    # using original or abs path of command is recommend.
    adg = '/home/Nye/soft/AutoDock-GPU-develop/bin/autodock_gpu_256wi'
    # cpu threads number
    cpu_core = 32
    # max gpu task number in parallel
    max_parallel = 256

    parallel_docking(pdbqt_dir, griding_dir, npts, gridcenter, outputlog_dir, receptor, run, adg, cpu_core, max_parallel)