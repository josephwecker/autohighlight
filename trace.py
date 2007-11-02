indent = 0

from sys import stdout
import sys

def trprint(*args):
    global indent
    sys.stdout.write(indent * "   ")
    sys.stdout.write(*args)
    sys.stdout.write("\n")

def trenter(name):
    global indent
    trprint("ENTERING %s:" % name)
    indent += 1

def trleave(name):
    global indent
    indent -= 1
    trprint("LEAVING %s." % name)

def trace(func, printArgs):
    def inner(*args):
        global indent

        displayArgsString = '...'
        if printArgs:
            if type(printArgs).__name__ == 'list':
                displayArgs = []
                for i in range(len(args)):
                    if i in printArgs:
                        displayArgs += [str(args[i])]
                    else:
                        displayArgs += ['...']
                displayArgsString = ', '.join(displayArgs)
            else:
                displayArgsString = ', '.join( [ str(arg) for arg in args[:printArgs]] )

        trenter( "%s(%s)" % (func.__name__, displayArgsString) )
        rt = func(*args)
        trleave( "%s(%s) = %s" % (func.__name__, displayArgsString, rt) )

        return rt
    return inner

def funtrace(func, printArgs):
    """FUNTrace is one of the niftiest little utilities we wrote"""
    func.im_class.__dict__[func.__name__] = trace(func, printArgs)
    return func


