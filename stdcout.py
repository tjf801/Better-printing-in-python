import ctypes

destructor = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.c_void_p)
getattrfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.c_char_p)
setattrfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.c_char_p, ctypes.py_object)
reprfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object)
binaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object)
ternaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object)
unaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object)
inquiry = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object)

class PyTypeObject(ctypes.Structure):
	_fields_ = (
		('ob_refcnt', ctypes.c_ssize_t),
		('ob_type', ctypes.POINTER(ctypes.c_void_p)), # PyTypeObject*
		
		('ob_size', ctypes.c_ssize_t),
		
		('tp_name', ctypes.c_char_p),
		('tp_basicsize', ctypes.c_ssize_t),
		('tp_itemsize', ctypes.c_ssize_t),
		
		('tp_dealloc', destructor), 
		('tp_vectorcall_offset', ctypes.c_ssize_t),
		('tp_getattr', getattrfunc),
		('tp_setattr', setattrfunc),
		
		('tp_as_async', ctypes.c_void_p),
		
		('tp_repr', reprfunc),
		
		('tp_as_number', ctypes.c_void_p), # PyNumberMethods*
		('tp_as_sequence', ctypes.c_void_p), # PySequenceMethods*
		('tp_as_mapping', ctypes.c_void_p), # PyMappingMethods*
		
		('tp_hash', inquiry),
		('tp_call', ternaryfunc),
		('tp_str', unaryfunc),
		('tp_getattro', getattrfunc),
		('tp_setattro', setattrfunc),
		
		('tp_as_buffer', ctypes.c_void_p), # PyBufferProcs*
		
		('tp_flags', ctypes.c_uint),
		('tp_doc', ctypes.c_char_p),
		
		('tp_traverse', ctypes.c_void_p),
		('tp_clear', ctypes.c_void_p),
		
		('tp_richcompare', ctypes.c_void_p),
		('tp_weaklistoffset', ctypes.c_ssize_t),
		('tp_iter', ctypes.c_void_p),
		('tp_iternext', ctypes.c_void_p),
		('tp_methods', ctypes.c_void_p),
		('tp_members', ctypes.c_void_p),
		('tp_getset', ctypes.c_void_p),
		('tp_base', ctypes.c_void_p),
		
		('tp_dict', ctypes.py_object),
		# TODO: rest of fields
	)

class PyNumberMethods(ctypes.Structure):
	_fields_ = (
		('nb_add', binaryfunc),
		('nb_subtract', binaryfunc),
		('nb_multiply', binaryfunc),
		('nb_remainder', binaryfunc),
		('nb_divmod', binaryfunc),
		('nb_power', ternaryfunc),
		('nb_negative', unaryfunc),
		('nb_positive', unaryfunc),
		('nb_absolute', unaryfunc),
		('nb_bool', inquiry),
		('nb_invert', unaryfunc),
		('nb_lshift', binaryfunc),
		('nb_rshift', binaryfunc),
		# TODO: rest of fields
	)



def main():
	import sys, io
	
	def operator_lshift(self: io.TextIOWrapper, other: object) -> io.TextIOWrapper:
		self.write(str(other))
		return self
	
	textio_wrapper_ptr = ctypes.cast(ctypes.c_void_p(id(io.TextIOWrapper)), ctypes.POINTER(PyTypeObject))
	
	textio_as_number = PyNumberMethods(nb_lshift=binaryfunc(operator_lshift))
	
	textio_wrapper_ptr.contents.tp_dict = ctypes.cast(ctypes.c_void_p(), ctypes.py_object)
	textio_wrapper_ptr.contents.tp_flags = ctypes.c_uint32(0)
	textio_wrapper_ptr.contents.tp_as_number = ctypes.cast(ctypes.pointer(textio_as_number), ctypes.c_void_p)
	
	ctypes.pythonapi.PyType_Ready(textio_wrapper_ptr)
	
	sys.stdout << "Hello, world!" << '\n'

if __name__=="__main__": main()