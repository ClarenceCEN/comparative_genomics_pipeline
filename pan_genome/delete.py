import re
import os


current_path = os.getcwd()
input_path = os.path.join(current_path,'input')
function_files = os.listdir(input_path)

pattern = re.compile(r'\|GeneMark.hmm.*?\s')

for function_file in function_files:
    if function_file.endswith('.function'):
        print(function_file)
        with open(os.path.join(input_path,function_file), 'r') as f:
            input_f = f.read()


        with open(os.path.join(input_path,function_file),'w') as f:
            output_f = re.sub(pattern,'\t',input_f)
            f.write(output_f)

