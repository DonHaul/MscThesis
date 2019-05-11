import sys,getopt

from optparse import OptionParser


def main(argv):

    a =ParsingInputs()

    print(a)


def ParsingInputs(argv):
    parser = OptionParser()
    parser.add_option("-a", "--aruco")
    parser.add_option("-s", "--settings")
    parser.add_option("-c", "--cameras",action="append")
    
    parser.add_option("-f", "--file", dest="filename",
                    help="write report to FILE", metavar="FILE")
    parser.add_option("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    print(options)



if __name__ == '__main__':
    main(sys.argv[1:])