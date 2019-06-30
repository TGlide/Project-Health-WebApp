import os
import glob

pugs = glob.glob("templates\\registration\\*.pug")
for pug in pugs:
    os.system("pypugjs -c django {} {}".format(pug, pug[:-3] + "html"))