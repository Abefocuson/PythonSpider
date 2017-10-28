# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Factory method for easily getting imdbs by name."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__sets = {}
from datasets.pascal_voc import pascal_voc
from datasets.coco import coco
from datasets.ILSVRC2017_DET import ilsvrc
from datasets.ILSVRC2017_realDET import ilsvrc_det
import numpy as np
#Set up ilsvrc_<year>_<split>
for year in ['2017']:
  for split in ['test', 'val', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']:
    name = '{}'.format(split)
    if split.find('t') >= 0 or split.find('v') >= 0:
      __sets[name] = (lambda split =split, year= year: ilsvrc(split, year))
    else:
      __sets[name] = (lambda split='train_'+split, year=year: ilsvrc(split, year))
# Set up ilsvrc_det <year>_<split>
for year in ['2017']:
  for split in ['test', 'val', 'train']:
    name = 'det_{}'.format(split)
    __sets[name] = (lambda split=split, year=year: ilsvrc_det(split, year))
# Set up voc_<year>_<split> 
for year in ['2007', '2012']:
  for split in ['train', 'val', 'trainval', 'test']:
    name = 'voc_{}_{}'.format(year, split)
    __sets[name] = (lambda split=split, year=year: pascal_voc(split, year))

# Set up coco_2014_<split>
for year in ['2014']:
  for split in ['train', 'val', 'minival', 'valminusminival', 'trainval']:
    name = 'coco_{}_{}'.format(year, split)
    __sets[name] = (lambda split=split, year=year: coco(split, year))

# Set up coco_2015_<split>
for year in ['2015']:
  for split in ['test', 'test-dev']:
    name = 'coco_{}_{}'.format(year, split)
    __sets[name] = (lambda split=split, year=year: coco(split, year))


def get_imdb(name):
  """Get an imdb (image database) by name."""
  if name not in __sets:
    raise KeyError('Unknown dataset: {}'.format(name))
  return __sets[name]()


def list_imdbs():
  """List all registered imdbs."""
  return list(__sets.keys())
