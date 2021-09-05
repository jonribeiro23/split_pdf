from os import listdir
from os.path import isfile, join

def get_files_name(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

# res = get_files_name('./01-09')

# for i in res:
#     print(i)

