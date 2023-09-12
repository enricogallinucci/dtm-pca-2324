import IPython
import html

def show(*images, max_per_row = -1):
    
    if max_per_row == -1:
        max_per_row = len(images)
    
    rows = [images[x:x+max_per_row] for x in range(0, len(images), max_per_row)]
    
    html_content = ""
    for l in rows:
        html_content += "".join(["<table><tr>"] 
                + [f"<td style='text-align:center;'>{html.escape(t)}</td>" for _,t in l]    
                + ["</tr><tr>"] 
                + [f"<td style='text-align:center;'><img src='{d}'></td>" for d,_ in l]
                + ["</tr></table>"])
    IPython.display.display(IPython.display.HTML(html_content))

_test_ok_image = {True: 'icons/tup.png', False: 'icons/tdn.png'}

def test_cases(*conditions):
    show(*[(_test_ok_image[c], t) for t,c in conditions])

def test_predicate_on_global_var(d, name, predicate):
    value = d.get(name)
    if value is None:
        return False
    try:
        return predicate(value)
    except:
        return False
    
def test_predicates_on_global_vars(d, *names_and_predicates):
    return test_cases(*[(n, test_predicate_on_global_var(d, n, p)) for n, p in names_and_predicates])

def test_global_function(d, name, args, predicate):
    f = d.get(name)
    if f is None:
        return False
    try:        
        r = f(*args)
        return predicate(r) if callable(predicate) else r == predicate
    except:
        return False

def function_test_cases(d, function_name, *tests):
    for args, predicate in tests:
        if not test_global_function(d, function_name, args, predicate):
            return test_cases((f"Test with parameters {args} failed", False))
    test_cases((f"{len(tests)} tests passed!", True))

    
def readFromFile(p):
    try:
        with open(p) as f:
            txt = f.read()
            return txt.split("\n")
    except:
        return None