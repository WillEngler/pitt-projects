import vmsim
import sys

def main():
    '''Create txt file with format cmd line args then results'''
    

    sys.stdout = open(sys.argv[1],'w')
    tnames = ['bzip.trace']
    frame_nums = [8,32,64,128]
    refresh_rates = [300,500,750,1000,2000]
    
    for refresh_rate in refresh_rates:
        for tname in tnames:
            for num in frame_nums:
                cmd = ['vmsim', '-n',str(num),'-a','nru', '-r',refresh_rate, tname]
                vmsim.parse_cmd(cmd)


if __name__ == "__main__":
    main()