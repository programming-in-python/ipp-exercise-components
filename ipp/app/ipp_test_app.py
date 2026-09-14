##
# MIT License
#
# Copyright (c) 2020 - 2025 Andrew D. King
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Command-line test harness for exercising the course sample code.
"""

import argparse
import logging
import traceback
from time import sleep

from ipp.common import config_const
from ipp.common.config_util import ConfigUtil

LOG_FORMAT = "%(asctime)s:::%(thread)d:%(name)s.%(module)s.%(funcName)s()[%(lineno)s]:%(levelname)s:%(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)


class IppTestApp:
    """
    A minimal test application used across the IPP course exercises.
    """

    def __init__(self):
        """
        Initialize the app in a not-yet-started state.
        """
        logging.info("Initializing IPP Test App...")

        self.is_started = False

    def is_app_started(self) -> bool:
        """
        Report whether the app has been started.
        """
        return self.is_started

    def start_app(self):
        """
        Start the IPP Test App, loading its configuration first.
        """
        logging.info("Starting Ipp Test App...")

        # NOTE: Loading the config file may not be necessary for every use case
        #       If not, the following SLOC's can be commented out and replaced
        #       with alternative logic.
        config_util = ConfigUtil()

        if config_util.is_config_data_loaded():
            # TODO: Add other startup logic here

            self.is_started = True

            logging.info("Ipp Test App started.")
        else:
            logging.error(
                "Failed to load config file and properly initialize app. Ipp Test App not started."
            )

    def stop_app(self, code: int):
        """
        Stop the app and log the given exit code.

        Args:
            code: The exit code to record for the shutdown.
        """
        if self.is_started:
            logging.info("Ipp Test App stopping...")

            # TODO: Add other shutdown logic here

            logging.info("Ipp Test App stopped with exit code %s.", str(code))
        else:
            logging.info("Ipp Test App not yet started.")


def main():
    """
    Run the client as a standalone application.

    The current implementation runs for roughly 65 seconds, then exits.
    """
    arg_parser = argparse.ArgumentParser(
        description="Ipp Test App for basic test functions and data set simulation as part of the Intro to Python Programming course."
    )

    arg_parser.add_argument(
        "-c",
        "--config_file",
        help="Optional custom configuration file for the Ipp Test App.",
    )

    config_file = None

    try:
        args = arg_parser.parse_args()
        config_file = args.config_file

        logging.info("Parsed configuration file arg: %s", config_file)
    except Exception:
        logging.info("No arguments to parse.")

    # init ConfigUtil
    config_util = ConfigUtil(config_file)
    ita = None

    try:
        # init Ipp Test App
        ita = IppTestApp()

        # start Ipp Test App
        ita.start_app()

        # check if Ipp Test App should run forever
        run_forever = config_util.get_boolean(
            config_const.IPP_TEST_APP, config_const.RUN_FOREVER_KEY
        )

        if run_forever:
            # sleep ~5 seconds every loop
            while True:
                sleep(5)

        else:
            # run Ipp Test App for ~65 seconds then exit
            if ita.is_app_started():
                sleep(65)
                ita.stop_app(0)

    except KeyboardInterrupt:
        logging.warning("Keyboard interruption for Ipp Test App. Exiting.")

        if ita:
            ita.stop_app(-1)

    except Exception as e:
        # handle any uncaught exception that may be thrown
        # during Ipp Test App initialization
        logging.error("Startup exception caused Ipp Test App to fail. Exiting.")
        traceback.print_exception(type(e), e, e.__traceback__)

        if ita:
            ita.stop_app(-2)

    # unnecessary
    logging.info("Exiting Ipp Test App.")
    exit()


if __name__ == "__main__":
    """
    Attribute definition for when invoking as app via command line
    
    """
    main()


def parse_args(args):
    """
    Parse command line args.

    Args:
        args: The arguments to parse.
    """
    logging.info("Parsing command line args...")
