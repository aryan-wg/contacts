import unittest
from unittest.mock import Mock, patch,call
import io
from src.utils.general_utils import hash_pass, take_address_input
from src.utils.validations_utils import int_input,validate_password,validate_pin_code,validate_phone,validate_email

class Test_validation_utils(unittest.TestCase):
    def test_validate_email(self):
        #arrang

        #act
        should_be_false = validate_email("not_an_email")
        should_be_true = validate_email("test@test.com")
            
        #assert
        assert should_be_false == False 
        assert should_be_true == True 

    def test_validate_phone(self):
        should_be_false = validate_phone(9234784893204)         
        should_be_false_2 = validate_phone(21391)
        should_be_false_3 = validate_phone("random string")

        should_be_true = validate_phone(1111111111)
        
        assert should_be_true == True
        assert should_be_false == False 
        assert should_be_false_2 == False
        assert should_be_false_3 == False

    def test_validate_pin_code(self):
        should_be_false = validate_pin_code(1234567)
        should_be_false_2 = validate_pin_code(12345)
        should_be_false_3 = validate_pin_code("random string")

        should_be_true = validate_pin_code(123456)


        assert should_be_false == False 
        assert should_be_false_2 == False 
        assert should_be_false_3 == False 
        assert should_be_true == True

    def test_validate_password(self):
        should_be_true = validate_password("testT@12")
        should_be_true_2 = validate_password("testTT@123")

        should_be_false = validate_password("testt@1")
        should_be_false_1 = validate_password("testt@12")
        should_be_false_2 = validate_password("TESTT@12")
        should_be_false_3 = validate_password("testT@@@")
        should_be_false_4 = validate_password("12345678")
        should_be_false_5 = validate_password("@#$%^&*/")
        should_be_false_6 = validate_password("ASDFGHJK")
        should_be_false_7 = validate_password("asdfghjk")

        assert True == should_be_true
        assert True == should_be_true_2
        assert False == should_be_false
        assert False == should_be_false_1
        assert False == should_be_false_2
        assert False == should_be_false_3
        assert False == should_be_false_4
        assert False == should_be_false_5
        assert False == should_be_false_6
        assert False == should_be_false_7

