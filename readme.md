# Evaluation of regex based solving

## Step 1
col: 7
hints: [13]
data: aaaaaaaaaaaaaaa
regex: (?<hint0>(a|m){13,})
result:
    Full match	0-15	aaaaaaaaaaaaaaa
    Group `hint0`	0-15	aaaaaaaaaaaaaaa
    Group 2.	14-15	a
Solver applied: FitHintInLargeAmbiguousZone
Post solver: aammmmmmmmmmmaa

## Step 2
col: 8
hints: [9,2]
data: aaaaaaaaaaaaaaa
regex: (?<hint0>(a|m){9,})(?<hintsep0>(a|b){1,})(?<hint1>(a|m){2,})
result:
    Full match	0-15	aaaaaaaaaaaaaaa
    Group `hint0`	0-12	aaaaaaaaaaaa
    Group 2.	11-12	a
    Group `hintsep0`	12-13	a
    Group 4.	12-13	a
    Group `hint1`	13-15	aa
    Group 6.	14-15	a
Solver applied: FitHintInLargeAmbiguousZone for hint0
Post solver: aaammmmmmaaaaaa

## Step 3
col: 9
hints: [9,2]
data: aaaaaaaaaaaaaaa
regex: (?<hint0>(a|m){8,})(?<hintsep0>(a|b){1,})(?<hint1>(a|m){2,})
result:
    Full match	0-15	aaaaaaaaaaaaaaa
    Group `hint0`	0-12	aaaaaaaaaaaa
    Group 2.	11-12	a
    Group `hintsep0`	12-13	a
    Group 4.	12-13	a
    Group `hint1`	13-15	aa
    Group 6.	14-15	a
Solver applied: FitHintInLargeAmbiguousZone for hint0
Post solver: aaaammmmaaaaaaa

## Step 4
col: 10
hints: [9,2]
data: aaaaaaaaaaaaaaa
regex: (?<hint0>(a|m){9,})(?<hintsep0>(a|b){1,})(?<hint1>(a|m){2,})
result:
    Full match	0-15	aaaaaaaaaaaaaaa
    Group `hint0`	0-12	aaaaaaaaaaaa
    Group 2.	11-12	a
    Group `hintsep0`	12-13	a
    Group 4.	12-13	a
    Group `hint1`	13-15	aa
    Group 6.	14-15	a
Solver applied: FitHintInLargeAmbiguousZone for hint0
Post solver: aaammmmmmaaaaaa

## Step 5
row: 7 & 8
hints: [4]
data: aaaaaammmmaaaaa
regex: (?<hint0>(a|m){4,})
result:
    Full match	0-15	aaaaaammmmaaaaa
    Group `hint0`	0-15	aaaaaammmmaaaaa
    Group 2.	14-15	a
Solver applied: HintCompletedMarksAmbiguous for hint0
Post solver: xxxxxxmmmmxxxxx

## Step 6
row: 6
hints: [9]
data: aaaaaammmmaaaaa
regex: (?<hint0>(a|m){9,})
result:
    Full match	0-15	aaaaaammmmaaaaa
    Group `hint0`	0-15	aaaaaammmmaaaaa
    Group 2.	14-15	a
Solver applied: BarAmbiguousZonesUnreachable for hint0
Post solver: xaaaaammmmaaaaa

## Step 7
row: 5
hints: [10]
data: aaaaaammmmaaaaa
regex: (?<hint0>(a|m){10,})
result:
    Full match	0-15	aaaaaammmmaaaaa
    Group `hint0`	0-15	aaaaaammmmaaaaa
    Group 2.	14-15	a
Solver applied: ExpandIntoAdjacentAmbiguousZones for hint0
Post solver: aaaaammmmmaaaaa

## Step 8
row: 4
hints: [6]
data: aaaaaammamaaaaa (Has 2 marked zones)
regex: (?<prefix>.*?)(?<hint0pt1>m{1,6})(?<hint0split>a{0,4})(?<hint0pt2>m{1,6})(?<suffix>.*)
result:
    Full match	0-15	aaaaaammamaaaaa
    Group `prefix`	0-6	aaaaaa
    Group `hint0pt1`	6-8	mm
    Group `hint0split`	8-9	a
    Group `hint0pt2`	9-10	m
    Group `suffix`	10-15	aaaaa
Solver applied: MergeMarkedZonesSplitByAmbiguous for hint0
Post solver: aaaaaammmmaaaaa

