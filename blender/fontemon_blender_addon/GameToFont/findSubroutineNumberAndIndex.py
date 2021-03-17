import bpy
from xml.etree.ElementTree import Element


def findSubroutineNumberAndIndex(subroutine_table):
  # type: (Element) -> bpy.Tuple[int,int]
  number_of_children = len(subroutine_table)
  return (-107 + number_of_children, number_of_children)