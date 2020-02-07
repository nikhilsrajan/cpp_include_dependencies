from cpp_include_dependency import get_dependent_dependeny_tuple_list, draw_dependency_chart

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