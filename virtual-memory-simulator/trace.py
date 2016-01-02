import vmsim
import sys

def main():
    trace_list = vmsim.file_to_trace_list(sys.argv[1])
    f = open(sys.argv[2],'w')
    for access in trace_list:
        f.write(str(access.page_num) + '\n')
    f.close()

if __name__ == '__main__':
    main()