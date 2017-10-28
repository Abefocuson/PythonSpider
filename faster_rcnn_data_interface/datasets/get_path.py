import os.path
INPUT_DATA = '../../../../data/ILSVRC2017/ILSVRC2017_DET/ILSVRC/Annotations/DET/train/ILSVRC2013_train'
#get names of classes
INPUT_DATA1 = '../../../../data/ILSVRC2017/ILSVRC2017_DET/ILSVRC/Annotations/DET/train/ILSVRC2013_train'
dir = [x[0] for x in os.walk(INPUT_DATA1)]
for i in range(1,len(dir)):
   dir[i] = dir[i][-9:]
dir[0] = '__background__'
dir=tuple(dir)
print (dir)
class_to_ind = dict(list(zip(dir, list(range(len(dir))))))
print (class_to_ind)