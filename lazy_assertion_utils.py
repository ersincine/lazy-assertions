import os
from itertools import combinations
from tree_printer import generate_tree_representation, TextColor, colorize_str


def generate_all_results(lazy_assertions):
    results = []
    message_trees = []
    true_count = 0
    for assertion in lazy_assertions:
        result, message_tree = assertion.evaluate()
        results.append(result)
        message_trees.append(message_tree)
        if result:
            true_count += 1
    return results, message_trees, true_count


def generate_error_message(*message_trees, expected=None, found=None):
    assert (expected is None) == (found is None)
    error_messages = []
    for message_tree in message_trees:
        lines = [values[1] + values[2] for values in generate_tree_representation(message_tree)]
        error_messages.append("\n".join(lines))
    error_message = ("\n" + "-" * 40 + "\n").join(error_messages)
    if expected is not None:
        error_message = f"Expected: {expected}   |   Found: {found}\n" + error_message
    return error_message


class SimpleLazyAssertion:

    def __init__(self, evaluation_function, *args, **kwargs):
        self.evaluation_function = evaluation_function
        self.args = args
        self.kwargs = kwargs

    def __and__(self, other):
        assert isinstance(other, SimpleLazyAssertion) or isinstance(other, CompoundLazyAssertion)
        return CompoundLazyAssertion(self, "AND", other)

    def __or__(self, other):
        assert isinstance(other, SimpleLazyAssertion) or isinstance(other, CompoundLazyAssertion)
        return CompoundLazyAssertion(self, "OR", other)

    def __invert__(self):
        return CompoundLazyAssertion(self, "NOT")

    def evaluate(self):
        return self.evaluation_function(*self.args, **self.kwargs)


class CompoundLazyAssertion:

    def __init__(self, lhs, operator, rhs=None):
        assert isinstance(lhs, SimpleLazyAssertion) or isinstance(lhs, CompoundLazyAssertion)
        if operator == "NOT":
            assert rhs is None
        else:
            assert operator in ("AND", "OR")
            assert isinstance(rhs, SimpleLazyAssertion) or isinstance(rhs, CompoundLazyAssertion)

        self.lhs = lhs                  # TODO: Maybe we need copy.copy or copy.deepcopy
        self.operator = operator
        self.rhs = rhs                  # TODO: Maybe we need copy.copy or copy.deepcopy
        self.already_evaluated = False  # TODO: Maybe we don't need this.

    def __and__(self, other):
        assert not self.already_evaluated
        return CompoundLazyAssertion(self, "AND", other)

    def __or__(self, other):
        assert not self.already_evaluated
        return CompoundLazyAssertion(self, "OR", other)

    def __invert__(self):
        assert not self.already_evaluated
        return CompoundLazyAssertion(self, "NOT")

    def evaluate(self):
        assert not self.already_evaluated
        self.already_evaluated = True
        if self.operator == "NOT":
            return self.lhs.evaluate()
        else:
            truth1, message_tree1 = self.lhs.evaluate()
            truth2, message_tree2 = self.rhs.evaluate()
            truth = (truth1 and truth2) if self.operator == "AND" else (truth1 or truth2)
            root = colorize_str(self.operator, TextColor.MAGENTA) + " " + get_truth_str(truth)
            children = [message_tree1, message_tree2]
            message_tree = (root, children)
            return truth, message_tree


def get_value_str(value, max_len=30):
    s = repr(value)
    return s if len(s) < max_len else s[:max_len - 3] + "..."


def get_function_call_str(function_name, *args, **kwargs):
    str_values = [get_value_str(value) for value in args]
    for name, value in kwargs.items():
        str_values.append(name + "=" + get_value_str(value))
    function_call_str = function_name + "(" + ", ".join(str_values) + ") "
    return function_call_str


def get_truth_str(truth):
    return colorize_str("[TRUE]" if truth else "[FALSE]", bold=True)


def evaluate_equal(*values):
    truth = all((value == values[0] for value in values))
    message = get_function_call_str("equal", *values) + get_truth_str(truth)
    return truth, message


def evaluate_unique(*values):
    # TODO: Maybe use a set.
    truth = True
    for value1, value2 in combinations(values, 2):
        if value1 == value2:
            truth = False
            break
    message = get_function_call_str("unique", *values) + get_truth_str(truth)
    return truth, message


def evaluate_empty(value):
    truth = len(value) == 0
    message = get_function_call_str("empty", value) + get_truth_str(truth)
    return truth, message


def evaluate_not_empty(value):
    truth = len(value) != 0
    message = get_function_call_str("not_empty", value) + get_truth_str(truth)
    return truth, message


def evaluate_exists(value):
    truth = os.path.exists(value)
    message = get_function_call_str("exists", value) + get_truth_str(truth)
    return truth, message


def evaluate_is_instance(value, type):
    truth = isinstance(value, type)
    message = get_function_call_str("is_instance", value, type) + get_truth_str(truth)
    return truth, message


def evaluate_is_convertible(value, type):
    try:
        type(value)
        truth = True
    except:
        truth = False
    message = get_function_call_str("is_convertible", value, type) + get_truth_str(truth)
    return truth, message

# TODO: get_function_call_str kısımlarını bir ara otomatik yapayım.
