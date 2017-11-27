import unittest
import test_build_program
import test_build_expressions
import test_build_primitives
import test_build_structures
import test_build_lines























'''
class TestStructures(unittest.TestCase):
    def test_basic_structure_build(self):
        a = build_program.Node(0,'for n = [0:5):')
        b = build_program.Node(0,'')
        c = build_program.Node(0,'')
        a.add(b)
        a.add(c)

        result = build_structures.buildStructure(a,None,None)
        expected = []
        self.assertEqual(result,expected)
'''

if __name__ == '__main__':
    print(test_build_program.test())
    #unittest.main()










