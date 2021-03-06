'''Base-class for simple command-line tools.'''

__author__ = 'Andreas <andreas@a-netz.de>'


from argparse import ArgumentParser
import logging
import signal
import sys
import yaml


class CmdlApp():
    def __init__(self):
        # set all config values to default values
        self.cmdlapp_config()


    def cmdlapp_config(self, has_cfgfile=False, reload_on_hup=False):
        self.has_cfgfile = has_cfgfile
        self.reload_on_hup = reload_on_hup


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

        if self.has_cfgfile == True:
            self.parser.add_argument(
                '-c', '--cfg',
                help='Path to the YAML config file.')

    
    def setup_logging(self):
        '''Set up the logging framework.'''

        if self.args.verbose:
            level = logging.DEBUG
            levelname = 'debug'
        else:
            level = logging.INFO
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
        logging.info(msg.format(levelname))


    def load_cfgfile(self):
        '''Load the configuration file.

        The file is specified by command line argument `logfile`.

        '''
        
        msg = "Loading config file '{0}'."
        logging.info(msg.format(self.args.cfg))

        try:
            with open(self.args.cfg, 'r') as f:
                self.cfg = yaml.load(f)
        except Exception as ex:
            msg = "Failed to load config file '{0}': {1}"

            if self.args.verbose:
                logging.exception(msg.format(self.args.cfg, ex))
            else:
                logging.error(msg.format(self.args.cfg, ex))

            sys.exit(1)


    def run(self):
        '''Function to start the actual work. 

        This function is called by the deriving class to start
        everything. Command line arguments are parsed, the config file
        is loaded if necessary and then the `main_fct` function
        (implemented by the subclass) is called to do some work.'''

        self.setup_args()
        self.args = self.parser.parse_args()

        self.setup_logging()

        if self.reload_on_hup:
            # register SIGHUP listener to reload config file. 
            signal.signal(signal.SIGHUP, self.sighup_handler)

        if self.has_cfgfile:
            self.load_cfgfile()

        try:
            self.main_fct()
        except KeyboardInterrupt:
            logging.info('Terminating due to Ctrl-C. Good bye.')
        except:
            logging.exception('Main function failed.')
    

    def on_reload(self):
        '''Handler for reloading the configuration. 

        Called when a SIGHUP signal is received. By default reloads
        the configuration from file.'''

        if self.reload_on_hup:
            msg = 'Reloading configuration due to SIGHUP signal.'
            logging.info(msg)

            self.load_cfgfile()

            
    def sighup_handler(self, sig, stack):
        '''Handler for the SIGHUP signal.

        Triggers reloading of the configuration file.'''
        
        if sig == signal.SIGHUP and self.reload_on_hup:
            self.on_reload()
        else:
            # ignore any other signal
            pass
