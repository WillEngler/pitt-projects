import vm
import vmsim
import unittest
import random
import sys

'''Page replacement algorithms'''
class Optimal(object):
    
    NOT_USED_AGAIN = sys.maxint

    def __init__(self,pTable,trace_list):
        self.pTable = pTable
        self.trace_list = trace_list
        self.valid_list = []
        self.access_times = self.preprocess_access_times()

        def select_victim():
            assert  self.valid_list
            access_count = self.pTable.access_count
            
            #initialize victim
            latest_use = self.traverse_frame_access_list(self.access_times[self.valid_list[0].page_num],access_count)
            victim = self.valid_list[0]
            #look for the frame that 
            for candidate in self.valid_list[1:]:
                access_list = self.access_times[candidate.page_num]
                next_use = self.traverse_frame_access_list(access_list,access_count)
                
                #Check if the next time the candidate will be used is the lowest we've seen so far
                if next_use > latest_use or (next_use == latest_use and not candidate.is_dirty):
                    victim = candidate
                    latest_use = next_use
                    if next_use == Optimal.NOT_USED_AGAIN and not victim.is_dirty:
                        break

            self.valid_list.remove(victim)
            return victim.page_num
        
        def add_valid_PTE(pte):
            self.valid_list.append(pte)

        pTable.select_victim = select_victim
        pTable.add_valid_PTE = add_valid_PTE

    @staticmethod
    def traverse_frame_access_list(access_list,access_count):
        for time in access_list:
            if time < access_count:
                access_list.pop(0)
            else:
                break

        if access_list:
            return access_list[0]
        else:
            return Optimal.NOT_USED_AGAIN

    def preprocess_access_times(self):
        access_times = {}
        for index in range(0,len(self.trace_list)):
            page_num = self.trace_list[index].page_num
            if page_num not in access_times:
                access_times[page_num] = [index]
            else:
                access_times[page_num].append(index)
        return access_times

    def run(self):
        for access in self.trace_list:
            self.pTable.request(access)

class OptimalTests(unittest.TestCase):
    def test_evict_most_distant(self):
        runner = vmsim.Runner()
        runner.run_single(Optimal,8,'opt_simple.trace')
        rightful_victim = runner.pTable.table[1055]
        self.assertFalse(rightful_victim.is_valid)


class Random(object):
    def __init__(self,pTable,trace_list):
        self.pTable = pTable
        self.trace_list = trace_list
        self.valid_list = []
        
        def select_victim():
            assert  self.valid_list
            victim = random.choice(self.valid_list)
            self.valid_list.remove(victim)
            return victim.page_num
        
        def add_valid_PTE(pte):
            self.valid_list.append(pte)

        pTable.select_victim = select_victim
        pTable.add_valid_PTE = add_valid_PTE

    def run(self):
        for access in self.trace_list:
            self.pTable.request(access)

class RandTests(unittest.TestCase):

    def setUp(self):
        #self.pTable = PageTable(8)
        #self.trace_list = file_to_trace_list('12.trace')
        pass

    def tearDown(self):
        #del self.pTable
        pass

    def test_evict(self):
        runner = vmsim.Runner()
        runner.run_single(Random,8,'12.trace')
        page_num_list = [1055,81758,24184,1141,201544,1187,28687,1182,1218,208986,24070]
        num_valid = 0
        for page_num in page_num_list:
            if runner.pTable.table[page_num].is_valid:
                num_valid += 1
        self.assertEqual(num_valid,8)
        

