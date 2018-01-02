import unittest
from core.utils.report import SimpleReport


class ReportTest(unittest.TestCase):

    def test_simple_report(self):
        r = SimpleReport('SAMPLE REPORT')
        r.add('Section-1', '1st Value', 1)
        r.add('Section-1', '2nd Value', 2.123)
        r.add('Section-1', '3rd Value', 'Hello World')
        r.add('Section-2', '1st Value', 1)
        r.add('Section-2', '2nd Value', 2.123)
        r.add('Section-2', '3rd Value', 'Hello World')

        s = '\n'
        s += '============================================================\n'
        s += '                       SAMPLE REPORT                        \n'
        s += '============================================================\n'
        s += '\n'
        s += '                         Section-1                          \n'
        s += '1st Value..................................................1\n'
        s += '2nd Value..............................................2.123\n'
        s += '3rd Value........................................Hello World\n'
        s += '\n'
        s += '                         Section-2                          \n'
        s += '1st Value..................................................1\n'
        s += '2nd Value..............................................2.123\n'
        s += '3rd Value........................................Hello World\n'

        self.assertEqual(str(r), s, 'String representation of report is not correct.')

if __name__ == '__main__':
    unittest.main()