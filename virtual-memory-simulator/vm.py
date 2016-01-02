import unittest

'''Classes to model virtual memory'''

class Access(object):
    
    @staticmethod
    def address_to_page_num(address_str):
        #Convert from hex to integer
        address = int(address_str,16)
        #Get string of binary representation of virtual address
        bits = bin(address)[2:]
        #If necessary, pad out to 32 bits
        bits = ''.join(['0' for x in range(0,32-len(bits))]) + bits
        assert len(bits) == 32

        #List should be of the form
        #'[20 page bits][12 offset bits]'
        page_bits = bits[:20]
        #Convert page bits to integer
        return int(page_bits,2)

    def __init__(self,address_str,access_char):
        self.page_num = self.address_to_page_num(address_str) 
        self.access_type = access_char

    def __repr__(self):
        return str(self.page_num) + ' ' + self.access_type

    def __str__(self):
        return self.__repr__()    

class PageTable(object):
    #20 bits to address the page table
    NUMENTRIES = 1048576

    '''Primary functions'''

    #Construct the page table with an empty dictionary large enough to 
    #accomodate every PTE in a 32-bit address space.
    #Also initialize bookkeeping counters and logs.
    def __init__(self,num_frames):
        #Maximum number of frames in main memory will be set at runtime
        self.num_frames = num_frames
        
        #Create dictionary
        self.table = {}
        
        #Create 1-based list to log the accesses
        #Initialize log[0] with filler for more intuitive access later on
        self.log = ['William Engler presents: Page Table 2: The Pagening. This time, it\'s virtual.']
        #Keep count of accesses, faults, and writes
        self.access_count = 0
        self.fault_count = 0
        self.write_count = 0
        self.valid_count = 0

    #This will be the main entry point to the PageTable object
    #This function will dispatch a memory access to appropriate
    #member functions depending on the access's type and state of the page table
    def request(self,access):
        self.access_count += 1
        #if self.access_count % 10000 == 0:
        #   print "Reached " + str(self.access_count)
        
        #Start the log for this access
        self.log.append('{0}:\t\t'.format(str(self.access_count)))

        page_num = access.page_num
        #Is this request a hit or a miss?
        if not self.is_valid_page_num(access.page_num):
            self.miss(page_num)
        else:
            self.hit(page_num)

        #Is this request a read or a write?
        if access.access_type == 'R':
            self.read(page_num)
        elif access.access_type == 'W':
            self.write(page_num)
        else:
            #Unexpected access type
            assert False

    '''Request outcomes'''

    def miss(self,page_num):
        self.fault_count += 1

        if self.valid_count == self.num_frames:
            self.replace()
        else:
            self.concat_to_log('page fault - no eviction')

        #Make valid. If necessary, make the PTE
        if page_num not in self.table:
            self.table[page_num] = PTE(page_num)
        else:
            self.table[page_num].is_valid = True

        #Let the algorithm know that we've added a valid PTE
        self.add_valid_PTE(self.table[page_num])
        self.valid_count += 1
        

    def hit(self,page_num):
        self.concat_to_log('hit')

    def read(self,page_num):
        self.table[page_num].is_referenced = True
        pass

    def write(self,page_num):
        self.table[page_num].is_dirty = True
        self.table[page_num].is_referenced = True
        pass

    def replace(self):
        
        #Use a page replacement algorithm to select a victim PTE
        page_num_to_evict = self.select_victim()
        victim = self.table[page_num_to_evict]
        
        #Write the appropriate message to the log
        if victim.is_dirty:
            self.concat_to_log('page fault - evict dirty')
            self.write_count += 1
        else:
            self.concat_to_log('page fault - evict clean')
        
        #Clear the victim PTE's bits
        self.valid_count -= 1
        victim.evict()

    '''To be monkey patched'''
    def select_victim(self):
        assert False

    def add_valid_PTE(self):
        assert False

    '''Utilities'''

    def is_valid_page_num(self,page_num):
        return page_num in self.table and self.table[page_num].is_valid

    #append message to end of log entry corresponding to access being processed
    def concat_to_log(self,message):
        self.log[self.access_count] = self.log[self.access_count] + message

class PTE(object):
    def __init__(self,page_num):
        #This simulation does not require that our PTEs actually point to an address
        #Three status bits are sufficient
        self.is_valid = True
        self.is_referenced = True
        self.is_dirty = False
    
        self.page_num = page_num

    def evict(self):
        self.is_valid = False
        self.is_referenced = False
        self.is_dirty = False

'''Tests'''

class PageTableTests(unittest.TestCase):

    def setUp(self):
        self.pTable = PageTable(8)
        self.access1 = Access('123','R')
        self.access2 = Access('124','R')
        self.access3 = Access('125','W')
        self.page_num = 0
        def do_nothing_on_add(page_num):
            pass
        self.pTable.add_valid_PTE = do_nothing_on_add

    def tearDown(self):
        del self.pTable

    def test_compulsory_miss(self):
        access = Access('123','R')
        pTable = self.pTable;
        pTable.request(access)
        self.assertTrue(pTable.table[self.page_num].is_valid)

    def test_hit(self):
        pTable = self.pTable
        pTable.request(self.access1)
        pTable.request(self.access2)
        self.assertCounts(2,1,0)

    def test_write(self):
        pTable = self.pTable
        pTable.request(self.access1)
        pTable.request(self.access2)
        pTable.request(self.access3)
        self.assertCounts(3,1,1)

    def test_evict(self):
        pTable = self.pTable
        access_list = [Access(hex(x*4096 + 1),'R') for x in range(0,9)]
        
        #Eviction function that always evicts page #1
        def evict_arbitrary():
            pTable.valid_count -= 1
            return 1

        #Monkey patch!
        pTable.select_victim = evict_arbitrary
        
        #Access one more page than our page table's capacity
        for access in access_list:
            pTable.request(access)
        
        #Every page numbered two or greater should still be valid
        for page_num in range(2,9):
            self.assertTrue(pTable.table[page_num].is_valid)
                
        #Page 1 should have been evicted
        self.assertFalse(pTable.table[1].is_valid)

    def assertCounts(self,accesses,faults,writes):
        pTable = self.pTable
        self.assertEqual(pTable.access_count,accesses)
        self.assertEqual(pTable.fault_count,faults)
        self.assertEqual(pTable.write_count,writes)