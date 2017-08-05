import sys
args = sys.argv
fileread = False
readfrom = ""
frameskipratevalue = 1
def help():
    print "Command line arguments:"
    print "--------------------------"
    print "'--help': Displays information about command line arguments"
    print "'--readfromfile' <file> : Processes data from a video file named <file>"
    print "'--frameskiprate' <number>: Sets the amount of frames skipped per scan to <number>"
    print "'version' : Displays current version"
    exit(0)
def readfromfile(fname):
    globals()["fileread"] = True
    globals()["readfrom"] = fname
def frameskiprate(rate):
    globals()["frameskipratevalue"] = int(rate)
def version():
    print "Version to be determined"
    exit(0)
argbinding = {
    "--help" : (help,False),
    "--readfromfile" : (readfromfile,True),
    "--frameskiprate" : (frameskiprate,True),
    "--v" : (version,False)
}
def processArgs():
    for i in range(0,len(args)):
        a = args[i]
        if a in argbinding:
            if argbinding[a][1]:
                i += 1
                argbinding[a][0](args[i])
            else:
                argbinding[a][0]()
