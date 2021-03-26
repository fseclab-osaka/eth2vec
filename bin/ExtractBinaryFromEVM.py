import sys
import os
import json
import hashlib
import EVMfunction as EVMf
import EVMcompiler as EVMc
import EVMparse as EVMp


print('Kam1n0 script for EVM is now running...')
print('start persisting...')

args = sys.argv
sol_file_name = args[1].split('\\')[-1]
abs_file_name = os.path.abspath(args[1])
json_file_name = abs_file_name


#Compile sol -> bin, asm
print('compile %s' % sol_file_name)
(if_pragma, contract_name_list) = EVMc.compiler(abs_file_name)


#Parse
data = dict()
data['ida_compiler'] = 'Unknown'
data['name'] = abs_file_name
data['md5'] = hashlib.md5(data['name'].encode('utf-8')).hexdigest()
data['architecture'] = {}
data['architecture']['type'] = 'metapc' #evm
data['architecture']['size'] = 'b64' #??
data['architecture']['endian'] = "le" #??
data['vulnerabilities'] = list()
data['contracts'] = list()

(asm, bin, ast) = EVMp.get_code_information(contract_name_list)

contract_count = len(contract_name_list)
ordered_ast = EVMf.get_ordered_ast(ast, contract_count, if_pragma) # get ordered_ast['Function']

#parameter
block_id = 0
current_address = 0
callee = dict()
prev_cont = None
prev_func = None
prev_block = None
for i in range(contract_count):
    if asm[i] != None:
        (prev_cont, prev_func, prev_block, current_address, block_id, bin) = EVMf.call_parse(
        data, asm[i], ordered_ast, contract_name_list[i], current_address,
        block_id, callee, bin, prev_cont, prev_func, prev_block, 0)
end_address = current_address
if prev_cont != None:
    prev_cont['see'] = end_address
if prev_func != None:
    prev_func['see'] = end_address
if prev_block != None:
    prev_block['see'] = end_address

#bytes
for c in data['contracts']:
    for f in c['functions']:
        for b in f['blocks']:
            begin = b['sea']*2
            end = b['see']*2
            b['bytes'] = bin[begin: end]
            #print(b['name'], ': ', begin, end, ': ', b['bytes'])

#call
EVMf.get_call(data, callee, end_address)

#Labeling
print('give labels to %s' % sol_file_name)
label_file = '.\\Label.json'
label = EVMf.get_json(label_file);
EVMf.labeling(sol_file_name, data, label);

#concate contracts and functions
data['functions'] = list()
for c in data['contracts']:
    for f in c['functions']:
        f['name'] = f['name'] + '.' + c['name']
        data['functions'].append(f)

#output
with open('%s.tmp0.json' % json_file_name, 'w', encoding="utf-8") as outfile:
    json.dump(data, outfile, ensure_ascii=False)
