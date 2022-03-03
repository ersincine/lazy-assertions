Example usage:

	x = 2
	y = 2
	numbers = []
	path = 'abc.png'
	this_true((empty(numbers) | equal(x, y)) & exists(path))

Output:

    AssertionError: Expected: True   |   Found: False
    AND [FALSE]
    ├── OR [TRUE]
    │   ├── empty([]) [TRUE]
    │   └── equal(2, 2) [TRUE]
    └── exists('abc.png') [FALSE]

Without lazy-assertions one could do:

	import os
	x = 2
	y = 2
	numbers = []
	path = 'abc.png'
	assert((numbers == [] or x == y) and os.path.exists(path))
	
The problem is the output:
	
	assert((numbers == [] or x == y) and os.path.exists(path))
	AssertionError

It is not possible to understand what went wrong.
We do not even know what the values of the variables were.
