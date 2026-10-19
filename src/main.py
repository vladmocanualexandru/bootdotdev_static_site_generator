import sys

from textnode import TextNode, TextType
from utils import copy_contents, generate_pages_recursive



def main():
    basepath = sys.argv[1] if len(sys.argv)>1 else "/"

    copy_contents("./static", "./docs")
    generate_pages_recursive("./content", "template.html", "./docs", basepath)

main()
