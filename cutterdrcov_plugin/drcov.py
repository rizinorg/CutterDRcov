import re
import struct
from .extras import file_name

MIN_DRCOV_FILE_SIZE = 20
DRCOV_VERSION = 2

DRCOV_HEADER_RE = r"DRCOV VERSION: (?P<version>\d+)\n"
MODULE_HEADER_V2_RE = r"Module Table: version (?P<version>\d+), count (?P<mod_num>\d+)\n"
BB_HEADER_RE = r"BB Table: (?P<bbcount>\d+) bbs\n"

class DRCovVersionMisMatch(Exception):
    pass

def check_module_header(drcov_file):
    header = drcov_file.readline().decode('utf-8')
    pattern = re.match(DRCOV_HEADER_RE, header)
    version = int(pattern.group('version'))
    if version != DRCOV_VERSION:
        raise DRCovVersionMisMatch
    # "DRCOV FLAVOR" doesn't really matter
    drcov_file.readline()

def get_module_header_info(drcov_file):
    header = drcov_file.readline().decode('utf-8')
    pattern = re.match(MODULE_HEADER_V2_RE, header)
    # skip "Columns: id, containing_id, start, end, entry, offset, path"
    drcov_file.readline()
    return (int(pattern.group("mod_num")), int(pattern.group("version")))

def parse_module_entry(drcov_file, version):
    entry = drcov_file.readline().decode('utf-8')[:-1]
    #XXX now put commas and spaces in the file path and this gets fucked up
    entry = re.split(r",\s+", entry)
    if version == 2:
        return {"start": int(entry[1], 16), "name": file_name(entry[-1])}
    return {"start": int(entry[2], 16), "name": file_name(entry[-1])}

def read_module_list(drcov_file):
    modules = []
    check_module_header(drcov_file)
    mod_num, mod_version = get_module_header_info(drcov_file)
    for _ in range(mod_num):
        modules.append(parse_module_entry(drcov_file, mod_version))
    return modules

def parse_bb_header(drcov_file):
    header = drcov_file.readline().decode('utf-8')
    pattern = re.match(BB_HEADER_RE, header)
    return int(pattern.group("bbcount"))

def read_bb_list(drcov_file, module_count):
    bblist = [{} for i in range(module_count)]
    bb_count = parse_bb_header(drcov_file)
    struct_fmt = '<IHH'
    struct_size = struct.calcsize(struct_fmt)
    struct_unpack = struct.Struct(struct_fmt).unpack_from
    for _ in range(bb_count):
        # size of struct is 64 bit
        bb_struct = drcov_file.read(struct_size)
        offset, size, mod_num = struct_unpack(bb_struct)
        if mod_num > module_count:
            # we have a case where dynamocov failed to capture which modules
            # does this basic block belongs to
            # print("Warning: we have unknown module number:", mod_num)
            continue
        bblist[mod_num][offset] = size
    return bblist

def dead_module_elimination(modules, bbs):
    delete = []
    for i in range(len(bbs)):
        if not bbs[i]:
            delete.insert(0, i)
    for i in delete:
        del bbs[i]
        del modules[i]


def intersect_bbs(bbs):
    result = {}
    first_dict = bbs[0]
    other_dicts = bbs[1:]
    for bb, size in first_dict.items():
        if all(bb in d for d in other_dicts):
            result[bb] = size
    return result


def union_bbs(bbs):
    result = {}
    for d in bbs:
        result.update(d)
    return result


def subtract_bbs(bbs):
    result = {}
    first_dict = bbs[0]
    other_dicts = bbs[1:]
    for bb, size in first_dict.items():
        if all(bb not in d for d in other_dicts):
            result[bb] = size
    return result


def process_set_of_files(path):
    supported_operations = {
        'intersect': intersect_bbs,
        'subtract': subtract_bbs,
        'union': union_bbs
    }
    with open(path, "r") as f:
        all_lines = [l.rstrip(' \t\n\r') for l in f.readlines()]
        lines = [l for l in all_lines if len(l)]
    op = supported_operations.get(lines[0])
    if not op:
        raise Exception('Unsupported operation')
    lines = lines[1:]
    if len(lines) == 1:
        return load(lines[0])
    files = [load(l) for l in lines]
    mod_list = files[0][0]
    mod_names = [ m['name'] for m in mod_list ]
    if any([m['name'] for m in f[0]] != mod_names for f in files[1:]):
        raise Exception('Module lists differ among coverage files')
    bbs = []
    for m in range(len(mod_list)):
        dicts = [f[1][m] for f in files]
        bbs.append(op(dicts))
    return [mod_list, bbs]


def load(path):
    if path.endswith(".set"):
        return process_set_of_files(path)
    drcov_file = open(path, "rb")
    modules = read_module_list(drcov_file)
    bbs = read_bb_list(drcov_file, len(modules))
    drcov_file.close()
    dead_module_elimination(modules, bbs)
    return [modules, bbs]
