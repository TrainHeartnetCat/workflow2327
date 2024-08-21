from modeller import *

code = 'ePro_1jpz-miss'
env = Environ()
model = Model(env, file=code)
aln = Alignment(env)
aln.append_model(model, align_codes=code)
aln.write(file=code+'.seq')