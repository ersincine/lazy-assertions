from lazy_assertion import *

if __name__ == "__main__":

    demo_no = 2

    if demo_no == 0:
        this_true((empty([]) | equal(2, 2, 2)) & exists("abc.png"))
    elif demo_no == 1:
        all_true(unique(1, 2, 2) & empty([]), equal(2, 2, 2) | exists("abc.png"))
    elif demo_no == 2:
        this_true(exists("abc.png"))
    else:
        x = "A"
        all_true(is_instance(x, str), is_convertible(x, int))
