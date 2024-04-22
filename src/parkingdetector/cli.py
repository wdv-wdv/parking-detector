import click
import os
import os.path
import config

from __about__ import __version__

#@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="parkingdetector")
@click.command()
@click.argument('filename', type=click.Path(exists=True))
def parkingdetector(filename):

    config.Config()
    if (os.path.isfile(filename)):
        print(f"filename: {filename}")
        import process
        process.execute(filename)

