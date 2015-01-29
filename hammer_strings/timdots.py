import pprint
import sys

with open('words', 'r') as read:
	lines = iter(read.readlines())

with open('wordsregex', 'w') as fh:
	try:
		while True:
			line = next(lines)
			fh.write(line.rstrip() + '|')
	except StopIteration as stop:
		pass
