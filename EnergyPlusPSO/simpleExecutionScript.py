import math, sys, pdb

def calculateFunction( array_of_values ):
    alpha = .05  # Half way between easy and hard.
    euclidean = sum( [ k**2 for k in array_of_values])**.25
    return (euclidean ** .5) * ( 2 * alpha * math.sin(euclidean))

def doMain():
    try:
        vars = []

        lines = open("Params.txt").readlines()

        if lines[0].startswith("NOOP"):
            sys.stdout.write("1\n")

        vars = [ float(line.split(":")[1]) for line in lines]

        sys.stdout.write("0\n")
        sys.stdout.write( "%s\n" % calculateFunction(vars))
        
    except:
        sys.stdout.write( "1\n")

    return 

if __name__ == "__main__":
    doMain()
