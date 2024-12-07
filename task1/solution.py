import unittest


def strict(func):
    def wrapper(*args, **kwargs):
        annotations = {k: v for k, v in func.__annotations__.items() if k != 'return'}
        element_types = {f'{item}': type(item) for item in args}
        if list(annotations.values()) == list(element_types.values()):
            return func(*args)
        else:
            raise TypeError

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


class TestSumTwo(unittest.TestCase):
    """
    Тестирование функции первого задания
    """

    def test_1(self):
        self.assertEqual(sum_two(1, 2), 3)

    def test_2(self):
        with self.assertRaises(TypeError):
            sum_two(1, 2.4)

    def test_3(self):
        with self.assertRaises(TypeError):
            sum_two(5.3, 7.8)

    def test_4(self):
        with self.assertRaises(TypeError):
            sum_two('1', 5)

    def test_5(self):
        self.assertEqual(sum_two(10, 12), 22)


if __name__ == '__main__':
    unittest.main()
