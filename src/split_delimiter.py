from textnode import TextNode, text_type_enum
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for elem in old_nodes:
        if elem.text_type != text_type_enum.type_text:
            new_nodes.append(elem)
            continue
        new_text = ""
        split_nodes = []
        if delimiter in elem.text:
            new_text = elem.text.split(delimiter)
            if len(new_text) % 2 == 0:
                raise ValueError("Invalid Markdown syntax, must close delimiter")
            for i in range(0, len(new_text)):
                if new_text[i] == "":
                    continue
                if i%2 != 0:
                    split_nodes.append(TextNode(new_text[i], text_type))
                else:
                    split_nodes.append(TextNode(new_text[i], text_type_enum.type_text))
        else:
            raise Exception("Delimiter not found in text")
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for elem in old_nodes:
        if elem.text_type != text_type_enum.type_text:
            new_nodes.append(elem)
            continue
        og_text = elem.text
        image_matches = extract_markdown_images(elem.text)
        if len(image_matches) == 0:
            new_nodes.append(elem)
            continue
        for image in image_matches:
            sections = og_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, not closure for image section")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_enum.type_text))
            new_nodes.append(TextNode(image[0], text_type_enum.type_image, image[1]))
            og_text = sections[1]
        if og_text != "":
            new_nodes.append(TextNode(og_text, text_type_enum.type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for elem in old_nodes:
        if elem.text_type != text_type_enum.type_text:
            new_nodes.append(elem)
            continue
        og_text = elem.text
        link_matches = extract_markdown_links(og_text)
        if len(link_matches) == 0:
            new_nodes.append(elem)
            continue
        for link in link_matches:
            sections = og_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, not closure for link section")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_enum.type_text))
            new_nodes.append(TextNode(link[0], text_type_enum.type_link, link[1]))
            og_text = sections[1]
        if og_text != "":
            new_nodes.append(TextNode(og_text, text_type_enum.type_text))
    return new_nodes