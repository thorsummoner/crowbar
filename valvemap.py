
from pprint import pprint

class ValveDict(dict):
	def __str__(self):
		out = ''
		for key, value in self.items():
			out += '\t"%s" "%s"\n' % (key, value)
		return out

	def __repr__(self):
		return self.__str__()

class ValveMap(ValveDict):

	mapversion = 0

	def __init__(self, *args, **kw):
		super(ValveMap, self).__init__(*args, **kw)
		self.itemlist = super(ValveMap, self).keys()

		self['versioninfo'] = ValveDict({"editorversion": 400, "editorbuild": 6550, "mapversion": self.mapversion, "formatversion": 100, "prefab": 0, })
		self['viewsettings'] = ValveDict({"bSnapToGrid": 1, "bShowGrid": 1, "bShowLogicalGrid": 0, "nGridSpacing": 64, "bShow3DGrid": 0, })
		self['world'] = ValveDict({"id": 1, "mapversion": self.mapversion, "classname": "worldspawn", "skyname": None, "maxpropscreenwidth": -1, "detailvbsp": None, "detailmaterial": None, })
		self['cameras'] = ValveDict({"activecamera": -1, })
		self['cordon'] = ValveDict({"mins": (-1024, -1024, -1024), "maxs": ( 1024,  1024,  1024), "active": 0, })

		if None == self['world']['mapversion']:
			self['world']['mapversion'] = self['versioninfo']['mapversion']

	def __str__(self):
		out = ''
		for key, value in self.items():
			out += '%s\n{\n%s}\n' % (key, value)
		return out

	def save(self):
		self.mapversion += 1
		self['versioninfo']['mapversion'] = self.mapversion
		self['world']['mapversion'] = self.mapversion
#
# TEST
#

#!python2
if __name__ == '__main__':
	print('hello wotld')
	import gamelib

	mymap = gamelib.TF2()
	mymap.save()

	with open('demofile.vmf', 'w') as demofile:
		print(str(mymap))
		demofile.write(str(mymap))
