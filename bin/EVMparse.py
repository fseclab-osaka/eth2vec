import json
import os
import EVMfunction as EVMf

def extract_code(code_data, depth, remove_byte_list):
    code = code_data['.code']
    for c in code:
        if 'tag' in c['name']:
            for i in range(depth):
                c['value'] = '0' + c['value']
    depth += 1
    if code_data.get('.data') != None:
        for next_code in code_data['.data'].values():
            #with open('asm%d.json' % depth, 'w', encoding="utf-8") as outfile:
                #json.dump(next_code, outfile, ensure_ascii=False)
            aux = next_code.get('.auxdata')
            if aux != None:
                remove_byte_list.append(aux)
            (depth, remove_byte_list) = extract_code(next_code, depth, remove_byte_list)
    return (depth, remove_byte_list)

def get_code_information(file_name_list):
    asm = list()
    ast = dict()
    bin = ''
    depth = 0
    for file_name in file_name_list:
    #for nn in range(2):
        #file_name = file_name_list[nn]
        #print('read %s' % contract_name_list[contract_count])
        remove_byte_list = list()
        asm_file = file_name + '.asm.json'
        asm_tmp = EVMf.get_json(asm_file)
        os.remove(asm_file)
        if asm_tmp != None:
            (depth, remove_byte_list) = extract_code(asm_tmp, depth, remove_byte_list)
        asm.append(asm_tmp)

        with open('%s.bin.txt' % file_name, 'r', encoding="utf-8") as bin_file:
            bin_tmp = bin_file.read() # bytecode + .auxdata
            if len(remove_byte_list) > 0:
                for b in remove_byte_list:
                    if remove_byte_list.index(b) == len(remove_byte_list) -1:
                        remove_byte = '00' + b
                    else:
                        remove_byte = b
                    #print(remove_byte)
                    bin_tmp = bin_tmp.replace(remove_byte, '')
        os.remove(file_name + '.bin.txt')
        bin = bin + bin_tmp.split('\"')[1] # remove "..."
        #with open('asm%d.json' % contract_count, 'w', encoding="utf-8") as outfile:
            #json.dump(asm_tmp, outfile, ensure_ascii=False)

    #with open('bin.txt', 'w', encoding="utf-8") as bin_file:
        #bin_file.write(bin)

    ast = EVMf.get_json('ast.json')
    os.remove('ast.json')

    return (asm, bin, ast)
