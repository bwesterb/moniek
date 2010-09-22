import pymongo
from django.conf import settings

conn = pymongo.Connection(settings.MONGO_HOST)
db = conn[settings.MONGO_DB]

class SONWrapper(object):
	def __init__(self, data, collection, parent=None):
		self._data = data
		self._collection = collection
		self._parent = parent
	def save(self):
		if self._parent is None:
			self._collection.save(self._data)
		else:
			self._parent.save()
	@property
	def _id(self):
		if self._parent is None:
			return self._data['_id']
		return self._parent._id
	def __repr__(self):
		return "<SONWrapper for %s>" % self._id

