import json



def test_encode( object_o ):
	encoding = None
	try:
		encoding= object_o._json()
	except AttributeError:
		encoding = json.JSONEncoder.default(object_o)
	return encoding

def to_json(python_object):         
	if isinstance(python_object, bytes):                                
	    return {'__class__': 'bytes',
		    '__value__': list(python_object)}
	elif isinstance(python_object, Test):
	    return {'__class__': 'Test',
		    '__first_value__': list(python_object.my_bytes),
		    '__second_value__': python_object.my_bool}
	raise TypeError(repr(python_object) + ' is not JSON serializable')

my_bytes = b'\xDE\xD5\xB4\xF8'

class Test():
	def __init__(self):
		self.my_bytes = b'\xDE\xD5\xB4\xF8'
		self.my_bool = True
"""	def default(self, o):
		try:
			iterable = iter(o)
		except TypeError:
			pass
		else:
			return list(iterable)
		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, o)
"""
t = Test()

with open('entry.json', 'w', encoding='utf-8') as f:
    json.dump(t, f, default=test_encode)
#json.dump(my_bytes, default=to_json)
