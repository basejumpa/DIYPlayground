import unittest
from arduino import Arduino

b = Arduino('COM4')
pin_out = 5
pin_in  = 9

#declare output pins as a list/tuple
b.output([pin_out])

class MyTestCase(unittest.TestCase):
    def test_something(self):
        b.setHigh(pin_out)
        self.assertEqual(b.getState(pin_in), True)

        b.setLow(pin_out)
        self.assertEqual(b.getState(pin_in), False)


if __name__ == '__main__':
    unittest.main()
