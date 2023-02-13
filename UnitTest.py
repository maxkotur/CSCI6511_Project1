# main.py

import unittest
from main import Player


class TestStringMethods(unittest.TestCase):

    def test_example1(self):
        problem = {
            "size": [1,4,10,15,22],
            "target": 181
        }
        player = Player()
        glob_target = problem["target"]
        result = player.run(problem=problem)
        self.assertEqual(result, 21)

    def test_example2(self):
        problem = {
            "size": [2,5,6,72],
            "target": 143
        }
        player = Player()
        glob_target = problem["target"]
        result = player.run(problem=problem)
        self.assertEqual(result, 8)

    def test_example3(self):
        problem = {
            "size": [2],
            "target": 143
        }
        player = Player()
        glob_target = problem["target"]
        result = player.run(problem=problem)
        self.assertEqual(result, -1)

    def test_example4(self):
        problem = {
            "size": [3,6],
            "target": 2
        }
        player = Player()
        glob_target = problem["target"]
        result = player.run(problem=problem)
        self.assertEqual(result, -1)

    def test_example5(self):
        problem = {
            "size": [5,8,12],
            "target": 6
        }
        player = Player()
        glob_target = problem["target"]
        result = player.run(problem=problem)
        self.assertEqual(result, 8)

    def test_example6(self):
        problem = {
            "size": [1,4,5],
            "target": 18
        }
        player = Player()
        glob_target = problem["target"]
        result = player.run(problem=problem)
        self.assertEqual(result, 11)

    def test_example7(self):
        problem = {
            "size": [1,3,5],
            "target": 0
        }
        player = Player()
        glob_target = problem["target"]
        result = player.run(problem=problem)
        self.assertEqual(result, 0)

    # def test_example(self):
    #     problem = {
    #         "size": [2,3,5,19,121,852],
    #         "target": 11443
    #     }
    #     player = Player()
    #     glob_target = problem["target"]
    #     result = player.run(problem=problem)
    #     self.assertEqual(result, 36)

if __name__ == '__main__':
    unittest.main()