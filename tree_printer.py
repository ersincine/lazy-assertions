def generate_tree_representation(tree, depth=0, is_last_child=True):
    # TODO: Test this function properly.

    def is_internal_node(subtree):
        return isinstance(subtree, tuple)

    def is_leaf(subtree):
        return isinstance(subtree, str)

    def get_branch_prefix():
        if depth == 0:
            return ""
        if is_last_child:
            return "└── "
        return "├── "

    if is_internal_node(tree):
        assert len(tree) == 2
        assert isinstance(tree[0], str)
        assert isinstance(tree[1], list)
    else:
        assert is_leaf(tree)

    # There are internal nodes and leaves.
    # e.g. directories are internal nodes, files are leaves.
    # or, operators are internal nodes, literals are leaves.

    # A leaf is str.
    # An internal node with three children is (str, [x, y, z]) where x is an internal node or leaf.

    lines = []
    if is_internal_node(tree):
        label = tree[0]
        children = tree[1]
        lines.append(("internal", get_branch_prefix(), label))
        prefix = ("    " if is_last_child else "│   ") if depth > 0 else ""
        for not_last_child in children[:-1]:
            lines.extend([
                (line[0], prefix + line[1], line[2])
                for line in
                generate_tree_representation(not_last_child,
                                                      depth=depth + 1,
                                                    is_last_child=False)

            ]
            )
        last_child = children[-1]
        lines.extend([
            (line[0], prefix + line[1], line[2])
                for line in
                      generate_tree_representation(last_child,
                                                  depth=depth + 1,
                                                  is_last_child=True)
        ]
        )
    else:
        # tree is a leaf
        label = tree
        lines.append(("leaf", get_branch_prefix(), label))

    return lines


def print_tree(tree, line_function=lambda x: x, internal_label_function=lambda x: x, leaf_label_function=lambda x: x):
    # TODO: Bunu yazmak yerine str döndürecek şekilde yazsak daha kullanışlı olur.
    # Dosyaya yazarken mesela. Ama renk bilgileri kaybolur orada muhtemelen.
    # Öyleyse parametre olarak vermek lazım.
    lines = generate_tree_representation(tree)
    for node_type, branch_prefix, label in lines:
        label_function = leaf_label_function if node_type == "leaf" else internal_label_function
        print(line_function(branch_prefix + label_function(label)))


class TextColor:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def colorize_str(text, text_color=None, underline=False, bold=False):
    result = text + TextColor.RESET
    if text_color:
        result = text_color + result
    if underline:
        result = TextColor.UNDERLINE + result
    if bold:
        result = TextColor.BOLD + result
    return result


class Tree:

    def __init__(self, root_name):
        self.root_name = root_name
        self.subtrees = []

    def add(self, *node_names):
        subtrees = [Tree(node_name) for node_name in node_names]
        self.subtrees.extend(subtrees)
        if len(node_names) == 1:
            return subtrees[0]
        return subtrees

    def compile(self):
        if len(self.subtrees) > 0:
            return self.root_name, [subtree.compile() for subtree in self.subtrees]
        return self.root_name


if __name__ == "__main__":

    print_tree(("root", ["child1", ("root2", ["child a", ("R", ["a", ("r", ["b"])])]), "child3"]))

    print("-" * 50)

    print_tree(("main", ["a.png", ("video", ["b.avi"]), ("all images", ["c.jpg", ("other photos", ["d.jpg", "e.jpg"]),
               "f.jpg"]), ("music", ["g.mp3"])]), internal_label_function=lambda x: x.upper())

    print("-" * 50)

    print_tree(("+", [("*", ["2", "1"]), "11"]), line_function=lambda x: "\t" * 3 + x)

    print("-" * 50)

    print_tree(("AND", [("OR", ["ALL", "ALL"]), ("AND", ["ALL", "ALL"])]))

    print("-" * 50)

    print_tree(("AND", ["1", ("OR", ["2", "3"])]))

    print("-" * 50)

    print_tree(("+", [("*", ["2", "1"]), "11"]), line_function=lambda x: "\t" * 3 + x)

    print("-" * 50)

    print_tree(("+", ["11", ("*", ["2", "1"])]), line_function=lambda x: "\t" * 3 + x)

    print("-" * 50)

    # Using Tree it is much easier to create a tree:
    hw02 = Tree("hw02")
    hw02.add("evaluation").add("grader.py", "exercise1_utils.hpp", "exercise2_utils.hpp", "exercise1_tests", "exercise2_tests", "exercise3_tests")
    hw02.add("exercise2").add("src").add("exercise1.cc")
    hw02.add("exercise2").add("src").add("exercise2.cc")
    data, src = hw02.add("exercise3").add("data", "src")
    data.add("example.csv")
    src.add("exercise3.cc")
    dir_structure = hw02.compile()
    # dir_structure = ('hw02', [('evaluation', ['grader.py', 'exercise1_utils.hpp', 'exercise2_utils.hpp', 'exercise1_tests', 'exercise2_tests', 'exercise3_tests']), ('exercise2', [('src', ['exercise1.cc'])]), ('exercise2', [('src', ['exercise2.cc'])]), ('exercise3', [('data', ['example.csv']), ('src', ['exercise3.cc'])])])
    print_tree(dir_structure)
