import argparse
import sys
import os
import json

args = None
def parse() -> None:
    """Parse call arguments and check values

    Exit program if an error occured
    """
    global args

    # CLI call parser
    parser = argparse.ArgumentParser(
        prog="run_workflow.py",
        description="Run a workflow automatically with the option --behavior delete (tke workflow need to not have commentary inside)",
        epilog="",
    )

    parser.add_argument(
        "--path_file",
        metavar="/path/to/file/to/create",
        action="store",
        dest="path_file",
        help="Path to save the workflow",
        required=True,
    )

    parser.add_argument(
        "--config",
        metavar="config.ini",
        action="store",
        default="config.ini",
        dest="config",
        help="Path to the config file",
        required=False,
    )

    args = parser.parse_args()

def run(args) -> None:
    """Run each step of the workflow
    """

    with open(args.path_file,"r") as file :
        data = json.load(file)

    steps = list(data["workflow"]["steps"].keys())
    for step in steps :
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s " + step + " --behavior DELETE")

def main() -> None:
    """Main function

    Return 0 if success, 1 if an error occured
    """

    parse()

    run(args)

    sys.exit(0)

if __name__ == "__main__":
    main()