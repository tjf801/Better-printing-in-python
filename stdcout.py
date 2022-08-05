import typing as _typing
import ctypes

from internals import PyTypeObject, PyNumberMethods, binaryfunc

import io, inspect, os

@_typing.runtime_checkable
class SupportsRLShift(_typing.Protocol):
	__slots__ = ()
	def __rlshift__(self, other: io.IOBase) -> io.IOBase: ...


# c++ ostream write operator
def operator_lshift(self: io.IOBase, other: object) -> io.IOBase:
	# check that self is writable
	if not self.writable():
		raise io.UnsupportedOperation('not writable')
	
	# NOTE: we cannot use the write() method because it gets overrided with different signatures
	# see https://github.com/python/cpython/blob/main/Modules/_io/iobase.c#:~:text=%22Even%20though%20IOBase,called.%5Cn%22
	
	# if the other type has a custom support for rlshift, use that instead
	# otherwise, fall back to the default implementation
	if isinstance(other, SupportsRLShift):
		result = other.__rlshift__(self)
		if result is not NotImplemented:
			return result
	
	# check if other is a stream manipulator function like endl
	# (must be a callable that takes a single positional argument)
	# NOTE: this will raise an exception if other does not return an IOBase
	elif callable(other):
		sig = inspect.signature(other)
		if len(sig.parameters) == 1:
			param = list(inspect.signature(other).parameters.values())[0]
			if param.kind in ( 
				inspect.Parameter.POSITIONAL_ONLY,
				inspect.Parameter.POSITIONAL_OR_KEYWORD,
				inspect.Parameter.VAR_POSITIONAL,
			) and param.default == inspect.Parameter.empty:
				# call the function with the stream as the first argument
				result = other(self)
				if not isinstance(result, io.IOBase):
					raise TypeError('IO manipulator function must return an IOBase object')
				return result
	
	# if the other type is raw bytes, just write it directly
	if isinstance(other, bytes):
		self.writelines((other,))
	
	# if the other type supports the buffer protocol, write it directly
	# TODO
	
	# if the other type supports __bytes__, write it directl
	# TODO: is this desired behavior?
	elif isinstance(other, _typing.SupportsBytes):
		self.writelines((other.__bytes__(),))
	
	# if self is a TextIO, we can use strings
	elif isinstance(self, (io.TextIOBase, io.TextIOWrapper)):
		# if the other type is a string, write it directly
		if isinstance(other, str):
			self.write(other)
		
		# otherwise convert the other type to a string
		else: self.write(str(other))
	
	# otherwise, the other type is not supported
	else:
		return NotImplemented
	
	# return self to allow chaining
	return self


# c++ istream read operator
# TODO: make this one good too
_T = _typing.TypeVar("_T")
def operator_rshift(self: io.TextIOWrapper, other: _typing.Type[_T]) -> _T:
	return other(self.readline())


Py_TPFLAGS_HEAPTYPE = (1 << 9)
Py_TPFLAGS_BASETYPE = (1 << 10)
Py_TPFLAGS_READY = (1 << 12)
Py_TPFLAGS_HAVE_GC = (1 << 14)

def overwrite_shift_operators():
	priv_io = io._io
	
	# overwrite io.IOBase with the new operators
	
	iobase_type_ptr = ctypes.cast(ctypes.c_void_p(id(priv_io._IOBase)), ctypes.POINTER(PyTypeObject))
	
	iobase_number_methods = PyNumberMethods(
		nb_lshift=binaryfunc(operator_lshift),
		nb_rshift=binaryfunc(operator_rshift),
	)
	iobase_type_ptr.contents.tp_dict = ctypes.cast(ctypes.c_void_p(), ctypes.py_object)
	iobase_type_ptr.contents.tp_flags = ctypes.c_uint32(
		Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC
	)
	iobase_type_ptr.contents.tp_as_number = ctypes.cast(ctypes.pointer(iobase_number_methods), ctypes.c_void_p)
	
	# reinitialize the IOBase type object
	ctypes.pythonapi.PyType_Ready(iobase_type_ptr)
	
	# pretty much reinitialize the entire io module
	for ty in (
		priv_io._BufferedIOBase,
		priv_io._RawIOBase,
		priv_io._TextIOBase,
		
		priv_io.BytesIO,
		priv_io.BufferedReader,
		priv_io.BufferedWriter,
		priv_io.BufferedRWPair,
		priv_io.BufferedRandom,
		
		priv_io.FileIO,
		# priv_io._BytesIOBuffer
		
		priv_io._WindowsConsoleIO,
		
		priv_io.StringIO,
		priv_io.TextIOWrapper):
		type_ptr = ctypes.cast(ctypes.c_void_p(id(ty)), ctypes.POINTER(PyTypeObject))
		
		type_ptr.contents.tp_dict = ctypes.cast(ctypes.c_void_p(), ctypes.py_object)
		type_ptr.contents.tp_bases = ctypes.cast(ctypes.c_void_p(), ctypes.py_object)
		type_ptr.contents.tp_flags = ctypes.c_uint32(type_ptr.contents.tp_flags & ~Py_TPFLAGS_READY)
		
		ctypes.pythonapi.PyType_Ready(type_ptr)

# run the function on import
overwrite_shift_operators()


# TODO: add this to sys module
_IO = _typing.TypeVar('_IO', bound=io.IOBase)	
def endl(stream: _IO) -> _IO:
	# TODO: does c++ actually use the correct line separator or just '\n'?
	stream.write(os.linesep)
	stream.flush()
	return stream


if __name__=="__main__":
	import sys
	
	sys.stdout << "Hello, world!" << endl
	
	x = sys.stdin >> int
	print(x+1)