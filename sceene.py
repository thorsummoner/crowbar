
class Sceene(object):
	"""docstring for SCeene"""

	LABEL = 'uninitialized'

	AXIES = 'xyz'

	def __init__(self, orientation):
		super(Sceene, self).__init__()
		self.orientation = [c for c in orientation if c in self.AXIES]

		if len(self.orientation) != 2:
			raise TypeError(
				'Invalid orientation `%s` (%s)' % (
					orientation, self.orientation
				)
			)

		self.LABEL = '/'.join(self.orientation)



