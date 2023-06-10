"""Copy files from a source directory to a destination directory."""

import argparse
import os
import shutil
import sys
from pathlib import Path

from rich.console import Console

DEFAULT_GLOB = "*.pdf"
DEFAULT_SOURCE_DIRECTORY = "_resources/download/research/papers/key"
DEFAULT_DESTINATION_DIRECTORY = "_site/download/research/papers/key"

DEFAULT_CONSOLE_STYLE = "bold blue"

console = Console()


def copy_files(
    source_dir: str, destination_dir: str, file_glob: str = DEFAULT_GLOB
) -> None:
    """Copy files from the source directory to the destination directory."""
    # create pathlib Path objects out of the two directories
    source_path = Path(source_dir)
    destination_path = Path(destination_dir)
    # create the destination directory if it doesn't exist
    destination_path.mkdir(parents=True, exist_ok=True)
    # iterate over all files in the source directory
    source_path_glob_iterator = source_path.glob(file_glob)
    # keep track of the number of files copied
    file_count = 0
    for file_path in source_path_glob_iterator:
        # construct the destination file path
        destination_file = destination_path / file_path.name
        # copy the file to the destination directory
        shutil.copy2(file_path, destination_file)
        # increment the file counter
        file_count = file_count + 1
    # output some debugging information about the completed copy
    console.print(
        f":tada: Finished copying {file_count} files", style=DEFAULT_CONSOLE_STYLE
    )


def main() -> None:
    """Perform the steps for the main function."""
    # parse the command-line arguments using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source")
    parser.add_argument("-d", "--destination")
    parser.add_argument("-f", "--force", action="store_true")
    args = parser.parse_args()
    # determine the valid directory for the source
    source_directory = DEFAULT_SOURCE_DIRECTORY
    # do not run the script unless quarto is rendering
    # all of the files (i.e., do not run during preview)
    if not os.getenv("QUARTO_PROJECT_RENDER_ALL") and not args.force:
        sys.exit()
    # use the default source directory if none was specified
    if args.source is None:
        console.print(
            f":clap: Using the default source directory of {source_directory}\n",
            style=DEFAULT_CONSOLE_STYLE,
        )
    # use the specified source directory
    else:
        console.print(
            ":clap: Using {args.source} as specified by --source",
            style=DEFAULT_CONSOLE_STYLE,
        )
        source_directory = args.source
    # use the default destination directory
    destination_directory = DEFAULT_DESTINATION_DIRECTORY
    if args.source is None:
        console.print(
            f":clap: Using the default destination directory of {destination_directory}\n",
            style=DEFAULT_CONSOLE_STYLE,
        )
    # use the specified destination directory
    else:
        console.print(
            ":clap: Using {args.destination} as specified by --destination",
            style=DEFAULT_CONSOLE_STYLE,
        )
        source_directory = args.source
    # perform the copy from the source to the desination
    copy_files(source_directory, destination_directory)


if __name__ == "__main__":
    # run the main function
    # that controls all of the file copies
    main()