## Step 9
row: 4
hints: [6]
data: aaaaaammmmaaaaa
regex-pre: (?<prefix>.*?)(?<hint0pre>a{0,5})(?<hint0>m{1,6})(?<hint0post>a{0,5})(?<suffix>.*)
pre-results:
    Full match	0-15	aaaaaammmmaaaaa
    Group `prefix`	0-1	a
    Group `hint0pre`	1-6	aaaaa
    Group `hint0`	6-10	mmmm
    Group `hint0post`	10-15	aaaaa
    Group `suffix`	15-15	
Analyze results and rerun with another regex to find the 4m and 2a around it
regex: (?<prefix>.*?)(?<hint0pre>a{2})(?<hint0>m{4})(?<hint0post>a{2})(?<suffix>.*)
result:
    Full match	0-15	aaaaaammmmaaaaa
    Group `prefix`	0-4	aaaa
    Group `hint0pre`	4-6	aa
    Group `hint0`	6-10	mmmm
    Group `hint0post`	10-12	aa
    Group `suffix`	12-15	aaa
Solver applied: BarAmbiguousZonesUnreachable for hint0
Post solver: xxxxaammmmaaxxx

## Step 10
row: 3
hints: [6]
data: aaaaaamaaaaaaaa
regex-pre: (?<prefix>.*?)(?<hint0pre>a{0,5})(?<hint0>m{1,6})(?<hint0post>a{0,5})(?<suffix>.*)
pre-results:
    Full match	0-15	aaaaaamaaaaaaaa
    Group `prefix`	0-1	a
    Group `hint0pre`	1-6	aaaaa
    Group `hint0`	6-7	m
    Group `hint0post`	7-12	aaaaa
    Group `suffix`	12-15	aaa
Analyze results, there are enough values around hint to expand into and too many not to bar the excedent
regex: (?<prefix>.*?)(?<hint0pre>a{5})(?<hint0>m{1})(?<hint0post>a{5})(?<suffix>.*)
result:
    Full match	0-15	aaaaaamaaaaaaaa
    Group `prefix`	0-1	a
    Group `hint0pre`	1-6	aaaaa
    Group `hint0`	6-7	m
    Group `hint0post`	7-12	aaaaa
    Group `suffix`	12-15	aaa
Solver applied: BarAmbiguousZonesUnreachable for hint0
Post solver: xaaaaamaaaaaxxx

## Step 11
row: 8
hints: [6]
data: aaaaaammamaaaaa
regex: (?<prefix>.*?)(?<hint0pt1>m{1,6})(?<hint0split>a{0,4})(?<hint0pt2>m{1,6})(?<suffix>.*)
result:
    Full match	0-15	aaaaaammamaaaaa
    Group `prefix`	0-6	aaaaaa
    Group `hint0pt1`	6-8	mm
    Group `hint0split`	8-9	a
    Group `hint0pt2`	9-10	m
    Group `suffix`	10-15	aaaaa
Solver applied: MergeMarkedZonesSplitByAmbiguous for hint0
Post solver: aaaaaammmmaaaaa

## Step 12
row: 8
hints: [6]
data: aaaaaammmmaaaaa
regex-pre: (?<prefix>.*?)(?<hint0pre>a{0,5})(?<hint0>m{1,6})(?<hint0post>a{0,5})(?<suffix>.*)
pre-results:
    Full match	0-15	aaaaaammmmaaaaa
    Group `prefix`	0-1	a
    Group `hint0pre`	1-6	aaaaa
    Group `hint0`	6-10	mmmm
    Group `hint0post`	10-15	aaaaa
    Group `suffix`	15-15	
Analyze results and rerun with another regex to find the 4m and 2a around it
regex: (?<prefix>.*?)(?<hint0pre>a{2})(?<hint0>m{4})(?<hint0post>a{2})(?<suffix>.*)
result:
    Full match	0-15	aaaaaammmmaaaaa
    Group `prefix`	0-4	aaaa
    Group `hint0pre`	4-6	aa
    Group `hint0`	6-10	mmmm
    Group `hint0post`	10-12	aa
    Group `suffix`	12-15	aaa
Solver applied: BarAmbiguousZonesUnreachable for hint0
Post solver: xxxxaammmmaaxxx

