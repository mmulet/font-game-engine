from xml.etree.ElementTree import Element, SubElement


def addCharStringToTable(out_subroutineTable: Element, charString: str,
                         index: int) -> None:
    SubElement(out_subroutineTable, "CharString", {
        'index': str(index)
    }).text = charString + "\n" + "return\n"
