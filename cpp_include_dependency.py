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
    return fin.read(1)


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
                    while c != '\n' and c:
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
                else:
                    setcurpos(fin, curpos)

            elif c == '"':  # ignoring string
                while True:
                    c = read1(fin)
                    if c == '\\':
                        c = read1(fin)
                    elif c == '"':
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
from os.path import isfile, join

def get_filepaths_in_folder(folderpath:str, ignore_files:List[str]) -> List[str]:
    list_filepaths = []
    for f in listdir(folderpath):
        if f not in ignore_files:
            if isfile(join(folderpath, f)):
                list_filepaths.append(join(folderpath, f))
    return list_filepaths


def get_filepaths_in_folders(folderpaths:List[str], ignore_files:List[str]) -> List[str]:
    list_filepaths = []
    for folderpath in folderpaths:
        list_filepaths += get_filepaths_in_folder(folderpath, ignore_files)
    return list_filepaths


# -----------------------------------------------------------
# ----- function to get dependent-dependency tuple list -----
# -----------------------------------------------------------

from typing import Tuple

def get_dependent_dependeny_tuple_list(folderpaths:List[str], ignore_files:List[str] = [], ignore_outside_files:bool = False) -> List[Tuple[str, str]]:
    dependent_dependency_tuple_list = []
    filepaths = []
    inside_files = []

    for filepath in get_filepaths_in_folders(folderpaths, ignore_files):
        filepaths.append(filepath)
        inside_files.append(get_filename_from_path(filepath))

    for filepath in filepaths:
        includes = get_includes(filepath)
        for include in includes:
            if include not in ignore_files and (not ignore_outside_files or include in inside_files):
                dependent_dependency_tuple_list.append((get_filename_from_path(filepath), include))
    
    return dependent_dependency_tuple_list


# ------------------------------
# ----- printing functions -----
# ------------------------------

def print_list(mylist:list) -> None:
    for item in mylist:
        print(item)


# ---------------------------------
# ----- draw dependency chart -----
# ---------------------------------

from typing import Dict
from graphviz import Digraph

def get_slope_intercept(x1:float, x2:float, y1:float, y2:float) -> [float, float]:
    slope = (y1 - y2) / (x1 - x2)
    intercept = (y2*x1 - y1*x2) / (x1 - x2)
    return slope, intercept


def normalize_dependency_count(dependency_count:Dict[str, int], normalize_min:int, normalize_max:int) -> Dict[str, int]:
    dependency_counts = dependency_count.values()
    normalized_dependency_count = dict()
    max_count = max(dependency_counts)
    min_count = min(dependency_counts)
    slope, intercept = get_slope_intercept(min_count, max_count, normalize_min, normalize_max)
    for key, value in dependency_count.items():
        normalized_dependency_count[key] = round(slope*value + intercept)
    return normalized_dependency_count


def get_dependency_count(dependent_dependeny_tuple_list:List[Tuple[str, str]]) -> Dict[str, int]:
    dependency_count = dict()

    # init
    for cur_tuple in dependent_dependeny_tuple_list:
        dependent = list(cur_tuple)[0]
        dependency = list(cur_tuple)[1]
        dependency_count[dependent] = 0
        dependency_count[dependency] = 0

    for cur_tuple in dependent_dependeny_tuple_list:
        dependency = list(cur_tuple)[1]
        dependency_count[dependency] += 1

    return dependency_count


def draw_dependency_chart(dependent_dependeny_tuple_list:List[Tuple[str, str]]) -> None:
    project_name = 'dependency_chart'
    export_path = project_name

    dependency_count = normalize_dependency_count(get_dependency_count(dependent_dependeny_tuple_list), 1, 9)

    d = Digraph(project_name, filename=export_path, node_attr={'colorscheme': 'orrd9', 'style': 'filled', 'shape' : 'record'})
    
    for nodename, d_count in dependency_count.items():
        d.node(nodename, fillcolor=str(d_count))

    for cur_tuple in dependent_dependeny_tuple_list:
        dependent = list(cur_tuple)[0]
        dependency = list(cur_tuple)[1]
        d.edge(dependent, dependency)
    
    d.render(view=True)
        

# ---------------
# ----- run -----
# ---------------

folderpaths = [
    '/home/ess-017/Repository/EssCore/code/source/include/',
    '/home/ess-017/Repository/EssCore/code/source/src/',
]

ignore_files = [
    'Export.h'
]

ignore_outside_files = True

dd_tuple_list = get_dependent_dependeny_tuple_list(folderpaths, ignore_files, ignore_outside_files)

draw_dependency_chart(dd_tuple_list)

