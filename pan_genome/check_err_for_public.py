import re

def modify_nuc(file_name,pro):
	print(pro,file_name)
	try:
		file_object = open('./input/'+file_name+'.nuc')
		seqs = file_object.read()
		file_object.close()
		pro_pattern = re.compile(r'>'+pro+'\n.*')
		new_seqs = re.sub(pro_pattern,'',seqs)
		with open('./input/'+file_name+'.nuc','w') as f:
			f.write(new_seqs)
		print('nuc done.')
	except FileNotFoundError:
		print('nuc not done.')

def modify_func(file_name,pro):
	print(pro,file_name)
	try:
		file_object = open('./input/'+file_name+'.function')
		seqs = file_object.read()
		file_object.close()
		pro_pattern = re.compile(r''+pro+'.*\n')
		new_seqs = re.sub(pro_pattern,'',seqs)
		with open('./input/'+file_name+'.function','w') as f:
			f.write(new_seqs)
		print('func done.')
	except FileNotFoundError:
		print('func not done.')

def modify_pep(file_name,pro):
	print(pro,file_name)
	try:
		file_object = open('./input/'+file_name+'.pep')
		seqs = file_object.read()
		file_object.close()
		pro_pattern = re.compile(r'>'+pro+'\n.*')
		new_seqs = re.sub(pro_pattern,'',seqs)
		with open('./input/'+file_name+'.pep','w') as f:
			f.write(new_seqs)
		print('pep done.')
	except FileNotFoundError:
		print('pep not done.')

for line in open('./output/0.error.message'):
	#print(line)
	pattern = re.compile(r'the length of (.*) in input/(.*)\.nuc is not.*',re.S)
	result = re.findall(pattern,line)
	if len(result)>0:
		pro = result[0][0]
		file_name = result[0][1]
		modify_nuc(file_name,pro)
		modify_func(file_name,pro)
		modify_pep(file_name,pro)