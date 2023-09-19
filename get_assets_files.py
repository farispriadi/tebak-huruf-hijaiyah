import pathlib,os

root_path = os.getcwd()
for subdir, dirs, files in os.walk(root_path):
    if "assets" in subdir:
        master_path = pathlib.Path(subdir)
        for file in files:
            full_path =  master_path/pathlib.Path(file)
            full_path = str(full_path).replace("/home/farispriadi/PROJECTS/game-anak/tebak-huruf-hijaiyah/","")
            print("(RELATIVE_PATH + '"+full_path+"', '{}'),".format("/".join(full_path.split("/")[:2])))