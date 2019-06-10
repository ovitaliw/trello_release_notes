"""Handle the commandline, perform the archiving and creating the release notes"""
from configargparse import ArgumentParser


def main(args):
    """Run through and execute the archiving"""
    raise NotImplementedError


if __name__ == "__main__":
    parser = ArgumentParser(
        default_config_files=["~/.trello_release_settings.ini"],
        description="A tool to archive what you've done in trello to a release like Alice Goldfuss does",
    )
    parser.add_argument(
        "-c", "--config", help="A path to a config file for these options"
    )
    args = parser.parse_args()
    main(args)
