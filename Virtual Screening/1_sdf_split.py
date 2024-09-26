# coding:utf-8

# 2024/8/29 created
# @ Jun

import re
import os

def sdf_split(path, output_path):
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass

    with open(path, 'r') as file:
        sdf_content = file.read()
    # 注意这边split出来的片段是不会带'$$$$\n'的，后面写文件的时候得加回去
    molecules = sdf_content.split('$$$$\n')
    # re.compile()就是预编译，省得每次匹配的时候都要编译一下正则片段
    cid_pattern = re.compile(r'> <PUBCHEM_COMPOUND_CID>\n(\d+)\n')

    count = 0

    # enumerate(sequence, [start=0])用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标。
    # eg:  seasons = ['Spring', 'Summer', 'Fall', 'Winter']
    #      list(enumerate(seasons)) -> [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
    #      # 如果设置从下标1开始
    #      list(enumerate(seasons, start=1)) -> [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
    for i, molecule in enumerate(molecules):
        if molecule.strip():
            cid_match = cid_pattern.search(molecule)
            if cid_match:
                cid = cid_match.group(1)
                output_filename = f'CID_{cid}.sdf'
                output = output_path + '/' + output_filename
                with open(output, 'w') as output_file:
                    output_file.write(molecule.strip() + '\n$$$$\n')
                count += 1
                print(f"Saved {output_filename}")
            else:
                print(f"CID not found for molecule {i + 1}")
    print(f'{count} molecules slipt.')


if __name__ == '__main__':
    input_combined_sdf_file = 'PubChem_compound_smiles_similarity_3d_O=[N+]([O-])OCCCO_records-3DAll1302-3D.sdf'
    output_directory = './ligandsdf'
    sdf_split(input_combined_sdf_file, output_directory)