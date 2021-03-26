import json
import sys

def get_ordered_ast(ast, contract_count, if_pragma):
    ast_dict = dict()
    ast_dict['Contracts'] = list()
    for i in range(contract_count):
        parent_ast = ast['children'][i+int(if_pragma)]
        if parent_ast['name'] == 'PragmaDirective':
            continue
        cont_info = get_cont_info(parent_ast)
        cont_info['Variables'] = list()
        cont_info['Events'] = list()
        cont_info['Functions'] = list()
        child_ast = parent_ast.get('children')
        if child_ast != None:
            for child in child_ast:
                if child['name'] == 'VariableDeclaration':
                    variables = get_var_info(child)
                    cont_info['Variables'].append(variables)
                elif child['name'] == 'EventDefinition':
                    events = get_event_info(child)
                    cont_info['Events'].append(events)
                elif child['name'] == 'FunctionDefinition':
                    functions = get_func_info(child)
                    cont_info['Functions'].append(functions)
            ast_dict['Contracts'].append(cont_info)
    return ast_dict

def get_cont_info(cont_ast):
    cont_attributes = cont_ast['attributes']
    cont_info = dict()
    cont_info['name'] = cont_attributes['name']
    cont_info['dependencies'] = cont_attributes['contractDependencies']
    cont_info['type'] = cont_attributes['contractKind']
    cont_info['linearizedBase'] = cont_attributes['linearizedBaseContracts']
    cont_info.update(get_range(cont_ast))
    return cont_info

def get_var_info(var_ast):
    var_attributes = var_ast['attributes']
    var_info = dict()
    var_info['isConstant'] = var_attributes['constant']
    var_info['visibility'] = var_attributes['visibility']
    var_info['type'] = var_attributes['type']
    var_info.update(get_range(var_ast))
    return var_info

def get_event_info(event_ast):
    event_attributes = event_ast['attributes']
    event_info = dict()
    event_info['parameters'] = list()
    param_ast = event_ast.get('children')
    if param_ast != None:
        var_ast = param_ast[0].get('children')
        if var_ast != None:
            for v in var_ast:
                event_info['parameters'].append(get_var_info(v))
    name = event_attributes['name']
    param_size = len(event_info['parameters'])
    if param_size > 0:
        name = '%s(%s)' %(name, param_size)
    event_info['name'] = name
    event_info.update(get_range(event_ast))
    return event_info

def get_func_info(func_ast):
    func_attributes = func_ast['attributes']
    func_info = dict()
    func_info['isConstant'] = func_attributes['constant']
    func_info['visibility'] = func_attributes['visibility']
    func_info['superFunction'] = func_attributes['superFunction']
    func_info['isConstructor'] = func_attributes['isConstructor']
    func_info['Parameters'] = list()
    func_info['Variables'] = list()
    child_ast = func_ast.get('children')
    if child_ast != None:
        for child in child_ast:
            if child['name'] == 'VariableDeclaration':
                variables = get_var_info(child)
                func_info['Variables'].append(variables)
            elif child['name'] == 'ParameterList':
                var_ast = child.get('children')
                if var_ast != None:
                    for v in var_ast:
                        func_info['Parameters'].append(get_var_info(v))
    name = func_attributes['name']
    if name == '':
        name = 'fallback'
    param_size = len(func_info['Parameters'])
    if param_size > 0:
        name = '%s(%s)' %(name, param_size)
    func_info['name'] = name
    func_info.update(get_range(func_ast))
    return func_info

def get_range(ast):
    src_list = ast['src'].split(':')
    begin = int(src_list[0])
    plus = int(src_list[1])
    #id = ast['id']
    #range = {'begin': begin, 'end': begin+plus, 'id': id}
    range = {'begin': begin, 'end': begin+plus}
    return range

def count_address(asm_dict, address, bin):
    begin = address*2
    sixty = int('60', 16)
    if asm_dict['name'] != 'tag':
        if asm_dict['name'] == 'PUSH':
            address += (len(asm_dict['value'])+1) // 2
        elif asm_dict['name'] == 'PUSH [tag]':
            add = bin[begin:begin+2]
            address += int(add, 16)-sixty+1
        elif asm_dict['name'] == 'PUSHSIZE':
            add = bin[begin:begin+2]
            address += int(add, 16)-sixty+1
        elif asm_dict['name'] == 'PUSH [$]' or asm_dict['name'] == 'PUSH #[$]':
            add = bin[begin:begin+2]
            address += int(add, 16)-sixty+1
        elif asm_dict['name'] == 'PUSHDEPLOYADDRESS':
            address += 20
        elif asm_dict['name'] == 'PUSHLIB':
            #print('PUSHLIB')
            #print(bin[begin:begin+2])
            address = set_PUSHLIB(bin, begin, address)
        elif asm_dict['name'] != 'JUMP':
            if asm_dict.get('value') != None:
                address += 1
        address = address+1
    return (bin, address)

