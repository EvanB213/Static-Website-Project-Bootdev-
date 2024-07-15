import shutil
import os

from markdown_block import *

def copy_dir(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    
    for file in os.listdir(source_dir):
        from_path = os.path.join(source_dir, file)
        dest_path = os.path.join(dest_dir, file)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_dir(from_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    from_file = open(from_path, 'r')
    from_markdown = from_file.read()
    from_file.close()

    temp_file = open(template_path, 'r')
    template = temp_file.read()
    temp_file.close()

    node = markdown_to_html_node(from_markdown)
    html = node.to_html()

    title = extract_title(from_markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    pass
