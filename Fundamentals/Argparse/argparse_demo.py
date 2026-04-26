import argparse

parser = argparse.ArgumentParser("Write the Usage example here" , description= "How it works ?")

parser.add_argument("argument",help="Summary that will be shown in --help")

parser.add_argument("positional")

parser.add_argument("--optional","--alias")

subparser = parser.add_subparsers(dest="commands")

subcmd1_parser = subparser.add_parser("cmd1")


args = parser.parse_args()
print(args)

if args.commands == "cmd1":
    print("cmd1 is called !")






