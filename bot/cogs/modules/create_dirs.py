import os


def create_dirs(paths):
    try:
        for path in list(paths):
            check = os.path.isdir(path)
            if check == False:
                os.makedirs(path)
                
    except:
        pass

