from lab_utils import *

def test_analyze_strings(g):
    function_test_cases(g, "analyze_strings", 
        ([['A']], (1, 1, [('A', 'A', 'A')])),
        ([['A', 'B']], (1, 1, [('A', 'A', 'A'), ('B', 'B', 'B')])),
        ([['AB', 'BA']], (2, 2, [('A', 'B', 'BA'), ('B', 'A', 'AB')])),
        ([['The', 'chances', 'of', 'finding', 'out', 'what’s', 'really', 'going', 'on', 'in', 'the', 'universe', 'are', 'so', 'remote']], (2, 8, [('T', 'e', 'ehT'), ('c', 's', 'secnahc'), ('o', 'f', 'fo'), ('f', 'g', 'gnidnif'), ('o', 't', 'tuo'), ('w', 's', 's’tahw'), ('r', 'y', 'yllaer'), ('g', 'g', 'gniog'), ('o', 'n', 'no'), ('i', 'n', 'ni'), ('t', 'e', 'eht'), ('u', 'e', 'esrevinu'), ('a', 'e', 'era'), ('s', 'o', 'os'), ('r', 'e', 'etomer')])),
        ([['the', 'only', 'thing', 'to', 'do', 'is', 'hang', 'the', 'sense', 'of', 'it', 'and', 'keep', 'yourself', 'occupied']], (2, 8, [('t', 'e', 'eht'), ('o', 'y', 'ylno'), ('t', 'g', 'gniht'), ('t', 'o', 'ot'), ('d', 'o', 'od'), ('i', 's', 'si'), ('h', 'g', 'gnah'), ('t', 'e', 'eht'), ('s', 'e', 'esnes'), ('o', 'f', 'fo'), ('i', 't', 'ti'), ('a', 'd', 'dna'), ('k', 'p', 'peek'), ('y', 'f', 'flesruoy'), ('o', 'd', 'deipucco')])),
    )
   
 
    
def test_combine_lists(g):
    function_test_cases(g, "combine_lists",     
        ([[], []], []),
        ([[1], ['']], [(1, '', ('',))]),
        ([[1, 2], ['', '']], [(1, '', ('',)), (2, '', ('', ''))]),
        ([[2, 3], ['A', '']], [(2, 'A', ('A', 'A')), (3, '', ('', '', ''))]),
        ([[4, 2], ['Don’t', 'Panic']], [(4, 'Don’t', ('Don’t', 'Don’t', 'Don’t', 'Don’t')), (2, 'Panic', ('Panic', 'Panic'))]),
        ([[7, 7, 8, 2, 7, 4, 6, 6, 4, 6, 4, 1, 5, 5, 1], ['It', 'is', 'a', 'mistake', 'to', 'think', 'you', 'can', 'solve', 'any', 'major', 'problems', 'just', 'with', 'potatoes']], [(7, 'It', ('It', 'It', 'It', 'It', 'It', 'It', 'It')), (7, 'is', ('is', 'is', 'is', 'is', 'is', 'is', 'is')), (8, 'a', ('a', 'a', 'a', 'a', 'a', 'a', 'a', 'a')), (2, 'mistake', ('mistake', 'mistake')), (7, 'to', ('to', 'to', 'to', 'to', 'to', 'to', 'to')), (4, 'think', ('think', 'think', 'think', 'think')), (6, 'you', ('you', 'you', 'you', 'you', 'you', 'you')), (6, 'can', ('can', 'can', 'can', 'can', 'can', 'can')), (4, 'solve', ('solve', 'solve', 'solve', 'solve')), (6, 'any', ('any', 'any', 'any', 'any', 'any', 'any')), (4, 'major', ('major', 'major', 'major', 'major')), (1, 'problems', ('problems',)), (5, 'just', ('just', 'just', 'just', 'just', 'just')), (5, 'with', ('with', 'with', 'with', 'with', 'with')), (1, 'potatoes', ('potatoes',))]),
    )

def test_create_histogram(g):
    function_test_cases(g, "create_histogram",         
        ([''], []),
        ([' '], []),
        (['.'], []),
        (['. .'], []),
        (['.,;?1234567890'], []),
        (['a.,123'], [('A', '*')]),
        (['abc'], [('A', '*'), ('B', '*'), ('C', '*')]),
        (['aaa'], [('A', '***')]),
        ([' aaa '], [('A', '***')]),
        (["-Funny,- he intoned funereally, -how just when you think life can't possibly get any worse it suddenly does.-"], [('A', '***'), ('B', '*'), ('C', '*'), ('D', '****'), ('E', '**********'), ('F', '***'), ('G', '*'), ('H', '****'), ('I', '*****'), ('J', '*'), ('K', '*'), ('L', '*****'), ('N', '**********'), ('O', '******'), ('P', '*'), ('R', '**'), ('S', '******'), ('T', '******'), ('U', '*****'), ('W', '***'), ('Y', '******')]),
    )                        
    
    
def test_find_common_words(g):
    function_test_cases(g, "find_common_words",             
        (["", ""], []),
        ([".", "abc"], []),
        (["", "b,."], []),
        (["-Funny,- he intoned funereally, -how just when you think life can't possibly get any worse it suddenly does.-", "Just when you think it can't get any worse, it can. And just when you think it can't get any better, it can."], ['any', "can't", 'get', 'it', 'just', 'think', 'when', 'worse', 'you']),
        (["Never regret anything that made you smile", "You can discover more about a person in an hour of play than in a year of conversation"], ["you"]),
    )                     
    
    
def test_word_count(g):
    function_test_cases(g, "word_count",             
        (["files/sheep.txt", 2], {'the': 4, 'bench': 2, 'sheep': 2}),
        (["files/divine_comedy.txt", 1000], {'la': 2361, 'di': 1898, 'per': 1384, 'a': 2046, 'e': 4070, 'che': 3697, 'ch': 1029, 'l': 2677, 'io': 1137, 'non': 1456, 'in': 1107, 'si': 1043}),
        (["files/lost.txt", 3], {'i': 6, 'the': 3, 'a': 3, 'but': 4, 'this': 3, 'is': 3, 'it': 7, 's': 4, 'what': 3, 'if': 3}),
    )
    