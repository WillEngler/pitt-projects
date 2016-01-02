import unittest
import vm
import alg
import sys


def main():
    parse_cmd(sys.argv)

'''Utilities'''
def parse_cmd(args):
    print args
    DEFAULT_REFRESH = 50

    kludge = {
        'opt':alg.Optimal,
        'nru':alg.NRU,
        'rand':alg.Random,
        'clock':alg.Clock
    }

    if len(args) is not 6 and len(args) is not 8:
        print str(len(args))
        exit_on_bad_cmd()
    num_frames = int(args[2])
    alg_name = args[4]
    if args[5] == '-r':
        refresh_rate = args[6]
        fname = args[7]
    else:
        refresh_rate = DEFAULT_REFRESH
        fname = args[5]
        #print fname

    algorithm = kludge[alg_name]
    runner = Runner()
    if algorithm is alg.NRU:
        runner.run_single(algorithm,num_frames,fname, refresh_rate=refresh_rate)
    else:
        runner.run_single(algorithm,num_frames,fname)

    print ''

def exit_on_bad_cmd():
    print "Expected input: ./vmsim.py -n <numframes> -a <opt|clock|nru|rand> [-r <refresh>] <tracefile>"
    sys.exit()

def file_to_trace_list(fname):
        trace_list = []
        with open(fname, 'r') as sample:
            for line in sample:
                tokens = line.split()
                trace_list.append( vm.Access(tokens[0],tokens[1]) )
        return trace_list

class UtilityTests(unittest.TestCase):
    
    def test_file_to_trace_list(self):
        expected_list = [vm.Access('0041f7a0','R'),vm.Access('13f5e2c0','R'), vm.Access('31348900','W'), vm.Access('004758a0', 'R')]
        computed_list = file_to_trace_list('sample.trace')
        self.assertEqual(str(expected_list),str(computed_list),'Lists not equal: \nExpected: ' + str(expected_list) + '\nComputed: ' + str(computed_list))

    def test_address_to_page_num(self):
        #15 1's in binary converted to hex.
        #All phsical address bits set to 1
        #three least significant page bits set to 1
        address_str = '7fff'
        expected = 7
        computed = vm.Access.address_to_page_num(address_str)
        self.assertEqual(expected,computed)


class Runner(object):
    def __init__(self):
        pass

    def run_single(self,algorithm,frames,trace_name, **kwargs):
        trace_list = file_to_trace_list(trace_name)
        self.trace_list = trace_list

        pTable = vm.PageTable(frames)
        self.pTable = pTable

        algorithm = algorithm(pTable,trace_list, **kwargs)
        self.algorithm = algorithm

        algorithm.run()
        
        result = Result(frames,pTable.access_count,pTable.fault_count,pTable.write_count)
        self.result = result

        '''
        for line in pTable.log:
            print line
        '''
        print result

class RunnerTests(unittest.TestCase):
    def setUp():
        pass
    def tearDown():
        pass


class Result(object):
    def __init__(self,frames,accesses,faults,writes):
        self.frames = frames
        self.accesses = accesses
        self.faults = faults
        self.writes = writes

    def misurda_format(self):
        return 'Number of frames:\t\t{0}\nTotal memory accesses:\t\t{1}\nTotal page faults:\t\t{2}\nTotal writes to disk:\t\t{3}'.format(self.frames,self.accesses,self.faults,self.writes)


    def __repr__(self):
        return self.misurda_format()


if __name__ == '__main__':
    main()
