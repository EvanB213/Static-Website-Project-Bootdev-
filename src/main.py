import os
import shutil
from copydir import copy_dir, generate_page_recursive

dir_public = "./public"
dir_static = "./static"
dir_content = "./content"
template_path = "./template.html"

def main():
    print("Deleting public directory")
    if os.path.exists(dir_public):
        shutil.rmtree(dir_public)
    
    print("Copying static files to public directory")
    copy_dir(dir_static, dir_public)

    print("Generating page")
    generate_page_recursive(dir_content, template_path, dir_public)  

main()