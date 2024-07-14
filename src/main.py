import os
import shutil
from copydir import copy_dir

dir_public = "./public"
dir_static = "./static"

def main():
    print("Deleting public directory")
    if os.path.exists(dir_public):
        shutil.rmtree(dir_public)
    
    print("Copying static files to public directory")
    copy_dir(dir_static, dir_public)

main()