def set_PUSHLIB(bin, begin, address):
    i = 0
    start = begin+4
    bin_former = bin[0:start-2]
    while True:
        current = start+i
        under_bar = bin[current:current+2]
        if under_bar == '__':
            #next = bin[current+2:current+4]
            #print(bin[start-3:current+3], i)
            bin_latter = bin[current+2:-1]
            bin_tmp = '00'
            for bin_i in range(i+2):
                bin_tmp += '0'
            if current%2 == 1:
                bin_tmp += '0'
            bin = bin_former + bin_tmp + bin_latter
            #print(bin[start-3:current+3])
            address += (i+1)//2 + 2
            break
        i += 1
    return address

def if_already_saved(current, name):
    for curr in current:
        if curr['name'] == name:
            return curr
    return None

def set_contract(data, cont_info, address):
    contract = dict()
    contract['name'] = cont_info['name']
    contract['sea'] = address
    contract['see'] = -1
    contract['id'] = address
    contract['type'] = cont_info['type']
    contract['call'] = list()
    contract['linearizedBase'] = cont_info['linearizedBase']
    contract['dependencies'] = cont_info['dependencies']
    contract['variables'] = cont_info['Variables']
    contract['events'] = cont_info['Events']
    contract['vulnerabilities'] = list()
    contract['functions'] = list()
    data['contracts'].append(contract)
    return contract

def set_function(contract, func_info, address):
    function = dict()
    function['name'] = func_info['name']
    function['sea'] = address
    function['see'] = -1
    function['id'] = address
    function['call'] = list()
    function['isConstant'] = func_info['isConstant']
    function['visibility'] = func_info['visibility']
    function['superFunction'] = func_info['superFunction']
    function['isConstructor'] = func_info['isConstructor']
    function['parameters'] = func_info['Parameters']
    function['variables'] = func_info['Variables']
    function['vulnerabilities'] = list()
    function['blocks'] = list()
    contract['functions'].append(function)
    return function

def set_block(name, address, id, function):
    block = dict()
    block['name'] = name
    block['sea'] = address
    block['see'] = -1
    block['id'] = id
    block['call'] = list()
    block['src'] = list()
    function['blocks'].append(block)
    return block

def search_current_cont_from_asm(asm, data_info, data, prev_cont, address):
    if prev_cont != None:
        prev_cont['see'] = address
    asm_begin = int(asm['begin'])
    asm_end = int(asm['end'])
    for cont_info in data_info:
        cont_begin = int(cont_info['begin'])
        cont_end = int(cont_info['end'])
        if cont_begin <= asm_begin and asm_end <= cont_end:
            contract = if_already_saved(data['contracts'], cont_info['name'])
            if contract == None:
                contract = set_contract(data, cont_info, address)
            return (contract, cont_info)
    return (None, None)

def search_current_func_from_asm(asm, cont_info, contract, prev_func, address):
    if prev_func != None:
        prev_func['see'] = address
        #prev_func['blocks'][-1]['see'] = address
    asm_begin = int(asm['begin'])
    asm_end = int(asm['end'])
    # get information of all function in the contract
    func_info_list = cont_info['Functions']
    # loop for each function
    for func_info in func_info_list:
        # get a begin/end address of the function
        func_begin = int(func_info['begin'])
        func_end = int(func_info['end'])
        if func_begin <= asm_begin and asm_end <= func_end:
            function = if_already_saved(contract['functions'], func_info['name'])
            if function == None:
                #create a new function
                function = set_function(contract, func_info, address)
            return function
    return None

def search_current_block_from_asm(asm, function, prev_block, address, id, callee):
    #a new block -> the empty function
    if asm['name'] == 'tag':
        #the current address -> see(end) of the previous block
        prev_block['see'] = address
        name = 'tag' + asm['value']
        #record the callee
        callee.update({name: id})
        callee.update({address: name})
        id += 1
        #new block (the current address -> sea(start))
        #set_block needs block -> function
        block = set_block(name, address, id, function)
        return (block, id)
    else:
        #a new src -> the current block
        prev_block['src'].append(set_src(hex(address), asm['name'], asm.get('value')))
        return (prev_block, id)

def set_src(address, name, value):
    src = list()
    src.append(address)
    src.append(name)
    if value != None:
        src.append(value)
    return src