## Step 13
row: 9
hints: [7]
data: aaaaaamaaaaaaaa
regex-pre: (?<prefix>.*?)(?<hint0pre>a{0,6})(?<hint0>m{1,7})(?<hint0post>a{0,6})(?<suffix>.*)
pre-results:
    Full match	0-15	aaaaaamaaaaaaaa
    Group `prefix`	0-0	
    Group `hint0pre`	0-6	aaaaaa
    Group `hint0`	6-7	m
    Group `hint0post`	7-13	aaaaaa
    Group `suffix`	13-15	aa
Analyze results and rerun with another regex to find the 1m and 6a around it
regex: (?<prefix>.*?)(?<hint0pre>a{6})(?<hint0>m{1})(?<hint0post>a{6})(?<suffix>.*)
result:
    Full match	0-15	aaaaaamaaaaaaaa
    Group `prefix`	0-0	
    Group `hint0pre`	0-6	aaaaaa
    Group `hint0`	6-7	m
    Group `hint0post`	7-13	aaaaaa
    Group `suffix`	13-15	aa
Solver applied: BarAmbiguousZonesUnreachable for hint0
Post solver: aaaaaamaaaaaaxx

## Step 14
row: 13
hints: [9]
data: aaaaaamaaaaaaaa
regex-pre: (?<prefix>.*?)(?<hint0pre>a{0,8})(?<hint0>m{1,9})(?<hint0post>a{0,8})(?<suffix>.*)
pre-results:
    Full match	0-15	aaaaaamaaaaaaaa
    Group `prefix`	0-0	
    Group `hint0pre`	0-6	aaaaaa
    Group `hint0`	6-7	m
    Group `hint0post`	7-15	aaaaaaaa
    Group `suffix`	15-15	
Analyze results and rerun with another regex to find the 1m and 6a around it
regex: (?<prefix>.*?)(?<hint0pre>a{8})(?<hint0>m{1})(?<hint0post>a{8})(?<suffix>.*)
result:
    no match
    This means i need to expand instead of barring
regex: (?<prefix>.*?)(?<hint0pre>a{0,8})(?<hint0>m{1})(?<hint0post>a{0,8})(?<suffix>.*)
result:
    Full match	0-15	aaaaaamaaaaaaaa
    Group `prefix`	0-0	
    Group `hint0pre`	0-6	aaaaaa
    Group `hint0`	6-7	m
    Group `hint0post`	7-15	aaaaaaaa
    Group `suffix`	15-15
    hint0pre has only 6 values, hint0post must be marked by (9 - 1 - 6 = 2)
Solver applied: ExpandMarkedZoneIntoAdjacentAmbiguousZoneToCompensate for hint0
Post solver: aaaaaammmaaaaaa

## Step 15
column: 6
hints: [3,4,1]
data: aaaamabbaaaaaaa
regex-pre: (?<prefix>.*?)(?<hint0>(a|m){3,})(?<hint0sep>(a|b){1,}?)(?<hint1>(a|m){4,})(?<hint1sep>(a|b){1,}?)(?<hint2>(a|m){1,})(?<suffix>.*)
pre-results:
    Full match	0-15	aaaamabbaaaaaaa
    Group `prefix`	0-0	
    Group `hint0`	0-6	aaaama
    Group `hint0sep`	6-8	bb
    Group `hint1`	8-13	aaaaa
    Group `hint1sep`	13-14	a
    Group `hint2`	14-15	a
    Group `suffix`	15-15	
This reveals that:
    - hint0 can fit in 0-6 and should be expanded from 5 to 4 (ExpandMarksDueToEdges)
    - hint1 can fit in 8-13 and should be set in 3 out of 5 zones at 9-12 (MarkMinimumOverlappingZone)
    - hint2 cannot be marked
Results:
    aaammabbammmaaa





(?P<prefix>(a|b)*?)(?P<hint0>(a|m){3,}?)(?P<sep0>(a|b){1,}?)(?P<hint1>(a|m){2,}?)(?P<sep1>(a|b){1,}?)(?P<hint2>(a|m){2,})(?P<suffix>(a|b)*)
aaaaaaaaabmm

(?P<suffix>(a|b)*?)(?P<hint2>(a|m){2,})(?P<sep1>(a|b){1,}?)(?P<hint1>(a|m){2,}?)(?P<sep0>(a|b){1,}?)(?P<hint0>(a|m){3,}?)(?P<prefix>(a|b)*)
mmbaaaaaaaaa