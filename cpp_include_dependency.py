# -------------------------------
# ----- character functions -----
# -------------------------------

def ischar(c:str) -> bool:
    return len(c) == 1


def isalpha(c:str) -> bool:
    if not ischar(c):
        return False
    elif (ord('A') <= ord(c) <= ord('Z')) or (ord('a') <= ord(c) <= ord('z')) or c == '_':
        return True
    else:
        return False


def isnum(c:str) -> bool:
    if not ischar(c):
        return False
    elif ord('0') <= ord(c) <= ord('9'):
        return True
    else:
        return False


def isalnum(c:str) -> bool:
    if isalpha(c) or isnum(c):
        return True
    else:
        return False


def iswhitespace(c:str) -> bool:
    if not ischar(c):
        return False
    elif c == ' ' or c == '\t' or c == '\n':
        return True
    else:
        return False


# ----------------------------------
# ----- file related functions -----
# ----------------------------------

def read1(fin) -> str:
    try:
        c = fin.read(1)
    except:
        print('Warning: character unsupported by \'utf-8\' codec encountered.')
        c = '?'
    return c


def getcurpos(fin) -> int:
    return fin.tell()


def setcurpos(fin, pos:int) -> None:
    fin.seek(pos)


def get_filename_from_path(filepath:str) -> str:
    return filepath.split('/')[-1]


# --------------------------------------------------------------
# ----- function to extract includes from a given filepath -----
# --------------------------------------------------------------

from typing import List

def get_includes(filepath:str) -> List[str]:
    print('get_includes:', filepath)
    includes = []
    with open(filepath) as fin:
        while True:
            c = read1(fin)
            if not c:
                break

            elif c == '/':
                curpos = getcurpos(fin)
                c = read1(fin)
                if c == '/':    # ignoring single line comment
                    while c != '\n' and not not c:
                        c = read1(fin)

                elif c == '*':  # ignoring multi line comment
                    while True:
                        c = read1(fin)
                        curpos = getcurpos(fin)
                        if c == '*':
                            c = read1(fin)
                            if c == '/':
                                break
                            else:
                                setcurpos(fin, curpos)
                        elif not c:
                            break
                else:
                    setcurpos(fin, curpos)

            elif c == '"':  # ignoring string
                while True:
                    c = read1(fin)
                    if c == '\\':
                        c = read1(fin)
                    elif c == '"':
                        break
                    elif not c:
                        break

            elif c == '#':
                word = ''
                c = read1(fin)
                while iswhitespace(c):
                    c = read1(fin)
                while isalnum(c):
                    word += c
                    c = read1(fin)
                if word == 'include':
                    word = ''
                    while c != '"' and c != '<':
                        c = read1(fin)
                    c = read1(fin)
                    while c != '"' and c != '>':
                        word += c
                        c = read1(fin)
                    includes.append(get_filename_from_path(word))
    return includes


# -------------------------------------------------------
# ----- functions to get filepaths from a folder(s) -----
# -------------------------------------------------------

from os import listdir
from os.path import isfile
from re import split

def myjoin(a:str, b:str):
    split_a = split(r'[/\\]', a)
    split_b = split(r'[/\\]', b)
    joined_splits = [x for x in split_a if x != ''] + [x for x in split_b if x != '']
    joined = '/'.join(joined_splits)
    return joined

def get_filepaths_in_folder(folderpath:str, ignore:List[str], recursive:bool=False) -> List[str]:
    print('get_filepaths_in_folder:', folderpath)
    list_filepaths = []
    for f in listdir(folderpath):
        if f not in ignore:
            f_path = myjoin(folderpath, f)
            if isfile(f_path):
                list_filepaths.append(myjoin(folderpath, f))
            elif recursive:
                list_filepaths += get_filepaths_in_folder(f_path, ignore, recursive)

    return list_filepaths


def get_filepaths_in_folders(folderpaths:List[str], ignore:List[str], recursive:bool=False) -> List[str]:
    print('get_filepaths_in_folders')
    list_filepaths = []
    for folderpath in folderpaths:
        list_filepaths += get_filepaths_in_folder(folderpath, ignore, recursive)
    return list_filepaths


# -----------------------------------------------------------
# ----- function to get dependent-dependency tuple list -----
# -----------------------------------------------------------

from typing import Tuple

def get_dependent_dependeny_tuple_list(folderpaths:List[str], ignore:List[str] = [], ignore_outside_files:bool = False, recursive:bool = False) -> List[Tuple[str, str]]:
    print('get_dependent_dependeny_tuple_list')
    dependent_dependency_tuple_list = []
    filepaths = []
    inside_files = []

    for filepath in get_filepaths_in_folders(folderpaths, ignore, recursive):
        filepaths.append(filepath)
        inside_files.append(get_filename_from_path(filepath))

    for filepath in filepaths:
        includes = get_includes(filepath)
        for include in includes:
            if include not in ignore and (not ignore_outside_files or include in inside_files):
                dependent_dependency_tuple_list.append((get_filename_from_path(filepath), include))
    
    print('Returning dependent_dependency_tuple_list')
    return dependent_dependency_tuple_list