def call_parse(data, asm, ast, cont_name, address, id, callee, bin, prev_cont, prev_func, prev_block, depth):
    code = asm['.code']
    if depth > 0:
        address += 1
    (prev_cont, prev_func, prev_block, address, id, bin) = parse(
    data, code, ast, cont_name, address, id, callee, bin, prev_cont, prev_func, prev_block)
    depth += 1
    if asm.get('.data') != None:
        for next_asm in asm['.data'].values():
            (prev_cont, prev_func, prev_block, address, id, bin) = call_parse(
            data, next_asm, ast, cont_name, address, id, callee, bin, prev_cont, prev_func, prev_block, depth)
    return (prev_cont, prev_func, prev_block, address, id, bin)

def parse(data, asm_list, ast, cont_name, address, id, callee, bin, prev_cont, prev_func, prev_block):
    data_info = ast['Contracts']
    contract = prev_cont
    function = prev_func
    block = prev_block
    while(True):
        if len(asm_list) == 0:
            return (contract, function, block, address, id, bin)
        asm = asm_list.pop(0)
        (contract, cont_info) = search_current_cont_from_asm(asm, data_info, data, contract, address)
        if contract != None:
            function = search_current_func_from_asm(asm, cont_info, contract, function, address)
            if function != None:
                if block != None:
                    block['see'] = address
                block_name = 'start_'+str(address)
                id += 1
                block = set_block(block_name, address, id, function)
                block['src'].append(set_src(hex(address), asm['name'], asm.get('value')))
                callee.update({block_name: id})
                callee.update({address: block_name})
                (bin, address) = count_address(asm, address, bin)
                break
        (bin, address) = count_address(asm, address, bin)
    for asm in asm_list:
        #get the current function/block
        (contract, cont_info) = search_current_cont_from_asm(asm, data_info, data, contract, address)
        if contract != None:
            function = search_current_func_from_asm(asm, cont_info, contract, function, address)
            if function != None:
                (block, id) = search_current_block_from_asm(asm, function, block, address, id, callee)
        #count the current address
        (bin, address) = count_address(asm, address, bin)
    #function['see'] = address
    return (contract, function, block, address, id, bin)

def search_callee(data, c, f, b, callee_name):
    for b2 in f['blocks']:
        if b2['name'] == callee_name: #the callee block in the same function
            if not (b2['id'] in b['call']):
                b['call'].append(b2['id'])
            return
    for f2 in c['functions']:
        for b2 in f2['blocks']:
            if b2['name'] == callee_name: #the callee block in the same contract
                if not (f2['id'] in f['call']):
                    f['call'].append(f2['id'])
                return
    for c2 in data['contracts']:
        for f2 in c2['functions']:
            for b2 in f2['blocks']:
                if b2['name'] == callee_name: #the callee block in the same contract
                    if not (c2['id'] in c['call']):
                        c['call'].append(c2['id'])
                    return

def get_call(data, callee, end_address):
    for c in data['contracts']:
        for f in c['functions']:
            for b in f['blocks']:
                if b['see'] == end_address:
                    continue
                #search the next block/function/contract
                last_inst = b['src'][-1][1]
                if last_inst != 'JUMP' and last_inst != 'RETURN' and last_inst != 'REVERT' and last_inst != 'INVALID' and last_inst != 'SELFDESTRUCT' and last_inst != 'STOP':
                    next_name = callee[b['see']]
                    search_callee(data, c, f, b, next_name)
                #search the callee block/function/contract
                for s in b['src']: # PUSH [tag]
                    if s[1] == 'PUSH [tag]':
                        callee_name = 'tag' + s[2]
                        search_callee(data, c, f, b, callee_name)

def get_json(file):
    with open(file, 'r', encoding="utf-8") as f:
        json_file = f.read()
        return json.loads(json_file)

def labeling(file_name, data, label):
    name = file_name.split('.')[0]
    s_label = label.get(name)
    if s_label == None:
        print("Failed to label")
        sys.exit(1)
    data['vulnerabilities'] = get_label_list(s_label['source'])
    for c in data['contracts']:
        c_label = s_label.get(c['name'])
        if c_label != None:
            c['vulnerabilities'] = get_label_list(c_label['contract'])
            for f in c['functions']:
                f_label = c_label.get(f['name'].split('(')[0])
                if f_label != None:
                    f['vulnerabilities'] = get_label_list(f_label)

def get_label_list(label):
    label_list = list()
    for v in label:
        if label[v] == 1:
            label_list.append(v)
    return label_list
