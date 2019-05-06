import PictoCrossSolver.Analyzers

def test_getRegularExpressionParts_scenario1():
    """
    Tests that regular expression parts count is valid
    1 hint should have 1 part
    """

    obj = PictoCrossSolver.Analyzers.RegexBuilder()
    
    parts = obj.getRegularExpressionParts([1], 0)

    assert len(parts) == 1

def test_getRegularExpressionParts_scenario2():
    """
    Tests that regular expression parts count is valid
    2 hints should have 3 parts
    """

    obj = PictoCrossSolver.Analyzers.RegexBuilder()
    
    parts = obj.getRegularExpressionParts([1, 1], 0)

    assert len(parts) == 3

def test_getRegularExpressionParts_scenario3():
    """
    Tests regular expression contents is valid
    2 hints should have 3 parts, middle part should be a separator
    First item should be greedy, others lazy
    Items should feature proper size constraints
    """

    obj = PictoCrossSolver.Analyzers.RegexBuilder()
    
    parts = obj.getRegularExpressionParts([2, 4], 0)

    assert parts[0] == '(?P<hint0>(a|m){2,})'
    assert parts[1] == '(?P<sep0>(a|b){1,}?)'
    assert parts[2] == '(?P<hint1>(a|m){4,}?)'


def test_getRegularExpressionParts_scenario4():
    """
    Tests regular expression contents is valid
    2 hints should have 3 parts, middle part should be a separator
    First item should be lazy, other greedy, separators always lazy
    Items should feature proper size constraints
    """

    obj = PictoCrossSolver.Analyzers.RegexBuilder()
    
    parts = obj.getRegularExpressionParts([2, 4], 1)

    assert parts[0] == '(?P<hint0>(a|m){2,}?)'
    assert parts[1] == '(?P<sep0>(a|b){1,}?)'
    assert parts[2] == '(?P<hint1>(a|m){4,})'


def test_getForwardRegularExpression_scenario1():
    """
    Tests regular expression contents is valid
    2 hints should have 5 parts, lazy prefix, 1 greedy part, 1 separator, 1 lazy part, greedy suffix
    """

    obj = PictoCrossSolver.Analyzers.RegexBuilder()
    
    expression = obj.getForwardRegularExpression([2, 4], 0)

    expectedParts = [
        '(?P<prefix>(a|b)*?)',
        '(?P<hint0>(a|m){2,})',
        '(?P<sep0>(a|b){1,}?)',
        '(?P<hint1>(a|m){4,}?)',
        '(?P<suffix>(a|b)*)'
    ]

    assert expression == "".join(expectedParts)


def test_getBackwardRegularExpression_scenario1():
    """
    Tests regular expression contents is valid
    2 hints should have 5 parts, lazy prefix, 1 greedy part, 1 separator, 1 lazy part, greedy suffix
    But everything should be flipped around
    """

    obj = PictoCrossSolver.Analyzers.RegexBuilder()
    
    expression = obj.getBackwardRegularExpression([2, 4], 0)

    expectedParts = [
        '(?P<suffix>(a|b)*?)',
        '(?P<hint1>(a|m){4,}?)',
        '(?P<sep0>(a|b){1,}?)',
        '(?P<hint0>(a|m){2,})',
        '(?P<prefix>(a|b)*)'
    ]

    assert expression == "".join(expectedParts)