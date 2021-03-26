import re
import json
from solcx import install_solc_pragma, compile_files
from solcx import set_solc_version_pragma
from solcx import install_solc, set_solc_version


def compiler(sol_file_name):
    with open('%s' % sol_file_name, 'r', encoding="utf-8") as sol_file:
        if_pragma = False
        while True:
            pragma_line = sol_file.readline()
            #print(pragma_line)
            pragma_pattern = r'(pragma)[\s]+(solidity)[\s]+(.+);[\s]*(/+.*)*'
            match_pragma_pattern = re.match(pragma_pattern, pragma_line)
            if match_pragma_pattern:
                pragmas = match_pragma_pattern.groups()
                pragma = pragmas[2]
                #print('pragma: %s' % pragma)
                install_solc_pragma(pragma)
                set_solc_version_pragma(pragma)
                if_pragma = True
                break
            if not pragma_line:
                break
        if not if_pragma: # no pragma
            install_solc('v0.4.25')
            set_solc_version('v0.4.25')
    compiled_sol = compile_files([sol_file_name])
    file_name_key_list = list(compiled_sol.keys())
    contract_name_list = list()
    for k in file_name_key_list:
        contract_name = k.split(':')[-1]
        contract_name_list.append(contract_name)
        with open('%s.bin.txt' % contract_name, 'w', encoding="utf-8") as outfile:
            json.dump(compiled_sol[k]['bin'], outfile, ensure_ascii=False)
        with open('%s.asm.json' % contract_name, 'w', encoding="utf-8") as outfile:
            json.dump(compiled_sol[k]['asm'], outfile, ensure_ascii=False)
    with open('ast.json', 'w', encoding="utf-8") as outfile:
        json.dump(compiled_sol[file_name_key_list[0]]['ast'], outfile, ensure_ascii=False)

    return (if_pragma, contract_name_list)
