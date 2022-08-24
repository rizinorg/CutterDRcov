import cutter
from .extras import hex_pad, file_name

def get_module_idx(modules, module):
    for i in range(len(modules)):
        if modules[i]['name'] == module:
            return i
    return -1



def analyse_function(function, base, covbbs):
    entry = ["", function['name'], hex_pad(function['offset'], 8), "", ""]
    bbs = cutter.cmdj("afbj @ " + function['name'])
    inst_count = 0
    inst_hits = 0
    bbs_count = 0
    bbs_hits = 0
    hit_set = set()
    to_be_added = {}
    for bblock in bbs:
        # radare2's basic block can't have jump inside it while that is
        # possible in DynamoRIO, for this reason we first need to check
        # if the size of the 2 basic block matches, if radare2's basic block
        # size is smaller thant we would add the next block untill the sizes
        # match. If dynamoRIO size is smaller then something is wrong with
        # r2 analysis or dynamoRIO coverage.
        bbs_count += 1
        inst_count += bblock['ninstr']
        dynamorio_size = 0
        covbbaddr = bblock['addr'] - base
        if covbbaddr in covbbs:
            dynamorio_size = covbbs[covbbaddr]
        if bblock['addr'] in to_be_added:
            dynamorio_size = to_be_added[bblock['addr']]
        if dynamorio_size == 0:
            continue
        bbs_hits += 1
        inst_hits += bblock['ninstr']
        hit_set.add(bblock['addr'])
        r2_size = bblock['size']
        if dynamorio_size > r2_size:
            to_be_added[bblock['addr'] + r2_size] = dynamorio_size - r2_size
    if bbs_hits == 0:
        return (None, hit_set)
    entry[3] = str(inst_hits) + "/" + str(inst_count)
    entry[4] = str(bbs_hits) + "/" + str(bbs_count)
    entry[0] = str(round(inst_hits * 100 / inst_count, 3)) + "%"
    return (entry, hit_set)

def analyse(config):
    config['bb_hits'] = set()
    config['table'] = []
    functions = cutter.cmdj("aflj")
    info = cutter.cmdj("ij")
    module = file_name(info['core']['file'])
    base = info["bin"]["baddr"]
    idx = get_module_idx(config['modules'], module)
    if idx == -1:
        return
    # [coverage, name, address, instruction hits, basic block hits]
    for function in functions:
        entry, hits = analyse_function(function, base, config['bbs'][idx])
        if entry is None:
            continue
        config['table'].append(entry)
        config['bb_hits'].update(hits)
