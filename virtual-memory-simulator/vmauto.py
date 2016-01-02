import vmsim
import sys

def main():
    '''Create txt file with format cmd line args then results'''
    

    sys.stdout = open(sys.argv[1],'w')
    tnames = ['gcc.trace','bzip.trace']
    frame_nums = [8,32,64,128]
    algs = ['clock','nru','rand','opt']
    
    for alg in algs:
        for tname in tnames:
            for num in frame_nums:
                cmd = ['vmsim', '-n',str(num),'-a',alg, tname]
                vmsim.parse_cmd(cmd)


if __name__ == "__main__":
    main()