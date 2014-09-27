import datetime

class Entry(object):
	def __init__(self, body):

		self.created_at = datetime.datetime.now()
		self.title = "%s" % self.created_at 
		self.body = body

	def __str__(self):
		return "Title: %s\nCreatedAt: %s\nBody:\n%s" % (self.title, self.created_at, self.body)

