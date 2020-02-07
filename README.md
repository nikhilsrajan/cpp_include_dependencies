# cpp_include_dependencies
Python3 script to extract include dependencies in a CPP project

## How to use
```
from cpp_include_dependency import get_dependent_dependeny_tuple_list
from draw_dependency_chart import draw_dependency_chart

# List of folders of whose files' include dependencies are to be extracted
folderpaths = [
    '/path/to/project/include/',
    '/path/to/project/src/',
    '/path/to/project/tests/'
]

# List of files to be ignored
# Useful when there are files that are included in every file
ignore_files = [
    'included_almost_everywhere.h',
    'catch.hpp'
]

# Option to ignore files not contained in the aforementioned folders
# This is useful in making the result less noisy by ignoring stdlib files
ignore_outside_files = True

# Get the dependencies as a list of (str, str) tuple -- (dependent, dependency)
dd_tuple_list = get_dependent_dependeny_tuple_list(folderpaths, ignore_files, ignore_outside_files)

# Draw dependency using graphviz and export as specified format
# The nodes are color coloured from white to dark red based on how many files have included it
draw_dependency_chart(dd_tuple_list, 'pdf')
```

## Dependencies
### cpp_include_dependency.py
- ```from typing import List, Tuple```
- ```from os import listdir```
- ```from os.path import isfile, join```
### draw_dependency_chart.py
- ```from typing import Dict, List, Tuple```
- ```from graphviz import Digraph```

