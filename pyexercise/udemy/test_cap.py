
import unittest
from cap import cap_text, Employee

class TestCap(unittest.TestCase):

    def test_one_word(self):
        text = 'python'
        result = cap_text(text)
        self.assertEqual(result, 'Python')

    def test_multiple_words(self):
        text = 'i love python'
        result = cap_text(text)
        self.assertEqual(result, 'I Love Python')

    def test_apostrophes(self):
        text = "i don't like python"
        result = cap_text(text)
        self.assertEqual(result, "I Don't Like Python")

class TestEmployee(unittest.TestCase): # how to test methods in class

    @classmethod # this class method will run before all tests once
    def setUpClass(cls):
        print('setUpClass')

    @classmethod # this class methond will run after all tests once
    def tearDownClass(cls):
        print('tearDownClass')

    def setUp(self): # this will run before every single test
        print('setUp')
        self.emp_1 = Employee('Aaron', 'Fan', 50000)
        self.emp_2 = Employee('Sandy', 'Hoo', 60000)

    def tearDown(self): # this will run after every single test
        print('tearDown\n')


    def test_email(self): # test is not neccesarily run in sequence
        print('test_email')
        self.assertEqual(self.emp_1.email, 'Aaron.Fan@email.com')
        self.assertEqual(self.emp_2.email, 'Sandy.Hoo@email.com')

    def test_fullname(self):
        print('test_fullname')
        self.assertEqual(self.emp_1.fullname, 'Aaron Fan')
        self.assertEqual(self.emp_2.fullname, 'Sandy Hoo')

    def test_apply_raise(self):
        print('test_apply_raise')
        self.emp_1.apply_raise()
        self.emp_2.apply_raise()

        self.assertEqual(self.emp_1.pay, 52500)
        self.assertEqual(self.emp_2.pay, 63000)


if __name__== '__main__':
    unittest.main()
