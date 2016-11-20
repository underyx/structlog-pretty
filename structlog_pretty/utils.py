from xml.dom.minidom import Node


def strip_minidom_whitespace(node):
    """Strips all whitespace from a minidom XML node and its children

    This operation is made in-place."""
    for child in node.childNodes:
        if child.nodeType == Node.TEXT_NODE:
            if child.nodeValue:
                child.nodeValue = child.nodeValue.strip()
        elif child.nodeType == Node.ELEMENT_NODE:
            strip_minidom_whitespace(child)
