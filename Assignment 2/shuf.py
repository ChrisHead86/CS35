#!/usr/local/cs/bin/python3.10
import argparse, string, random, sys
class shuf:
    def __init__(self, l):
        self.l = l

    def shuf(self, num=""):
        #we set the length and parser and shuffle the lines
        lent = len(self.l)
        parser = argparse.ArgumentParser()
        random.shuffle(self.l)
        
        
        #we now set up structural pattern matching for num
        match num:
            #now we set up our cases
            case "":
                for x in range(lent):
                    print(self.l[x])
            case non_empty:
                try: 
                    y = int(num)
                    assert (y>=0)
                except:
                    parser.error("Error: Invalid Count")
                for i in range(int(num)):
                    print(random.choice(self.l))

    def repeat(self, num=""):
        lent = len(self.l)
        parser = argparse.ArgumentParser()
        match num:
            case "":
                while True:
                    print(random.choice(self.l))
            case non_empty:
                try:
                    count = int(num)
                    assert (count >= 0)
                except:
                    parser.error("ERROR: INVALID CNT")

                for i in range(int(num)):
                    print(random.choice(self.l))






#we now define main()
def main():

    parser = argparse.ArgumentParser(description = "Write a random permutation of the input lines to standard output.\n")
    #we now use parser for each of the arguments in shuf

    parser.add_argument("file", nargs = "*", help = "File Name")
    #NOT VALID CODE value 10 if not included
    parser.add_argument('-n', '--number', action = "store", dest = "counting", default = "", help = 'some number') # integer number, no default nor required, so if omitted it is None
    parser.add_argument("-i", '--input-range', action = "store", dest = "input_range", help = "Treat the numbers as input line")
    parser.add_argument("-e", "--echo", action = "store_true", dest = "echo", help = "treat each ARG as an input line")
    parser.add_argument("-r", "--repeat", action = "store_true", dest = "repeat", help = "output lines can be repeated")
    output = []
    args = parser.parse_args()

   # match vars(args): # args is an argparse.Namespace object, vars() returns it as a dictionary instead, which makes pattern matching easier
    #    case { 'filename': filename, 'count': 10 }: # this matches the default case where count is 10
     #       print('this is the default case') # you can do any sort of logic here, function calls etc in your shuf
      #  case { 'filename': filename, 'count': count, 'number': number }:
       #     if number is None: # now we have a count that isn't 10, but number was not spec
        #        print('number has been omitted')
        #case { 'number': number, **kwargs }: # here we have a specified number, and kwargs stores the rest of the dictionary
         #   print(f'number is {number} and kwargs is {kwargs}')
        #case _: # this is a default case
         #   print('format not recognized')
    
    #echo case
    if args.echo:
        output = args.file
    elif args.input_range:
        try:
            input_r = args.input_range.split('-')
            assert(len(input_r) == 2)
            LO = int(input_r[0])
            HI = int(input_r[1])
            assert(LO < HI)
            assert(not (LO < 0 or HI < 0))
            output = list(range(LO,HI+1))
        except:
            parser.error("ERROR: Range Invalid")
        try:
            assert(not args.echo)
        except:
            parser.error("ERROR: -e and -i uncombinable")
        try:
            assert(not args.file)
        except:
            parser.error("Too many operands")
    elif args.file:
        if len(args.file)==1:
            try:
                #default-take input as is
                if args.file[0]=='-':
                    for ln in sys.stdin:
                        output.append(ln.rstrip('\n'))
                #all other cases
                else:
                    with open(args.file[0]) as input:
                        for ln in input.readlines():
                            output.append(ln.rstrip('\n'))
            except:
                parser.error("ERROR: Unable to open file")
                return
        else:
            parser.error("ERROR: More Arguments than able")
    else:
        for ln in sys.stdin:
            output.append(ln.rstrip('\n'))

    sh = shuf(output)

    if (args.repeat):
        sh.repeat(args.counting)
    else:
        sh.shuf(args.counting)

if __name__ == "__main__":
    main()






