import unittest
from demule.utils.report import SimpleReport


class ReportTest(unittest.TestCase):

    def test_simple_report(self):
        r = SimpleReport('SAMPLE REPORT')
        r.add('Section-1', '1st Value', 1)
        r.add('Section-1', '2nd Value', 2.123)
        r.add('Section-1', '3rd Value', 'Hello World')
        r.add('Section-2', '1st Value', 1)
        r.add('Section-2', '2nd Value', 2.123)
        r.add('Section-2', '3rd Value', 'Hello World')

        print(r)

if __name__ == '__main__':
    unittest.main()