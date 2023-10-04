import time
import random
from lab_utils import *


def _string_slicing_quiz(num, total):
    s = "Winter is coming!"    
    print(f'Slicing attempt {num}/{total} on string s="{s}"')
    length = random.choice((1,2,2,3,3,3,4,4,4,4,5,5,5,6,6,7))    
    step = random.choice((1,1,1,1,2,2,2,3,3))    
    start = random.randint(0, len(s) - step * length)    
    stop = start + step * length    
    if random.choice((0,0,1)) == 1:
        start, stop, step = stop, start, -step        
    result = s[start:stop:step]        
    ok = False
    start_time = time.time()
    while not ok:
        sol = input(f'Enter a slicing expression to obtain "{result}" >')        
        if any(c not in "s[]:0123456789- " for c in sol):
            print("Your expression contains an invalid character.")
        else:
            try:
                user_result = eval(sol)
                if user_result == result:
                    ok = True
                    print("Correct!")
                else:
                    print(f'Your expression {sol} produces "{user_result}" and not "{result}".')
            except:
                print("Your expression is not correct.")
    return time.time() - start_time


def string_slicing_game():
    tot = 5
    elapsed = [_string_slicing_quiz(i+1, tot) for i in range(tot)]
    average_time, min_time, max_time = sum(elapsed) / tot, min(elapsed), max(elapsed)
    levels = ("Grand Master", "Master", "Gold", "Silver", "Bronze")
    level_delta = 10
    level_step = 10
    level = min(len(levels)-1, int(max(0, average_time-level_delta) / level_step))
    print(f"Time avg/min/max (seconds): {average_time:.2f}/{min_time:.2f}/{max_time:.2f}")
    print("******************************************************")
    print(f"Your String Slicing Level is: {levels[level]}")
    print("******************************************************")
    

def test_es_3(d):
    test_predicates_on_global_vars(d,
        ('ciphertext', lambda x: x == "Huk'zv'ol'zwvrl3'huk'zv'ol'zwvrl3'{oh{'svyk'vm'Jhz{htlyl3'I|{'uv~'{ol'yhpuz'~llw'v.ly'opz'ohss3'~p{o'uv'vul'{olyl'{v'olhy5")
    )
    
    
