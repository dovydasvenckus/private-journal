import datetime

class Entry(object):
	def __init__(self, title, body):
		self.title = title
		self.body = body
		self.created_at = datetime.datetime.now()

	def __str__(self):
		return "Title: %s\nCreatedAt: %s\nBody:\n%s" % (self.title, self.created_at, self.body)

