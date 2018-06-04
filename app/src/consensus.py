import os
import hashlib

import exceptions_ as exceptions_


class Consensus:

    '''
    this class creates the consensus.iexec file used to verify the PoCo (proof of contribution).
    this file contains hashes of every text file produced as output.
    '''

    def __init__(self):
        pass

    def run(self, target, save_to):
        try:
            file_ = open(save_to, 'w+')
        except Exception as e:
            raise exceptions_.Fatal(e + ' - ' + file_)

        if os.path.isfile(target):
            hash_ = self.md5(target)
            file_.write('{}'.format(hash_))
            file_.close()
            return

        if os.path.isdir(target):
            for filename in os.listdir(target):
                filepath = '{}/{}'.format(target, filename)
                hash_ = self.md5(filepath)
                file_.write('{}\n'.format(hash_))
            file_.close()
            return

    def md5(self, target):
        md5 = hashlib.md5()
        try:
            with open(target, 'rb') as f:
                buffer = f.read()
                md5.update(buffer)
            return md5.hexdigest()
        except Exception as e:
            raise exceptions_.Fatal(e)