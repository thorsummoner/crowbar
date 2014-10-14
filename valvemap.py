
from pprint import pprint

class ValveDict(dict):
	def __init__(self, *args, **kw):
		super(ValveDict, self).__init__(*args, **kw)
		self.itemlist = super(ValveDict, self).keys()

	def __str__(self):
		out = ''
		for key, value in self.items():
			out += '\t"%s" "%s"\n' % (key, value)
		return out

	def __repr__(self):
		return self.__str__()

class ValveMap(object):
	"""ValveMap File Handler"""

	_versioninfo = ValveDict({"editorversion": 400, "editorbuild": 6550, "mapversion": 0, "formatversion": 100, "prefab": 0, })
	@property
	def versioninfo(self):
		return self._versioninfo
	@versioninfo.setter
	def versioninfo(self, value):
		self._versioninfo = value

	_viewsettings = ValveDict({"bSnapToGrid": 1, "bShowGrid": 1, "bShowLogicalGrid": 0, "nGridSpacing": 64, "bShow3DGrid": 0, })
	@property
	def viewsettings(self):
		return self._viewsettings
	@viewsettings.setter
	def viewsettings(self, value):
		self._viewsettings = value

	_world = ValveDict({"id": 1, "mapversion": None, "classname": "worldspawn", "skyname": None, "maxpropscreenwidth": -1,
		"detailvbsp": None, "detailmaterial": None, })
	@property
	def world(self):
		return self._world
	@world.setter
	def world(self, value):
		self._world = value

	_cameras = ValveDict({"activecamera": -1, })
	@property
	def cameras(self):
		return self._cameras
	@cameras.setter
	def cameras(self, value):
		self._cameras = value

	_cordon = ValveDict({"mins": (-1024, -1024, -1024), "maxs": ( 1024,  1024,  1024), "active": 0, })
	@property
	def cordon(self):
		return self._cordon
	@cordon.setter
	def cordon(self, value):
		self._cordon = value


	def __init__(
		self,
		versioninfo = None,
		viewsettings  = None,
		world         = None,
		cameras       = None,
		cordon        = None
	):
		super(ValveMap, self).__init__()
		if None != versioninfo: self.versioninfo = versioninfo
		if None != viewsettings:  self.viewsettings  = viewsettings
		if None != world:         self.world         = world
		if None != cameras:       self.cameras       = cameras
		if None != cordon:        self.cordon        = cordon

		if None == self.world['mapversion']:
			self.world['mapversion'] = self.versioninfo['mapversion']

	def __str__(self):
		out = ''
		for i in dir(self):
			if i.startswith('_'):
				continue
			out += '%s\n{\n%s\n}\n' % (i, getattr(self, i))
		return out


#
# TEST
#

#!python2
if __name__ == '__main__':
	print('hello wotld')
	import gamelib

	mymap = gamelib.TF2()

	with open('demofile.vmf', 'w') as demofile:
		print(str(mymap))
		demofile.write(str(mymap))
