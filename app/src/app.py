# usage: python3 app.py path/to/datadir (if empty default to /iexec)
# import argparse
import os
import subprocess
import sys

import imghdr
import json
from collections import OrderedDict
import yaml
import yamlordereddictloader

from color_transfer_ import ColorTransfer
from consensus import Consensus
import exceptions_ as exceptions_


class Flag:

    task_started = '[INFO] processing file - {}'
    task_ended = '[INFO] done..\n'
    execution_ended = '[INFO] Original supported files have been moved to folder "in" \n' \
                    + '[INFO] Results are saved in folder "out"'


class App:

    _SUPPORTED_IMAGES = [ 'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'jpeg', 'bmp', 'png' ]
    _CONSENSUS = 'consensus.iexec'

    def __init__(self):
        self._datadir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else '/iexec'
        self._read_input_config_file()
        try:
            self._prepare_datadir()
        except Exception as e: 
            raise exceptions_.Fatal(err=e)

    # def parseArgs(self):
    #     argParser = argparse.ArgumentParser()
    #     argParser.add_argument('datadir', required=False, help='Path to input folder', type=str)
    #     self.args = vars(argParser.parse_args())

    def _paths(self, key):
        return {
            'datadir': '{}',
            'in': '{}/in',
            'conf': '{}/input-config.yml',
            'out': '{}/out',
            'json': '{}/out/output.json'
        }[key].format(self._datadir)

    def _absolute_path(self, dirname, filename, extension=''):
        return '{}/{}{}'.format(self._paths(dirname), filename, extension)

    def _read_input_config_file(self):
        if not os.path.isfile(self._paths('conf')):
            raise exceptions_.Fatal(key='InputConfigNotFound', param=self._paths('conf'))
        try:
            self._input_config = yaml.load(open(self._paths('conf')), yamlordereddictloader.SafeLoader)
        except Exception as e:
            raise exceptions_.Fatal(err=e, key='IllegalInputConfigFormat')

    def _is_config_file(self, filename):
        return self._absolute_path('datadir', filename) == self._paths('conf')

    def _is_supported_file(self, filename):
        return ( os.path.isfile(self._absolute_path('datadir', filename))
            and not self._is_config_file(filename)
            and imghdr.what( self._absolute_path('datadir', filename) ) in self._SUPPORTED_IMAGES )

    def _prepare_datadir(self):
        datadir_content = os.listdir(self._paths('datadir'))
        os.mkdir(self._paths('in'))
        os.mkdir(self._paths('out'))
        for filename in [ f for f in datadir_content if self._is_supported_file(f) ]:
            subprocess.call([ 'mv', self._absolute_path('datadir', filename), self._paths('in') ])

    def _rename_input_files(self):
        prefix = 'original'
        for filename in os.listdir(self._paths('in')):
            old_path = self._absolute_path('in', filename)
            new_name = '{}-{}'.format(prefix, filename)
            new_path = self._absolute_path('in', new_name)
            subprocess.call([ 'mv', old_path, new_path ])

    def main(self):

        color_transfer = ColorTransfer()

        for entry in self._input_config:
            print(Flag().task_started.format(entry['source'] + ' - ' + entry['target']))
            source = self._absolute_path('in', entry['source'])
            target = self._absolute_path('in', entry['target'])
            save_to = self._absolute_path('out', entry['source'] + '+' + entry['target'])
            clip = False if entry.get('clip') is None else entry['clip']
            preserve_paper = False if entry.get('preserve_paper') is None else entry['preserve_paper']

            try:
                color_transfer.run(
                    source=source,
                    target=target,
                    clip=clip,
                    preserve_paper=preserve_paper,
                    save_to=save_to 
                )
            except Exception as e:
                raise exceptions_.Error(err=e, key='CantTransferColor')

            print(Flag().task_ended)

        try: 
            self._rename_input_files()
        except Exception as e:
            raise exceptions_.Error(err=e, key='CantRenameInputFiles')

        try:
            Consensus().run(
                target=self._paths('out'),
                save_to=self._absolute_path('datadir', self._CONSENSUS)
            )
        except Exception as e:
            raise exceptions_.Fatal(err=e, key='CantCreateConsensusFile')

        print(Flag().execution_ended)


if __name__ == '__main__':
    App().main()