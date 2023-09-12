import IPython
import html
from lab_utils import *
    
def test_es_4(d):
    test_predicates_on_global_vars(d,
        ('n1', lambda x: x == 3.5),
        ('n2', lambda x: x == 46),
        ('n3', lambda x: x == 46/3.5),
        ('n4', lambda x: x == 13 and type(x) == int),
        ('n5', lambda x: x == 13 and type(x) == int),
        ('n6', lambda x: x == 13.5),
        ('n7', lambda x: x == type(13.5)),
        ('n8', lambda x: x == 1.75),
        ('n9', lambda x: x == 13)
    )
    
def test_es_5(d):
    test_predicates_on_global_vars(d,
        ('pi', lambda x: x == 3.14159),
        ('area_of_the_circle', lambda x: x == 5541.76476),
        ('circumference', lambda x: x == 263.89356),
        ('min_value', lambda x: x == 263.89356),
        ('int_circumference', lambda x: x == 263 and type(x) == int),
        ('type_of_circumference', lambda x: x == float),
        ('type_of_int_circumference', lambda x: x == int),
    )
