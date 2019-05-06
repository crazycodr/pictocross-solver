import PictoCrossSolver.Analyzers

def test_analyze_scenario1():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy
    Pattern should return a possible result of "aaaaaa" for hint 0 from the start
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getForwardRegularExpression([1], 0)
    
    assert obj.analyze("aaaaaa", expression, 0) == slice(0, 6, None)


def test_analyze_scenario2():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy
    Pattern should return a possible result of "aa" for hint 0 from the start
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getForwardRegularExpression([1], 0)
    
    assert obj.analyze("aabaaa", expression, 0) == slice(0, 2, None)


def test_analyze_scenario3():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy
    Pattern should return a possible result of "aaa" for hint 0 from the end
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getForwardRegularExpression([2], 0)
    
    assert obj.analyze("abbaaa", expression, 0) == slice(3, 6, None)


def test_analyze_scenario4():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy
    Pattern should return a possible result of "mma" for hint 0 from the end
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getForwardRegularExpression([2], 0)
    
    assert obj.analyze("abbmma", expression, 0) == slice(3, 6, None)


def test_analyze_scenario5():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy and hint 1 is lazy
    Pattern should return a possible result of "aaa" for hint 0 from the start
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getForwardRegularExpression([2, 2], 0)
    
    assert obj.analyze("aaaaaa", expression, 0) == slice(0, 3, None)


def test_analyze_scenario6():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is lazy and hint 1 is greedy
    Pattern should return a possible result of "aa" for hint 0 from the start
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getForwardRegularExpression([2, 2], 1)
    
    assert obj.analyze("aaaaaa", expression, 0) == slice(0, 2, None)


def test_analyze_scenario7():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is lazy and hint 1 is greedy
    Pattern should return a possible result of "aaaa" for hint 1 from the end
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getForwardRegularExpression([2, 2], 1)
    
    assert obj.analyze("aaaaaa", expression, 1) == slice(3, 6, None)


def test_analyze_scenario8():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy and hint 1 is lazy
    Pattern should return a possible result of "aaa" for hint 1 from the end
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getForwardRegularExpression([2, 2], 0)
    
    assert obj.analyze("aaaaaa", expression, 1) == slice(4, 6, None)


def test_analyze_scenario11():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy and pattern shows a possible result of "aaaaaa"
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getBackwardRegularExpression([1], 0)
    
    assert obj.analyze("aaaaaa", expression, 0) == slice(0, 6, None)


def test_analyze_scenario12():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy and pattern shows a possible result of "aaa"
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getBackwardRegularExpression([1], 0)
    print(expression)
    
    assert obj.analyze("aaabaa", expression, 0) == slice(0, 3, None)


def test_analyze_scenario13():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy and pattern shows a possible result of "aaa"
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getBackwardRegularExpression([2], 0)
    
    assert obj.analyze("aaabba", expression, 0) == slice(0, 3, None)


def test_analyze_scenario14():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy and pattern shows a possible result of "amm"
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getBackwardRegularExpression([2], 0)
    
    assert obj.analyze("ammbba", expression, 0) == slice(0, 3, None)


def test_analyze_scenario15():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is greedy, hint 1 is lazy, we want hint 0's slice which
    should be the last 3 characters
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getBackwardRegularExpression([2, 2], 0)
    print(expression)
    
    assert obj.analyze("aaaaaa", expression, 0) == slice(3, 6, None)


def test_analyze_scenario16():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is lazy, hint 1 is greedy, we want hint 0's slice which
    should be the last 2 characters
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getBackwardRegularExpression([2, 2], 1)
    
    assert obj.analyze("aaaaaa", expression, 0) == slice(4, 6, None)


def test_analyze_scenario17():
    """
    Tests that analyzer returns proper result
    In this test, hint 0 is lazy, hint 1 is greedy, we want hint 1's slice which
    should be the first 3 characters
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getBackwardRegularExpression([2, 2], 1)
    
    assert obj.analyze("aaaaaa", expression, 1) == slice(0, 3, None)


def test_analyze_scenario18():
    """
    Tests that analyzer returns proper result in backwards mode
    In this test, hint 0 is greedy, hint 1 is lazy, we want hint 1's slice which
    should be the first 2 characters
    """

    obj = PictoCrossSolver.Analyzers.RegexZoneAnalyzer()

    expression = PictoCrossSolver.Analyzers.RegexBuilder.getBackwardRegularExpression([2, 2], 0)
    
    assert obj.analyze("aaaaaa", expression, 1) == slice(0, 2, None)