class NRU(object):
    def __init__(self,pTable,trace_list,refresh_rate):
        self.pTable = pTable
        self.trace_list = trace_list
        self.valid_list = []
        self.refresh_rate = refresh_rate
        self.refresh_count = 0

        def select_victim():
            assert  self.valid_list

            cand_list = []
            list_priority = 1
            for candidate in self.valid_list:
                cand_priority = self.assign_priority(candidate)    
                if cand_priority > list_priority:
                    cand_list = []
                    list_priority = cand_priority
                if cand_priority == list_priority:
                    cand_list.append(candidate)

            victim = random.choice(cand_list)
            self.valid_list.remove(victim)
            #print 'evicting ' + str(victim.page_num)
            return victim.page_num
        
        def add_valid_PTE(pte):
            self.valid_list.append(pte)

        pTable.select_victim = select_victim
        pTable.add_valid_PTE = add_valid_PTE

    #From scale of 1 to 4, where 4 has highest eviction priority
    @staticmethod
    def assign_priority(pte):
        if pte.is_dirty and not pte.is_referenced:
            return 4
        elif not pte.is_referenced:
            return 3
        elif pte.is_dirty:
            return 2
        else:
            return 1

    def run(self):
        for access in self.trace_list:
            self.refresh_count = (1 + self.refresh_count)  % (self.refresh_rate + 1)
            if self.refresh_count == 0:
                self.refresh()
            self.pTable.request(access)

    def refresh(self):
        for pte in self.valid_list:
            pte.is_referenced = False

class NRUTests(unittest.TestCase):
    def test_dirty(self):
        runner = vmsim.Runner()
        runner.run_single(NRU,8,'nru_dirty.trace', refresh_rate=5)
        rightful_victim = runner.pTable.table[201544]
        self.assertFalse(rightful_victim.is_valid)
    def test_clean(self):
        runner = vmsim.Runner()
        runner.run_single(NRU,8,'nru_clean.trace', refresh_rate=8)
        rightful_victim = runner.pTable.table[1182]
        self.assertFalse(rightful_victim.is_valid)
    def test_priority(self):
        pri1 = vm.PTE(42)
        pri2 = vm.PTE(42)
        pri3 = vm.PTE(42)
        pri4 = vm.PTE(42)

        pri1.is_referenced = True
        pri1.is_dirty = False
        self.assertEqual(NRU.assign_priority(pri1),1)

        pri2.is_referenced = True
        pri2.is_dirty = True
        self.assertEqual(NRU.assign_priority(pri2),2)

        pri3.is_referenced = False
        pri3.is_dirty = False
        self.assertEqual(NRU.assign_priority(pri3),3)

        pri4.is_referenced = False
        pri4.is_dirty = True
        self.assertEqual(NRU.assign_priority(pri4),4)

class Clock(object):
    def __init__(self,pTable,trace_list):
        self.pTable = pTable
        self.trace_list = trace_list
        self.clock_max = pTable.num_frames
        self.clock_list = [None for x in range(0,self.clock_max)]
        self.clock_index = 0

        def select_victim():
            while(True):
                if not self.clock_list[self.clock_index].is_referenced:
                    break
                else:
                    #print 'Unreferencing ' + str(self.clock_list[self.clock_index].page_num)
                    self.clock_list[self.clock_index].is_referenced = False
                    self.clock_index = (self.clock_index + 1) % self.clock_max

            victim_num = self.clock_list[self.clock_index].page_num
            #print 'Evicting ' + str(victim_num)
            self.clock_list[self.clock_index] = None
            return victim_num
        
        def add_valid_PTE(pte):
            #print 'adding ' + str(pte.page_num)
            self.clock_list[self.clock_index] = pte
            self.clock_index = (self.clock_index + 1) % self.clock_max

        pTable.select_victim = select_victim
        pTable.add_valid_PTE = add_valid_PTE

    def run(self):
        for access in self.trace_list:
            self.pTable.request(access)

class ClockTests(unittest.TestCase):
    def test_evict_lru(self):
        runner = vmsim.Runner()
        runner.run_single(Clock,8,'clock.trace')
        rightful_victim = runner.pTable.table[81758]
        self.assertFalse(rightful_victim.is_valid)
        rightful_victim = runner.pTable.table[24184]