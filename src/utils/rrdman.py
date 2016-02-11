import datetime
import logging
import os
import subprocess
from time import mktime


class RRDManager():
    def __init__(self, datadir, graphdir):
        self.datadir = datadir
        self.graphdir = graphdir

        
    def get_rrdfile(self, signal):
        filename = signal + '.rrd'
        
        filepath = os.path.join(self.datadir, filename)

        return filepath


    def get_graphfile(self, signal, duration):
        filename = signal + '_' + duration + '.png'
        
        filepath = os.path.join(self.graphdir, filename)

        return filepath


    def check_rrd(self, signal):
        filepath = self.get_rrdfile(signal)

        if not os.path.isfile(filepath):
            self.create_rrd(signal)


    def create_rrd(self, signal):
        filepath = self.get_rrdfile(signal)
        
        cmd = [
            'rrdtool',
            'create',
            filepath,
            # one minute steps
            '--step', '60',
            'DS:value:GAUGE:120:U:U',
            # average over 5 values (5 minutes), store 288 = 24h
            'RRA:AVERAGE:0.5:5:288',
            # average over 20 values (20 minutes), store 2160 = 30d
            'RRA:AVERAGE:0.5:20:2160'
        ]

        subprocess.check_call(cmd)


    def update_rrd(self, signal, value):
        filepath = self.get_rrdfile(signal)

        valstr = 'N:' + str(value)
            
        cmd = [
            'rrdtool',
            'update',
            filepath,
            valstr
        ]
        
        subprocess.check_call(cmd)

        msg = "Updated rrd '{0}' with value {1}."
        logging.debug(msg.format(filepath, value))

        
    def create_graph(self, name, signals, title=''):
        now = datetime.datetime.now()
        delta = datetime.timedelta(hours=6)
        start = int(mktime((now - delta).timetuple()))

        graphfile = self.get_graphfile(name, '6h')

        cmd = [
            'rrdtool',
            'graph',
            graphfile,
            '--start', str(start),
            '-w', '1024',
            '-h', '768',
            '--title', title,
        ]

        for signal in signals:
            rrdfile = self.get_rrdfile(signal)
            cmd.append(
                'DEF:' + signal + '=' + rrdfile + ':value:AVERAGE')

        for signal in signals:            
            cmd.append(
                'LINE2:' + signal)

        subprocess.check_call(cmd)

        msg = "Created graph '{0}'."
        logging.info(msg.format(name))
