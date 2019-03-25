import ntpath

def hexPad(num, pad):
    return "{0:#0{1}x}".format(num,pad + 2)

# https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
# cuz windows sucks :( .. hard
def fileName(path):
   # There's one caveat: Linux filenames may contain backslashes. So on linux,
    # r'a/b\c' always refers to the file b\c in the a folder, while on Windows,
    # it always refers to the c file in the b subfolder of the a folder. So when
    # both forward and backward slashes are used in a path, you need to know the
    # associated platform to be able to interpret it correctly. In practice it's
    # usually safe to assume it's a windows path since backslashes are seldom
    # used in Linux filenames, but keep this in mind when you code so you don't
    # create accidental security holes.

    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
