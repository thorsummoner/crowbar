#!/c/Python27/python.exe

from xml.dom import minidom
from pprint import pprint, pformat

FILE = "C:\Users\dylang\Desktop\menu_test\Valve+Developer+Community-20140920004156.xml"

xmldoc = minidom.parse(FILE)
pages = xmldoc.getElementsByTagName('page')
pprint(pages)
help(pages[0])
# print itemlist[0].attributes['name'].value
# for page in pages:
#     pprint(page.nodeValue)
