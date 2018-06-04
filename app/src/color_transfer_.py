import os

from collections import OrderedDict
import numpy as np
import cv2
from color_transfer import color_transfer


class ColorTransfer:
    '''
    Should np.clip scale L*a*b* values before final conversion to BGR? Approptiate min-max scaling used if False.
    Should color transfer strictly follow methodology layed out in original paper?
    '''

    def __init__(self):
        pass

    def run(self, source, target, clip, preserve_paper, save_to):
        source = cv2.imread(source)
        target = cv2.imread(target)
        transfer = color_transfer(source, target)
        cv2.imwrite(save_to, transfer)