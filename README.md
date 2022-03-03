Example usage:

	x = 2
	numbers = []
	path = 'abc.png'
	this_true((empty(numbers) | equal(x, 2)) & exists(path))

Output:

    AssertionError: Expected: True   |   Found: False
    AND [FALSE]
    ├── OR [TRUE]
    │   ├── empty([]) [TRUE]
    │   └── equal(2, 2) [TRUE]
    └── exists('abc.png') [FALSE]


