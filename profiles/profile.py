class Profile(object):
	"""A Game profile dialog"""

	"""Profile name, used for display and saving purposes."""
	self._name = str()
	property
	def name(self):
	    return self._name
	@name.setter
	def name(self, value):
	    self._name = value

	def __init__(self):
		super(Profile, self).__init__()

