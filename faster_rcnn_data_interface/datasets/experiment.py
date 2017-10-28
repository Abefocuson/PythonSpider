import os.path
_data_path='./data/ILSVRC2017_DET/ILSVRC'
_image_set='train'
if _image_set.find('train') >= 0 or _image_set.find('test') >= 0 or _image_set.find('val') >= 0:
    image_set_file = os.path.join(_data_path, 'ImageSets', 'DET',
                                  _image_set + '.txt')
    assert os.path.exists(image_set_file), \
        'Path does not exist: {}'.format(image_set_file)
    image_index = []
    with open(image_set_file) as f:
        for x in f.readlines():
            image_index.append(x[0:x.find(' ')])


else:
    assert False, 'Cannot identify image set type'
print(image_index)