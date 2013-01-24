import sys

__author__ = 'xl'


def make_progress(cur_val, end_val=100, bar_length=40, leading_massage=""):
    percent = float(cur_val) / end_val
    hashes = '#' * int(round(percent * bar_length))
    msg = ("\r{2}[{0:.<%ds}]{1:3.02f}%%"%bar_length).format(hashes,percent*100,leading_massage)

    sys.stdout.write(msg)
    sys.stdout.flush()

def run(leading_massage = "", success_massage="Done", bar_length=10):
    for i in range(301):
        make_progress(i, 300, bar_length, leading_massage)
        for j in range(500000): pass
    done_massage = ("\r{1}\n").format(leading_massage, success_massage)
    sys.stdout.write(done_massage)
    sys.stdout.flush()

#run("Downloading XL", "XL is Downloaded.", 20)


