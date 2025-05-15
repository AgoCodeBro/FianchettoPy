import fianchetto.cli.main_cli as cli
import argparse

def main():
    parser = argparse.ArgumentParser()
    cli_view_modes = parser.add_mutually_exclusive_group()
    cli_view_modes.add_argument("-l", "--light", action="store_true", help="Runs the cli with lightmode in mind")
    cli_view_modes.add_argument("-r", "--raw", action="store_true", help="Runs the cli using letters to represent the pieces")
    args = parser.parse_args()
    if args.light:
        cli.main(1)


    elif args.raw:
        cli.main(2)

    else:
        cli.main(0)


if __name__ == "__main__":
    main()