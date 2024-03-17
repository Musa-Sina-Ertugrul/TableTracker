from db_scanner.utils.interface import Interface
import unittest

# TODO: Add docstring

class TestInterface(unittest.TestCase):

    class TestClassFuncInitiliazed(metaclass=Interface,arg1="func_1"):
        
        def func_1(self):
            return True
    
    class TestClassFuncNotInitiliazed:
        
        pass

    class TestClassFuncAsVarInitiliazed:
        
        var_1: str = "Something"
    
    class TestClassWrongType:
        
        pass
        

    def setUp(self) -> None:
        super().setUp()
    
    def test_is_initiliazed(self):
        
        self.assertTrue(bool((test_obj := self.TestClassFuncInitiliazed())))
        self.assertTrue(hasattr(test_obj,"func_1") and callable(test_obj.func_1))
    
    def test_is_not_initiliazed(self):

        with self.assertRaises(NotImplementedError) as error:
            test_obj = Interface.__new__(Interface,"TestClassFuncNotInitiliazed",(None,),self.TestClassFuncNotInitiliazed.__dict__,arg1="func_1")
        
        self.assertTrue(type(error.exception) is NotImplementedError)
    
    def test_not_callable(self):

        with self.assertRaises(NotImplementedError) as error:
            test_obj = Interface.__new__(Interface,"TestClassFuncAsVarInitiliazed",(None,),self.TestClassFuncAsVarInitiliazed.__dict__,arg1="var_1")
        
        self.assertTrue(type(error.exception) is NotImplementedError)

    def test_is_not_str(self):

        with self.assertRaises(TypeError) as error:
            test_obj = Interface.__new__(Interface,"TestClassWrongType",(None,),self.TestClassWrongType.__dict__,arg1=1)
        
        self.assertTrue(type(error.exception) is TypeError)