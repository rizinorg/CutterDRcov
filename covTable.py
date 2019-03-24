import cutter
from pathlib import Path
from .extras import hexPad
def getModuleIdx(modules, module):
    for i in range(len(modules)):
        if modules[i]['name'] == module:
            return i



def analyse_function(function, covbbs):
    entry = ["", function['name'], hexPad(function['offset'], 8) ,"" ,""]
    bbs = cutter.cmdj("afbj @" + function['name'])
    inst_count = 0
    inst_hits = 0
    bbs_count = 0
    bbs_hits = 0
    hit_set = set()
    to_be_added = {}
    for bb in bbs:
        # radare2's basic block can't have jump inside it while that is
        # possible in DynamoRIO, for this reason we first need to check
        # if the size of the 2 basic block matches, if radare2's basic block
        # size is smaller thant we would add the next block untill the sizes
        # match. If dynamoRIO size is smaller then something is wrong with
        # r2 analysis or dynamoRIO coverage.
        bbs_count += 1
        inst_count += bb['ninstr']
        dynamoRIOSize = 0
        if bb['addr'] in covbbs:
            dynamoRIOSize = covbbs[bb['addr']]
        if bb['addr'] in to_be_added:
            dynamoRIOSize = to_be_added[bb['addr']]
        if dynamoRIOSize == 0:
            continue
        bbs_hits += 1
        inst_hits += bb['ninstr']
        hit_set.add(bb['addr'])
        r2Size = bb['size']
        if dynamoRIOSize > r2Size:
            to_be_added[bb['addr'] + r2Size] = dynamoRIOSize - r2Size
    if bbs_hits == 0:
        return (None, hit_set)
    entry[3] = str(inst_hits) + "/" + str(inst_count)
    entry[4] = str(bbs_hits) + "/" + str(bbs_count)
    entry[0] = str(round(inst_hits*100/inst_count,3)) + "%"
    return (entry, hit_set)

def analyse(config):
    functions = cutter.cmdj("aflj")
    module = Path(cutter.cmdj("ij")['core']['file']).name
    idx = getModuleIdx(config['modules'], module)
    # [coverage, name, address, instruction hits, basic block hits]
    config['bb_hits'] = set()
    config['table'] = []
    for function in functions:
        entry, hits = analyse_function(function, config['bbs'][idx])
        if entry == None:
            continue
        config['table'].append(entry)
        config['bb_hits'].update(hits)
