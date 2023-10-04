# test_addition.py
import pytest
'''Creating first Test'''
# content of test_sample.py
def func(x):
    return x + 1
def test_answer():
    #fail
    assert func(3) == 5
    #pass
    # assert func(4) == 5

 #content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")


'''Test on Addition'''
def test_addition():

    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2
def add(a,b):
    return a + b

@pytest.fixture(params=[1, 2, 3])
def input_data(request):
    return request.param

"""FOR INSTANCE IF YOU WANT TO DO PARAMETERIZED TESTING"""
@pytest.mark.parametrize("input,expected", [(2,4), (3,9), (4, 16) ] )
def test_square(input,expected):
    assert input ** 2== expected