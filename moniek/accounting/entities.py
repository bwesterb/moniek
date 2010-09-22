import decimal
import functools

from pymongo.son import SON

from django.db.models import permalink

from moniek.accounting.mongo import db, SONWrapper

ecol = db['entities']

def decimal_to_pair(dec):
	if dec._exp >= 0:
		return (0, int(dec))
	return (-dec._exp, int(dec*(10**-dec._exp)))

def pair_to_decimal(pair):
	return decimal.Decimal(pair[1]) / (10**pair[0])

def by_id(n):
	return entity(ecol.find_one({'_id': n}))

def all():
	for m in ecol.find():
		yield entity(m)

def entity(d):
	return TYPE_MAP[d['type']](d)

class Entity(SONWrapper):
	def __init__(self, data):
		super(Entity, self).__init__(data, ecol)
	@property
	def type(self):
		return self._data['type']
	@property
	def id(self):
		return str(self._id)
	@property
	def _id(self):
		return self._id
	#@permalink
	#def get_absolute_url(self):
	#	return ('entity-by-id', (), {'_id': self.id})

	def get_name(self):
		return self._data['name']
	def set_name(self, value):
		self._data['name'] = value
	name = property(get_name, set_name)


	def get_description(self):
		return self._data['description']
	def set_description(self, value):
		self._data['description'] = value
	description = property(get_description, set_description)

	def __repr__(self):
		return "<Entity %s (%s)>" % (self.id, self.type)

	def as_account(self): return Account(self._data)
	def as_commodity(self): return Commodity(self._data)
	def as_mutation(self): return Mutation(self._data)
	def as_transaction(self): return Transaction(self._data)
	def as_commodityClass(self): return CommodityClass(self._data)


class Account(Entity):
	def get_parent(self):
		return by_id(self._data['parent'])
	def set_parent(self, value):
		self._data['parent'] = value._id
	parent = property(get_parent, set_parent)

	@property
	def children(self):
		return map(entity, ecol.find({'parent': self._id,
					      'type': T_ACCOUNT}))

class Commodity(Entity):
	def get_class(self):
		return by_id(self._data['class'])
	def set_class(self, value):
		self._data['class'] = value._id
	klass = property(get_class, set_class)

	@property
	def valuations(self):
		return dict((k,pair_to_decimal(v))
				for k, v in self._data['valuations'])

class Amount(object):
	def __init__(self, data):
		self._data = dict()

	def __repr__(self):
		return "Amount(%s)" % repr(self._data)

	@staticmethod
	def _coordwise_op(op, args):
		data = {}
		comids = set()
		for arg in args:
			comids.extend(arg._data.iterkeys())
		for comid in comids:
			data[comid] = op(*[arg._data[comid] for arg in args
					if comid in arg._data])
		return Amount(data)

	@staticmethod
	def add(*summands):
		cw_binadd = lambda x,y: x+y
		cw_add = lambda *sms: reduce(cw_binadd, sms, 0) 
		return _coordwise_op(cw_add, summands)

	def __add__(self, other):
		Amount.add(self, other)

	def scale(self, scalar):
		scale_op = lambda val: scalar * val 
		return _coordwise_op(scale_op, (self,))

	def __rmul__(self, scalar):
		self.scale(scalar)


class Mutation(Entity):
	def get_account(self):
		return by_id(self._data['account'])
	def set_account(self, value):
		self._data['account'] = value._id
	account = property(get_account, set_account)

	def get_transaction(self):
		return by_id(self._data['transaction'])
	def set_transaction(self, value):
		self._data['transaction'] = value._id
	transaction = property(get_transaction, set_transaction)

	def get_value(self):
		return Amount(self._data['value'])
	def set_value(self, value):
		self._data['value'] = value._data
	value = property(get_value, set_value)

class Transaction(Entity):
	pass

class CommodityClass(Entity):
	pass

T_ACCOUNT = 'ac'
T_COMMODITY = 'cm'
T_MUTATION = 'mt'
T_TRANSACTION = 'tx'
T_COMMODITY_CLASS = 'cc'

TYPE_MAP = {
	T_ACCOUNT: Account,
	T_COMMODITY: Commodity,
	T_MUTATION: Mutation,
	T_TRANSACTION: Transaction,
	T_COMMODITY_CLASS: CommodityClass,
}

def of_type(t):
	for m in ecol.find({'type': t}):
		yield TYPE_MAP[t](m)

accounts = functools.partial(of_type, T_ACCOUNT)
commodities = functools.partial(of_type, T_COMMODITY)
mutations = functools.partial(of_type, T_MUTATION)
transactions = functools.partial(of_type, T_TRANSACTION)
commodityClasses = functools.partial(of_type, T_COMMODITY_CLASS)

def prepare_database():
	ecol.ensure_index('type')
	ecol.ensure_index('parent')
	ecol.ensure_index('account')
	ecol.ensure_index('transaction')
	db['entityCounter'].remove()
	db['entityCounter'].insert({'x':0})

def next_id():
	result = db.command(SON((
		('findandmodify', 'entityCounter'),
		('query', {}),
		('upsert', True),
		('update', {'$inc': {'x': 1}}))))
	return int(result['value']['x'])
