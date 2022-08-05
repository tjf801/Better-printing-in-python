"Internal CPython implementation details used by the C API, made in python"

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
		('tp_descr_get', ctypes.c_void_p),
		('tp_descr_set', ctypes.c_void_p),
		('tp_dictoffset', ctypes.c_ssize_t),
		('tp_init', ctypes.c_void_p),
		('tp_alloc', ctypes.c_void_p),
		('tp_new', ctypes.c_void_p),
		('tp_free', ctypes.c_void_p),
		('tp_is_gc', ctypes.c_void_p),
		('tp_bases', ctypes.py_object),
		('tp_mro', ctypes.py_object),
		# TODO: rest of fields
	)

"""descrgetfunc tp_descr_get;
    descrsetfunc tp_descr_set;
    Py_ssize_t tp_dictoffset;
    initproc tp_init;
    allocfunc tp_alloc;
    newfunc tp_new;
    freefunc tp_free; /* Low-level free-memory routine */
    inquiry tp_is_gc; /* For PyObject_IS_GC */
    PyObject *tp_bases;
    PyObject *tp_mro; /* method resolution order */"""

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

