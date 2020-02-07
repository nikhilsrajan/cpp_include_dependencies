from typing import Dict, List, Tuple
from graphviz import Digraph

def get_slope_intercept(x1:float, x2:float, y1:float, y2:float) -> [float, float]:
    slope = (y1 - y2) / (x1 - x2)
    intercept = (y2*x1 - y1*x2) / (x1 - x2)
    return slope, intercept


def normalize_dependency_count(dependency_count:Dict[str, int], normalize_min:int, normalize_max:int) -> Dict[str, int]:
    print('normalize_dependency_count')
    dependency_counts = dependency_count.values()
    normalized_dependency_count = dict()
    max_count = max(dependency_counts)
    min_count = min(dependency_counts)
    slope, intercept = get_slope_intercept(min_count, max_count, normalize_min, normalize_max)
    for key, value in dependency_count.items():
        normalized_dependency_count[key] = round(slope*value + intercept)
    return normalized_dependency_count


def get_dependency_count(dependent_dependeny_tuple_list:List[Tuple[str, str]]) -> Dict[str, int]:
    print('get_dependency_count')
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


def draw_dependency_chart(dependent_dependeny_tuple_list:List[Tuple[str, str]], draw_format:str='pdf', export_name:str='dependency_chart') -> None:
    print('draw_dependency_chart')
    if len(dependent_dependeny_tuple_list) == 0:
        print('Error: dependent_dependeny_tuple_list is empty. No dependency chart to draw.')
        return

    dependency_count = normalize_dependency_count(get_dependency_count(dependent_dependeny_tuple_list), 1, 9)

    d = Digraph(export_name, filename=export_name, node_attr={'colorscheme': 'orrd9', 'style': 'filled', 'shape' : 'record'})
    
    for nodename, d_count in dependency_count.items():
        d.node(nodename, fillcolor=str(d_count))

    for cur_tuple in dependent_dependeny_tuple_list:
        dependent = list(cur_tuple)[0]
        dependency = list(cur_tuple)[1]
        d.edge(dependent, dependency)
    
    print('Drawing dependency chart')
    d.render(view=True, format=draw_format)