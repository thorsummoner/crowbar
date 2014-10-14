#!python2

print('hello wotld')
import gamelib
from pprint import pprint

mymap = gamelib.TF2()

with open('demofile', 'w') as demofile:
	demofile.write(str(mymap))
