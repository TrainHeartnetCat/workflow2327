from modeller import *
from modeller.automodel import *    # Load the AutoModel class

log.verbose()
env = Environ()

# directories for input atom files
# 没具体查这行的规则，但根据情况推测第一个参数是运算完文件保存位置(然而测试了一下并不是)，第二个可能是临时文件位置(然鹅测试了一下并不是)，似乎会自动删除
# 这一行第一个参数随便设置都还是产生在当前文件夹，我个人感觉它只需要存在即可，根据.io推测是输入参数，估计在library位置
env.io.atom_files_directory = ['.', '../atom_files']

class MyModel(AutoModel):
    def select_atoms(self):
        return Selection(self.residue_range('227:A', '228:A'))

a = MyModel(env, alnfile = 'alignment.ali',
            knowns = 'ePro_1jpz-miss.pdb', sequence = '1jpz_fill')
a.starting_model= 1
a.ending_model  = 1

a.make()

