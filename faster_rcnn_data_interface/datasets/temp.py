from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from datasets.imdb import imdb
import datasets.ds_utils as ds_utils
import xml.etree.ElementTree as ET
import numpy as np
import scipy.sparse
import scipy.io as sio
import utils.cython_bbox
import pickle
import subprocess
import uuid
#from .voc_eval import voc_eval
from model.config import cfg

#get names of classes
# INPUT_DATA1 = '../../../../data/ILSVRC2017/ILSVRC2017_DET/ILSVRC/Annotations/DET/train/ILSVRC2013_train'
# assert os.path.exists('../../../../data/ILSVRC2017/ILSVRC2017_DET/ILSVRC/Annotations/DET/train/ILSVRC2013_train'), \
#     'class path does not exist: {}'.format(self._devkit_path)
# dirt = [x[0] for x in os.walk(INPUT_DATA1)]
# for i in range(1,len(dirt)):
#    dirt[i] = dirt[i][-9:]
# dirt[0] = '__background__'
# dirt=tuple(dirt)

class ilsvrc(imdb):
    def __init__(self, image_set, year, devkit_path='./data/2017'):
        imdb.__init__(self, 'ilsvrc_'+year+'_'+image_set)
        self._year = year
        self._image_set = image_set
        self._devkit_path = devkit_path
        self._data_path = os.path.join(self._devkit_path, 'ILSVRC')
        #self._classes = self.get_classes(self._devkit_path)  # always index 0
        self._classes = ('__background__', 'n01530575', 'n02086646', 'n04606251', 'n02093991', 'n07747607', 'n02095314',
                         'n02504458', 'n02071294', 'n02121808', 'n04273569', 'n02017213', 'n02100583', 'n03908714',
                         'n03179701', 'n02356798', 'n04039381', 'n04118538', 'n01806567', 'n02086079', 'n03676483',
                         'n04392985', 'n02108000', 'n04442312', 'n03495258', 'n01537544', 'n01847000', 'n03594945',
                         'n02444819', 'n07768694', 'n02769748', 'n03891251', 'n02510455', 'n02037110', 'n04252225',
                         'n01742172', 'n01795545', 'n04081281', 'n07749582', 'n03777568', 'n02018207', 'n03775546',
                         'n04065464', 'n01692333', 'n02007558', 'n02219486', 'n02099429', 'n02132136', 'n01776313',
                         'n01443537', 'n03255030', 'n07714571', 'n03770679', 'n02951585', 'n02011460', 'n04228054',
                         'n02814533', 'n01770393', 'n01558993', 'n02281406', 'n01753488', 'n03476991', 'n02112137',
                         'n03498962', 'n02027492', 'n01592084', 'n03201208', 'n03095699', 'n03314780', 'n02105162',
                         'n02840245', 'n02106030', 'n02492035', 'n04357314', 'n01644373', 'n02821627', 'n03372029',
                         'n04254680', 'n02992211', 'n07697537', 'n00141669', 'n02088466', 'n03085013', 'n02105641',
                         'n10565667', 'n03125729', 'n01726692', 'n02111889', 'n07693725', 'n03991062', 'n01729322',
                         'n01843383', 'n02490219', 'n02804414', 'n02879718', 'n01675722', 'n02437136', 'n02102177',
                         'n02107312', 'n01944390', 'n02484975', 'n02119022', 'n03376595', 'n03673027', 'n02089078',
                         'n03494278', 'n02787622', 'n07718472', 'n04557648', 'n02090721', 'n03599486', 'n02279972',
                         'n02799071', 'n02802426', 'n03337140', 'n04141076', 'n03513137', 'n02422699', 'n02951358',
                         'n06874185', 'n03947888', 'n02013706', 'n02096051', 'n02493793', 'n03792782', 'n02134418',
                         'n02086240', 'n03297495', 'n01756291', 'n01641577', 'n03832673', 'n04509417', 'n04019541',
                         'n02077923', 'n02097474', 'n04330267', 'n02489166', 'n03982430', 'n02102318', 'n02101006',
                         'n01735189', 'n08256735', 'n03804744', 'n02112350', 'n02085936', 'n02105251', 'n01828970',
                         'n02107683', 'n01582220', 'n02109961', 'n02113712', 'n02281787', 'n03769881', 'n03770439',
                         'n03868242', 'n02093754', 'n02066245', 'n02002556', 'n04263257', 'n03038685', 'n03272010',
                         'n02018795', 'n02134084', 'n02437312', 'n03271574', 'n02100877', 'n01495701', 'n04336792',
                         'n03690938', 'n01798484', 'n04376876', 'n02133161', 'n03961711', 'n07718747', 'n02096294',
                         'n01534433', 'n03908618', 'n02454379', 'n02120505', 'n03814639', 'n02113978', 'n02487347',
                         'n03950228', 'n03445777', 'n03416640', 'n02088632', 'n02326432', 'n02110063', 'n01667778',
                         'n07720875', 'n02777292', 'n02101556', 'n02076196', 'n02764044', 'n02328150', 'n01728920',
                         'n02009912', 'n02098105', 'n02766320', 'n02033041', 'n03134739', 'n02062744', 'n02099712',
                         'n04536866', 'n00477639', 'n02094114', 'n02107908', 'n03958227', 'n03942813', 'n02096437',
                         'n03001627', 'n01784675', 'n07615774', 'n02129165', 'n02693246', 'n02099601', 'n02093859',
                         'n02111500', 'n02099849', 'n07880968', 'n04591713', 'n01734418', 'n02124075', 'n03995372',
                         'n02791124', 'n02102040', 'n02839592', 'n02325366', 'n02099267', 'n02112706', 'n02094258',
                         'n03379051', 'n02892767', 'n03670208', 'n01664065', 'n02280649', 'n01797886', 'n04335209',
                         'n03400231', 'n02835271', 'n02123597', 'n02981792', 'n02097209', 'n03529860', 'n04371430',
                         'n02092339', 'n02088238', 'n02129604', 'n02924116', 'n07742313', 'n02486410', 'n02096177',
                         'n04409515', 'n01695060', 'n06892775', 'n03062245', 'n03249569', 'n03481172', 'n01737021',
                         'n02111129', 'n07739125', 'n04356056', 'n02488702', 'n07697313', 'n02009229', 'n04252077',
                         'n02165456', 'n04591157', 'n02277742', 'n02086910', 'n02028035', 'n02692232', 'n02503517',
                         'n01674464', 'n02097047', 'n02110627', 'n02411705', 'n02091134', 'n01532829', 'n01796340',
                         'n09835506', 'n02493509', 'n04379243', 'n02834778', 'n02113186', 'n03662601', 'n03100240',
                         'n03619890', 'n01614925', 'n03000684', 'n02118333', 'n03538406', 'n04483307', 'n03063599',
                         'n02002724', 'n02108915', 'n01518878', 'n04554684', 'n02102973', 'n01531178', 'n02415577',
                         'n07734744', 'n02091831', 'n02087046', 'n02492660', 'n02690373', 'n02828884', 'n04487081',
                         'n03120778', 'n03141823', 'n03745146', 'n01498041', 'n02445715', 'n02095889', 'n02389026',
                         'n01560419', 'n03791053', 'n01740131', 'n07745940', 'n04317175', 'n04099969', 'n02113799',
                         'n04347754', 'n02110185', 'n03838899', 'n02087394', 'n02119789', 'n02276258', 'n04515003',
                         'n02096585', 'n01616318', 'n03017168', 'n03642806', 'n02324045', 'n04311174', 'n01855672',
                         'n02091467', 'n02423022', 'n04259630', 'n04542943', 'n02105056', 'n04152593', 'n03124170',
                         'n03483316', 'n01860187', 'n01984695', 'n07583066', 'n02089973', 'n02104029', 'n01910747',
                         'n03110669', 'n02342885', 'n02422106', 'n03445924', 'n02094433', 'n02880940', 'n03467517',
                         'n04256520', 'n04540053', 'n02108551', 'n02091032', 'n02970849', 'n02870880', 'n02317335',
                         'n04209133', 'n08539072', 'n04468005', 'n04147183', 'n04154565', 'n02687172', 'n03764736',
                         'n02105855', 'n03207941', 'n02108422', 'n02206856', 'n04004767', 'n02486261', 'n03785016',
                         'n01739381', 'n04116512', 'n08518171', 'n02488291', 'n01983481', 'n04146614', 'n02979186',
                         'n03128519', 'n03131574', 'n02701002', 'n01669191', 'n02095570', 'n01689811', 'n03759954',
                         'n02109047', 'n02113624', 'n02106382', 'n02509815', 'n02494079', 'n02051845', 'n03452741',
                         'n02097130', 'n02268443', 'n02108089', 'n02355227', 'n02091244', 'n02100236', 'n01990800',
                         'n02815834', 'n02097298', 'n01665541', 'n02412080', 'n02101388', 'n04023962', 'n08517676',
                         'n03761084', 'n02088094', 'n01751748', 'n04037443', 'n02098413', 'n01819313', 'n02958343',
                         'n02110806', 'n01806143', 'n01580077', 'n02123045', 'n01729977', 'n01688243', 'n01694178',
                         'n01601694', 'n03793489', 'n01820546', 'n02104365', 'n02402425', 'n01687978', 'n02025239',
                         'n03109150', 'n02106550', 'n02089867', 'n02107142', 'n04131690', 'n04429376', 'n04270147',
                         'n04380533', 'n02109525', 'n03535780', 'n02691156', 'n03790512', 'n02395003', 'n10148035',
                         'n02374451', 'n01685808', 'n01496331', 'n02484322', 'n01677366', 'n01514859', 'n01728572',
                         'n03188531', 'n03633091', 'n04530566', 'n02093647', 'n02091635', 'n04332243', 'n02090622',
                         'n02111277', 'n02106662', 'n02113023', 'n04026417', 'n02930766', 'n01622779', 'n02085782',
                         'n02105412', 'n02917067', 'n03636649', 'n02672831', 'n02123394', 'n03211117', 'n02058221',
                         'n01744401', 'n02012849', 'n02084071', 'n01749939', 'n02006656', 'n07753275', 'n02098286',
                         'n02398521', 'n02396427', 'n02100735', 'n01662784', 'n02106166', 'n01882714', 'n07697100',
                         'n03841666', 'n02112018', 'n03344393', 'n02102480', 'n01693334', 'n03127747', 'n03797390',
                         'n07753113', 'n03928116', 'n04118776', 'n04487394', 'n02056570', 'n04074963', 'n07695742',
                         'n01807496', 'n01824575', 'n02807133', 'n04517823', 'n01818515', 'n02504013', 'n03196217',
                         'n02110341', 'n02107574', 'n02105505', 'n03394916', 'n04344873', 'n02274259', 'n01608432',
                         'n01503061', 'n01682714', 'n01755581', 'n04285008', 'n02883205', 'n02687992', 'n07873807',
                         'n02346627', 'n01514668', 'n03782006', 'n02395406', 'n04070727', 'n03447447', 'n02419796',
                         'n01843065', 'n02110958', 'n02088364', 'n03584254', 'n02786058', 'n07753592', 'n02403003',
                         'n04612504', 'n03063338', 'n02093428', 'n03581125', 'n02120079', 'n01748264', 'n01639765',
                         'n01667114', 'n07930864', 'n01833805', 'n02131653', 'n02085620', 'n03710721', 'n00007846',
                         'n01829413', 'n01855032', 'n02090379', 'n03120491', 'n02397096', 'n02676566', 'n03916031',
                         'n04254120', 'n01982650', 'n03720891', 'n02092002', 'n02093256', 'n02391049', 'n04334599',
                         'n01644900', 'n02097658', 'n01817953')

        self._class_to_ind = dict(list(zip(self.classes, list(range(self.num_classes)))))
        self._image_ext = '.JPEG'
        self._image_index = self._load_image_set_index()
        # Default to roidb handler
        self._roidb_handler = self.gt_roidb
        self._salt = str(uuid.uuid4())
        self._comp_id = 'comp4'

        # PASCAL specific config options
        self.config = {'cleanup': True,
                       'use_salt': True,
                       'use_diff': False,
                       'matlab_eval': False,
                       'rpn_file': None}

        assert os.path.exists(self._devkit_path), \
          'VOCdevkit path does not exist: {}'.format(self._devkit_path)
        assert os.path.exists(self._data_path), \
          'Path does not exist: {}'.format(self._data_path)
    # def get_classes(self, devkit_path):
    #     INPUT_DATA1 = os.path.join(devkit_path,"..",'ILSVRC2017','ILSVRC2017_DET','ILSVRC',
    #                                'Annotations/DET/train/ILSVRC2013_train')
    #     assert os.path.exists(INPUT_DATA1), \
    #         'class path does not exist: {}'.format(self._devkit_path)
    #     dirt = [x[0] for x in os.walk(INPUT_DATA1)]
    #     for i in range(1, len(dirt)):
    #         dirt[i] = dirt[i][-9:]
    #     dirt[0] = '__background__'
    #     dirt = tuple(dirt)
    #     return dirt
    def image_path_at(self, i):
        """
        Return the absolute path to image i in the image sequence.
        """
        return self.image_path_from_index(self._image_index[i])

    def image_path_from_index(self, index):
        """
        Construct an image path from the image's "index" identifier.
        """
        if index.index('train')>=0:
            image_path = os.path.join(self._data_path, 'Data','VID','train',
                                      index[0:51],index[51:57] + self._image_ext)
            assert os.path.exists(image_path), \
                'Path does not exist: {}'.format(image_path)
            return image_path
        elif index.index('test')>=0:
            image_path = os.path.join(self._data_path, 'Data','VID','test',
                                      index + self._image_ext)
            assert os.path.exists(image_path), \
                'Path does not exist: {}'.format(image_path)
            return image_path
        elif index.index('val')>=0:
            image_path = os.path.join(self._data_path, 'Data','VID','val',
                                      index + self._image_ext)
            assert os.path.exists(image_path), \
                'Path does not exist: {}'.format(image_path)
            return image_path
        else:
            assert False, 'Illegal index identified'

    def _load_image_set_index(self):
        """
        Load the indexes listed in this dataset's image set file.
        """
        # Example path to image set file:
        # self._devkit_path + /VOCdevkit2007/VOC2007/ImageSets/Main/val.txt
        if self._image_set.index('train')>=0:
            image_set_file = os.path.join(self._data_path, 'ImageSets', 'VID',
                                          self._image_set + '.txt')
            assert os.path.exists(image_set_file), \
                'Path does not exist: {}'.format(image_set_file)
            image_index=[]
            with open(image_set_file) as f:
                for x in f.readlines():
                    INPUT_DATA2 = os.path.join(self._data_path,'Data','VID','train', x[0:51])
                    dirt = [y[2] for y in os.walk(INPUT_DATA2)]
                    dirt = dirt[0]
                    for i in range(1, len(dirt)):
                        image_index.append(x[0:51] + dirt[i][0:6])
            return image_index
        elif self._image_set.index('test')>=0:
            image_set_file = os.path.join(self._data_path, 'ImageSets', 'VID',
                                          self._image_set + '.txt')
            assert os.path.exists(image_set_file), \
                'Path does not exist: {}'.format(image_set_file)
            with open(image_set_file) as f:
                image_index = [x.strip()[0:31] for x in f.readlines()]
            return image_index
        elif self._image_set.index('val')>=0:
            image_set_file = os.path.join(self._data_path, 'ImageSets', 'VID',
                                          self._image_set + '.txt')
            assert os.path.exists(image_set_file), \
                'Path does not exist: {}'.format(image_set_file)
            with open(image_set_file) as f:
                image_index = [x.strip()[0:30] for x in f.readlines()]
            return image_index
        else:
            assert False,'Cannot identify image set type'


    def gt_roidb(self):
        """
        Return the database of ground-truth regions of interest.

        This function loads/saves from/to a cache file to speed up future calls.
        """
        cache_file = os.path.join(self.cache_path, self.name + '_gt_roidb.pkl')
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as fid:
                try:
                    roidb = pickle.load(fid)
                except:
                    roidb = pickle.load(fid, encoding='bytes')
            print('{} gt roidb loaded from {}'.format(self.name, cache_file))
            return roidb

        gt_roidb = [self._load_ilsvrc_annotation(index)
                    for index in self.image_index]
        with open(cache_file, 'wb') as fid:
            pickle.dump(gt_roidb, fid, pickle.HIGHEST_PROTOCOL)
        print('wrote gt roidb to {}'.format(cache_file))

        return gt_roidb

    def rpn_roidb(self):
        if int(self._year) == 2007 or self._image_set.index('test')<0:
            gt_roidb = self.gt_roidb()
            rpn_roidb = self._load_rpn_roidb(gt_roidb)
            roidb = imdb.merge_roidbs(gt_roidb, rpn_roidb)
        else:
            roidb = self._load_rpn_roidb(None)
        return roidb

    def _load_rpn_roidb(self, gt_roidb):
        filename = self.config['rpn_file']
        print('loading {}'.format(filename))
        assert os.path.exists(filename), \
            'rpn data not found at: {}'.format(filename)
        with open(filename, 'rb') as f:
            box_list = pickle.load(f)
        return self.create_roidb_from_box_list(box_list, gt_roidb)

    def _load_ilsvrc_annotation(self, index):
        """
        Load image and bounding boxes info from XML file in the PASCAL VOC
        format.
        """
        if index.index('train')>=0:
            filename = os.path.join(self._data_path, 'Annotations','VID', 'train',index[0:51], index[51:57]+'.xml')
            tree = ET.parse(filename)
            objs = tree.findall('object')
            num_objs = len(objs)
            boxes = np.zeros((num_objs, 4), dtype=np.uint16)
            gt_classes = np.zeros((num_objs), dtype=np.int32)
            overlaps = np.zeros((num_objs, self.num_classes), dtype=np.float32)
            # "Seg" area for pascal is just the box area
            seg_areas = np.zeros((num_objs), dtype=np.float32)

            # Load object bounding boxes into a data frame.
            for ix, obj in enumerate(objs):
                bbox = obj.find('bndbox')
                # Make pixel indexes 0-based
                x1 = float(bbox.find('xmin').text) - 1
                y1 = float(bbox.find('ymin').text) - 1
                x2 = float(bbox.find('xmax').text) - 1
                y2 = float(bbox.find('ymax').text) - 1
                cls = self._class_to_ind[obj.find('name').text.lower().strip()]
                boxes[ix, :] = [x1, y1, x2, y2]
                gt_classes[ix] = cls
                overlaps[ix, cls] = 1.0
                seg_areas[ix] = (x2 - x1 + 1) * (y2 - y1 + 1)

            overlaps = scipy.sparse.csr_matrix(overlaps)

            return {'boxes': boxes,
                    'gt_classes': gt_classes,
                    'gt_overlaps': overlaps,
                    'flipped': False,
                    'seg_areas': seg_areas}



    def _get_comp_id(self):
        comp_id = (self._comp_id + '_' + self._salt if self.config['use_salt']
                   else self._comp_id)
        return comp_id

    def _get_ilsvrc_results_file_template(self):
        # VOCdevkit/results/VOC2007/Main/<comp_id>_det_test_aeroplane.txt
        filename = self._get_comp_id() + '_det_' + self._image_set + '_{:s}.txt'
        path = os.path.join(
            self._devkit_path,
            'results',
            'ILSVRC2017',
            'Main',
            filename)
        return path

    def _write_ilsvrc_results_file(self, all_boxes):
        for cls_ind, cls in enumerate(self.classes):
            if cls == '__background__':
                continue
            print('Writing {} ILSVRC results file'.format(cls))
            filename = self._get_ilsvrc_results_file_template().format(cls)
            with open(filename, 'wt') as f:
                for im_ind, index in enumerate(self.image_index):
                    dets = all_boxes[cls_ind][im_ind]
                    if dets == []:
                        continue
                    # the VOCdevkit expects 1-based indices
                    for k in range(dets.shape[0]):
                        f.write('{:s} {:.3f} {:.1f} {:.1f} {:.1f} {:.1f}\n'.
                                format(index, dets[k, -1],
                                       dets[k, 0] + 1, dets[k, 1] + 1,
                                       dets[k, 2] + 1, dets[k, 3] + 1))

    def _do_python_eval(self, output_dir='output'):
        annopath = os.path.join(
            self._devkit_path,
            'ILSVRC',
            'Annotations',
            'VID'
            '{:s}.xml')
        imagesetfile = os.path.join(
            self._devkit_path,
            'VOC' + self._year,
            'ImageSets',
            'Main',
            self._image_set + '.txt')
        cachedir = os.path.join(self._devkit_path, 'annotations_cache')
        aps = []
        # The PASCAL VOC metric changed in 2010
        use_07_metric = True if int(self._year) < 2010 else False
        print('VOC07 metric? ' + ('Yes' if use_07_metric else 'No'))
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        for i, cls in enumerate(self._classes):
            if cls == '__background__':
                continue
            filename = self._get_ilsvrc_results_file_template().format(cls)
            rec, prec, ap = voc_eval(
                filename, annopath, imagesetfile, cls, cachedir, ovthresh=0.5,
                use_07_metric=use_07_metric)
            aps += [ap]
            print(('AP for {} = {:.4f}'.format(cls, ap)))
            with open(os.path.join(output_dir, cls + '_pr.pkl'), 'wb') as f:
                pickle.dump({'rec': rec, 'prec': prec, 'ap': ap}, f)
        print(('Mean AP = {:.4f}'.format(np.mean(aps))))
        print('~~~~~~~~')
        print('Results:')
        for ap in aps:
            print(('{:.3f}'.format(ap)))
        print(('{:.3f}'.format(np.mean(aps))))
        print('~~~~~~~~')
        print('')
        print('--------------------------------------------------------------')
        print('Results computed with the **unofficial** Python eval code.')
        print('Results should be very close to the official MATLAB eval code.')
        print('Recompute with `./tools/reval.py --matlab ...` for your paper.')
        print('-- Thanks, The Management')
        print('--------------------------------------------------------------')

    def _do_matlab_eval(self, output_dir='output'):
        print('-----------------------------------------------------')
        print('Computing results with the official MATLAB eval code.')
        print('-----------------------------------------------------')
        path = os.path.join(cfg.ROOT_DIR, 'lib', 'datasets',
                            'VOCdevkit-matlab-wrapper')
        cmd = 'cd {} && '.format(path)
        cmd += '{:s} -nodisplay -nodesktop '.format(cfg.MATLAB)
        cmd += '-r "dbstop if error; '
        cmd += 'voc_eval(\'{:s}\',\'{:s}\',\'{:s}\',\'{:s}\'); quit;"' \
            .format(self._devkit_path, self._get_comp_id(),
                    self._image_set, output_dir)
        print(('Running:\n{}'.format(cmd)))
        status = subprocess.call(cmd, shell=True)

    def evaluate_detections(self, all_boxes, output_dir):
        self._write_ilsvrc_results_file(all_boxes)
        self._do_python_eval(output_dir)
        if self.config['matlab_eval']:
            self._do_matlab_eval(output_dir)
        if self.config['cleanup']:
            for cls in self._classes:
                if cls == '__background__':
                    continue
                filename = self._get_ilsvrc_results_file_template().format(cls)
                os.remove(filename)

    def competition_mode(self, on):
        if on:
            self.config['use_salt'] = False
            self.config['cleanup'] = False
        else:
            self.config['use_salt'] = True
            self.config['cleanup'] = True

    if __name__ == '__main__':
        from datasets.ILSVRC2017_DET import ilsvrc2017
        d = ilsvrc2017('train_1', '2017')
        res = d.roidb
        from IPython import embed;

        embed()