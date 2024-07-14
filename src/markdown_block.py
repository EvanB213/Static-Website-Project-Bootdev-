from enum import Enum
from htmlnode import *
from textnode import *
from split_delimiter import text_to_textnodes

class block_type(Enum):
    block_type_paragraph = "paragraph"
    block_type_heading = "heading"
    block_type_code = "code"
    block_type_quote = "quote"
    block_type_unorder_list = "unordered_list"
    block_type_order_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    text = markdown.split("\n\n")
    for line in text:
        if len(line) == 0:
            continue
        else:
            blocks.append(line.strip())
    return blocks

def block_to_block_type(markdown):
    text = markdown.split("\n")
    if (markdown.startswith("# ") or markdown.startswith("## ") or markdown.startswith("### ") or markdown.startswith("#### ") or
        markdown.startswith("##### ") or markdown.startswith("###### ")):
        return block_type.block_type_heading
    if len(text) > 1 and text[0].startswith("```") and text[-1].endswith("```"):
        return block_type.block_type_code
    if markdown.startswith(">"):
        for line in text:
            if not line.startswith(">"):
                return block_type.block_type_paragraph
        return block_type.block_type_quote
    if markdown.startswith("* "):
        for line in text:
            if not line.startswith("* "):
                return block_type.block_type_paragraph
        return block_type.block_type_unorder_list
    if markdown.startswith("- "):
        for line in text:
            if not line.startswith("- "):
                return block_type.block_type_paragraph
        return block_type.block_type_unorder_list
    if markdown.startswith("1. "):
        i = 1
        for line in text:
            if not line.startswith(f"{i}. "):
                return block_type.block_type_paragraph
            i += 1
        return block_type.block_type_order_list
    return block_type.block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        html_node = block_to_html_node(block)
        child_nodes.append(html_node)
    return ParentNode("div", child_nodes, None)

def block_to_html_node(block):
    type = block_to_block_type(block)
    if type == block_type.block_type_paragraph:
        return paragraph_to_node(block)
    if type == block_type.block_type_heading:
        return heading_to_node(block)
    if type == block_type.block_type_code:
        return code_to_node(block)
    if type == block_type.block_type_quote:
        return quote_to_node(block)
    if type == block_type.block_type_unorder_list:
        return unorder_list_to_node(block)
    if type == block_type.block_type_order_list:
        return order_list_to_node(block)
    return ValueError("Invalid block type")

def text_to_child(text):
    child_notes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        child_notes.append(html_node)
    return child_notes

def paragraph_to_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    child_nodes = text_to_child(paragraph)
    return ParentNode("p", child_nodes)

def heading_to_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    child_nodes = text_to_child(text)
    return ParentNode(f"h{level}", child_nodes)

def code_to_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    child_nodes = text_to_child(text)
    code = ParentNode("code", child_nodes)
    return ParentNode("pre", [code])

def quote_to_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    child_nodes = text_to_child(content)
    return ParentNode("blockquote", child_nodes)

def unorder_list_to_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        child_nodes = text_to_child(text)
        html_items.append(ParentNode("li", child_nodes))
    return ParentNode("ul", html_items)

def order_list_to_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        child_nodes = text_to_child(text)
        html_items.append(ParentNode("li", child_nodes))
    return ParentNode("ol", html_items)