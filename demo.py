from lazy_assertion import *

if __name__ == "__main__":

    demo_no = 0

    if demo_no == 0:
        this_true(unique(1, 2, 2) & (empty([]) | equal(2, 2, 2)) & exists("abc.png"))
    else:
        all_true(unique(1, 2, 2) & empty([]), equal(2, 2, 2) | exists("abc.png"))
