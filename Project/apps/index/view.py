import os
import re

from flask import Blueprint, render_template

index_bp = Blueprint('login', __name__)

class Database():
    base = None
    dirs = None

    def __init__(self):
        self.base = ''
        self.dirs = []
    def update(self, base, dirs):
        self.base = base
        self.dirs = dirs
system_database = Database()

@index_bp.route('/')
def render_earth():
    base = 'static/data'
    dirs = os.listdir(base)
    dirs1 = dirs.copy()

    # region System file format self-checking
    for file_name in dirs1:
        input_path = base + '/' + file_name
        is_standard = True

        if (file_name[-4:] == '.txt' and (' ' in file_name)):
            file_name_pre = file_name[:-4]

            with open(input_path, 'r') as f:
                first_line = f.readline()
                first_line = first_line.strip(' ')
                first_line = re.split(r"[ ]+", first_line)
                if (len(first_line) == 9):
                    is_standard = False

            # Change to the form that tle2czml can read
            if (not is_standard):
                new_tr = []

                with open(input_path, 'r') as f:
                    tr = f.readlines()

                len_tr = len(tr)
                for i in range(int(len_tr / 2)):
                    new_tr.append('\n')
                    new_tr.append(tr[i * 2])
                    new_tr.append(tr[i * 2 + 1])

                with open(input_path, 'w') as f:
                    f.writelines(new_tr)

            # output_path = base + '/' + file_name_pre + '.czml'
        else:
            dirs.remove(file_name)
    # endregion

    system_database.update(base, dirs)

    return render_template('index/index.html')