import re
from pathlib import Path
import struct


MIN_DRCOV_FILE_SIZE = 20
DRCOV_VERSION = 2

DRCOV_HEADER_RE = "DRCOV VERSION: (?P<version>\d+)\n"
MODULE_HEADER_V2_RE = "Module Table: version (?P<version>\d+), count (?P<mod_num>\d+)\n"
BB_HEADER_RE = "BB Table: (?P<bbcount>\d+) bbs\n"
class InvalidDRCovFile(Exception):
    pass

class DRCovVersionMisMatch(Exception):
    pass

def get_file_size(f):
    """
        f: file
    """
    f.seek(0,2)
    file_size = f.tell()
    f.seek(0,0)
    return file_size

def open_file(file_name):
    f = open(file_name, "rb")
    file_size = get_file_size(f)
    if file_size <= MIN_DRCOV_FILE_SIZE:
        raise InvalidDRCovFile
    return f
    
def check_module_header(f):
    header = f.readline().decode('utf-8')
    pattern = re.match(DRCOV_HEADER_RE, header)
    version = int(pattern.group('version'))
    if version != DRCOV_VERSION:
        raise DRCovVersionMisMatch    
    # "DRCOV FLAVOR" doesn't really matter
    f.readline()

def get_module_header_info(f):
    header = f.readline().decode('utf-8')
    pattern = re.match(MODULE_HEADER_V2_RE, header)
    # skip "Columns: id, containing_id, start, end, entry, offset, path"
    f.readline()
    return (int(pattern.group("mod_num")), int(pattern.group("version")))

def parse_module_entry(f, version):
    entry = f.readline().decode('utf-8')[:-1]
    #XXX now put commas and spaces in the file path and this gets fucked up
    entry = re.split(",\s+", entry)
    if version == 2:
        return {"start": int(entry[1], 16), "name": Path(entry[-1]).name}
    else:
        return {"start": int(entry[2], 16), "name": Path(entry[-1]).name}
        
def read_module_list(f):
    modules = []    
    check_module_header(f)
    mod_num, mod_version = get_module_header_info(f)
    for i in range(mod_num):
        modules.append(parse_module_entry(f, mod_version))
    return modules

def parse_bb_header(f):
    header = f.readline().decode('utf-8')
    pattern = re.match(BB_HEADER_RE, header)
    return int(pattern.group("bbcount"))

def read_bb_list(f, module_count):
    bblist = [{} for i in range(module_count)]
    bb_count = parse_bb_header(f)
    struct_fmt = '<IHH'
    struct_size = struct.calcsize(struct_fmt)
    struct_unpack = struct.Struct(struct_fmt).unpack_from
    for i in range(bb_count):
        # size of struct is 64 bit
        bb = f.read(8)
        offset, size, mod_num = struct_unpack(bb)
        bblist[mod_num][offset] = size
    return bblist

def DCov_dead_module_elimination(modules, bbs):
    delete = []
    import pdb
    pdb.set_trace()
    for i in range(len(bbs)):
        if len(bbs[i]) == 0:
            delete.insert(0, i)
    for i in delete:
        del bbs[i]
        del modules[i]
def DCov_load(file_name):
    f = open_file(file_name)
    modules = read_module_list(f)
    bbs = read_bb_list(f, len(modules))
    f.close()
    DCov_dead_module_elimination(modules, bbs)
    return [modules, bbs]
