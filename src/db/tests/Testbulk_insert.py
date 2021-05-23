import logging
import unittest

#https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time/14132912#14132912
from bulk_insert import build_chunk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Testbulk_insert(unittest.TestCase):
    
    def test_build_chunk(self):
        lines = 'f11|f12|f13\nf21|f22|f23|f24\nf31|f32|f33\nf41f42f43\nf51f52\nf61|f62|f63\n'
        sep = '|'
        nb_sep = 2

        chunk  = []
        for i,line in enumerate(lines.splitlines()):
            chunk = build_chunk(sep, nb_sep, chunk, line, i+1)
            
        self.assertEqual([1,'f11','f12','f13'], chunk[0])
        self.assertEqual([2,'f21','f22','f23|f24'], chunk[1])
        self.assertEqual([3, 'f31', 'f32', 'f33f41f42f43f51f52'], chunk[2])
        self.assertEqual([6, 'f61', 'f62', 'f63'], chunk[3])

if __name__ == '__main__':
    unittest.main()
