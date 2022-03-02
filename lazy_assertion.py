from lazy_assertion_utils import SimpleLazyAssertion, generate_error_message, generate_all_results
import lazy_assertion_utils as assertion


def this_true(lazy_assertion):
    result, message_tree = lazy_assertion.evaluate()
    if result is not True:
        assert False, generate_error_message(message_tree, expected="True", found="False")


def this_false(lazy_assertion):
    result, message_tree = lazy_assertion.evaluate()
    if result is not False:
        assert False, generate_error_message(message_tree, expected="False", found="True")


def all_true(*lazy_assertions):
    results, message_trees, true_count = generate_all_results(lazy_assertions)
    if true_count < len(lazy_assertions):
        assert False, generate_error_message(*message_trees, expected="all True", found="some False")


def all_false(*lazy_assertions):
    results, message_trees, true_count = generate_all_results(lazy_assertions)
    if true_count > 0:
        assert False, generate_error_message(*message_trees, expected="all False", found="some True")


def some_true(*lazy_assertions):
    results, message_trees, true_count = generate_all_results(lazy_assertions)
    if true_count == 0:
        assert False, generate_error_message(*message_trees, expected="some True", found="all False")


def some_false(*lazy_assertions):
    results, message_trees, true_count = generate_all_results(lazy_assertions)
    if true_count == len(lazy_assertions):
        assert False, generate_error_message(*message_trees, expected="some False", found="all True")


def one_true(*lazy_assertions):
    results, message_trees, true_count = generate_all_results(lazy_assertions)
    if true_count != 1:
        assert False, generate_error_message(*message_trees, expected="1 True", found=f"{true_count} True")


def one_false(*lazy_assertions):
    results, message_trees, true_count = generate_all_results(lazy_assertions)
    false_count = len(lazy_assertions) - true_count
    if false_count != 1:
        assert False, generate_error_message(*message_trees, expected="1 False", found=f"{false_count} False")


def same(*values):
    assert len(values) >= 2
    return SimpleLazyAssertion(assertion.evaluate_same, *values)


def different(*values):
    assert len(values) >= 2
    return SimpleLazyAssertion(assertion.evaluate_different, *values)


def equal(*values):
    assert len(values) >= 2
    return SimpleLazyAssertion(assertion.evaluate_equal, *values)


def unique(*values):
    assert len(values) >= 2
    return SimpleLazyAssertion(assertion.evaluate_unique, *values)


def empty(value):
    return SimpleLazyAssertion(assertion.evaluate_empty, value)


def not_empty(value):
    return SimpleLazyAssertion(assertion.evaluate_not_empty, value)


def exists(value):
    return SimpleLazyAssertion(assertion.evaluate_exists, value)


