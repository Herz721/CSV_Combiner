from unittest.mock import patch
import CSV_Combiner
import generatefixtures

class Test(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        generatefixtures.main()
        return
        
    @classmethod
    def tearDownClass(cls):
        return

    def setUp(self):

    def test_file_not_found(self):
        args = ['CSV_Combiner.csv', 'clothing.csv', 'file_not_found.csv', 'combined.csv']
        combiner = CSV_Combiner(args)
        with mock.patch('sys.stdout') as fake_stdout:
            combiner.combine
        fake_stdout.assert_has_calls([
            mock.call.write('Something'),
            mock.call.write('\n')
        ])

    def test_case1(self):
        print self.number
        self.assertEqual(self.number,10,msg='Your input is not 10')
        
    def test_case2(self):
        print self.number
        self.assertEqual(self.number,20,msg='Your input is not 20')

    @unittest.skip('暂时跳过用例3的测试')
    def test_case3(self):
        print self.number
        self.assertEqual(self.number,30,msg='Your input is not 30')


    def tearDown(self):
        print 'Test over'
        
if __name__=='__main__':
    unittest.main()