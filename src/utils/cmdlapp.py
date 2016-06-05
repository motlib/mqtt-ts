'''Base-class for simple command-line tools.'''

__author__ = 'Andreas <andreas@a-netz.de>'


import logging
from argparse import ArgumentParser


class CmdlApp():
    def __init__(self):
        pass

    def setup_args(self):
        self.parser = ArgumentParser()

        self.parser.add_argument(
            '-v', '--verbose',
            help='Enable verbose logging output.',
            action='store_true');

        self.parser.add_argument(
            '-l', '--logfile',
            help='Log output to logfile.',
            default=None)

    
    def setup_logging(self):
        '''Set up the logging framework.'''

        if self.args.verbose:
            level = logging.DEBUG
            levelname = 'debug'
        else:
            level = logging.WARNING
            levelname = 'warning'
        
        lcfg = {
            'level': level,
            'format': '%(asctime)s %(levelname)s: %(message)s',
            }

        if self.args.logfile != None:
            lcfg['filename'] = self.args.logfile
            lcfg['filemode'] = 'a'

        logging.basicConfig(**lcfg)

        msg = "Logging system initialized to level '{0}'."
        logging.debug(msg.format(levelname))

        
    def run(self):
        self.setup_args()
        self.args = self.parser.parse_args()

        self.setup_logging()


        self.main_fct()

