import os
import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torchvision.transforms.functional as TF
from collections import namedtuple
from torchvision.transforms import InterpolationMode


class CityscapesDataset(Dataset):

    def __init__(self, root, split='train', mode='fine', augment=False):

        self.root = os.path.expanduser(root)
        self.mode = 'gtFine' if mode == 'fine' else 'gtCoarse'
        self.images_dir = os.path.join(self.root, 'leftImg8bit', split)
        self.targets_dir = os.path.join(self.root, self.mode, split)
        self.split = split
        self.augment = augment
        self.images = []
        self.targets = []
        self.mapping = {
            0: 0,    # unlabeled
            1: 1,    # ego vehicle
            2: 2,    # rect border
            3: 3,    # out of roi
            4: 4,    # static
            5: 5,    # dynamic
            6: 6,    # ground
            7: 7,    # road
            8: 8,    # sidewalk
            9: 9,    # parking
            10: 10,  # rail track
            11: 11,  # building
            12: 12,  # wall
            13: 13,  # fence
            14: 14,  # guard rail
            15: 15,  # bridge
            16: 16,  # tunnel
            17: 17,  # pole
            18: 18,  # polegroup
            19: 19,  # traffic light
            20: 20,  # traffic sign
            21: 21,  # vegetation
            22: 22,  # terrain
            23: 23,  # sky
            24: 24,  # person
            25: 25,  # rider
            26: 26,  # car
            27: 27,  # truck
            28: 28,  # bus
            29: 29,  # caravan
            30: 30,  # trailer
            31: 31,  # train
            32: 32,  # motorcycle
            33: 33,  # bicycle
            -1: -1   # licenseplate
        }
        self.mappingrgb = {
            0: (0, 0, 0),      # unlabeled
            1: (0, 0, 0),      # ego vehicle
            2: (0, 0, 0),      # rectification border
            3: (0, 0, 0),      # out of roi
            4: (0, 0, 0),      # static
            5: (111, 74, 0),   # dynamic
            6: (81, 0, 81),    # ground
            7: (128, 64, 128), # road
            8: (244, 35, 232), # sidewalk
            9: (250, 170, 160),# parking
            10: (230, 150, 140),# rail track
            11: (70, 70, 70),  # building
            12: (102, 102, 156),# wall
            13: (190, 153, 153),# fence
            14: (180, 165, 180),# guard rail
            15: (150, 100, 100),# bridge
            16: (150, 120, 90), # tunnel
            17: (153, 153, 153),# pole
            18: (153, 153, 153),# polegroup
            19: (250, 170, 30), # traffic light
            20: (220, 220, 0),  # traffic sign
            21: (107, 142, 35), # vegetation
            22: (152, 251, 152),# terrain
            23: (70, 130, 180), # sky
            24: (220, 20, 60),  # person
            25: (255, 0, 0),    # rider
            26: (0, 0, 142),    # car
            27: (0, 0, 70),     # truck
            28: (0, 60, 100),   # bus
            29: (0, 0, 90),     # caravan
            30: (0, 0, 110),    # trailer
            31: (0, 80, 100),   # train
            32: (0, 0, 230),    # motorcycle
            33: (119, 11, 32),  # bicycle
            -1: (0, 0, 142)    # license plate
        }

        # Ensure that this matches the above mapping
        # For example 4 classes, means we should map to the ids=(0,1,2,3)
        # This is used to specify how many outputs the network should product...
        self.num_classes = 35

        # =============================================
        # Check that inputs are valid
        # =============================================
        if mode not in ['fine', 'coarse']:
            raise ValueError('Invalid mode! Please use mode="fine" or mode="coarse"')
        if mode == 'fine' and split not in ['train', 'test', 'val']:
            raise ValueError('Invalid split for mode "fine"! Please use split="train", split="test" or split="val"')
        elif mode == 'coarse' and split not in ['train', 'train_extra', 'val']:
            raise ValueError('Invalid split for mode "coarse"! Please use split="train", split="train_extra" or split="val"')
        if not os.path.isdir(self.images_dir) or not os.path.isdir(self.targets_dir):
            raise RuntimeError('Dataset not found or incomplete. Please make sure all required folders for the'
                               ' specified "split" and "mode" are inside the "root" directory')

        # =============================================
        # Read in the paths to all images
        # =============================================
        for city in os.listdir(self.images_dir):
            img_dir = os.path.join(self.images_dir, city)
            target_dir = os.path.join(self.targets_dir, city)
            for file_name in os.listdir(img_dir):
                self.images.append(os.path.join(img_dir, file_name))
                target_name = '{}_{}'.format(file_name.split('_leftImg8bit')[0], '{}_labelIds.png'.format(self.mode))
                # target_name = '{}_{}'.format(file_name.split('_leftImg8bit')[0], '{}_color.png'.format(self.mode))
                self.targets.append(os.path.join(target_dir, target_name))

    def __repr__(self):
        fmt_str = 'Dataset ' + self.__class__.__name__ + '\n'
        fmt_str += '    Number of images: {}\n'.format(self.__len__())
        fmt_str += '    Split: {}\n'.format(self.split)
        fmt_str += '    Mode: {}\n'.format(self.mode)
        fmt_str += '    Augment: {}\n'.format(self.augment)
        fmt_str += '    Root Location: {}\n'.format(self.root)
        return fmt_str

    def __len__(self):
        return len(self.images)

    def mask_to_class(self, mask):
        '''
        Given the cityscapes dataset, this maps to a 0..classes numbers.
        This is because we are using a subset of all masks, so we have this "mapping" function.
        This mapping function is used to map all the standard ids into the smaller subset.
        '''
        maskimg = torch.zeros((mask.size()[0], mask.size()[1]), dtype=torch.uint8)
        for k in self.mapping:
            maskimg[mask == k] = self.mapping[k]
        return maskimg

    def mask_to_rgb(self, mask):
        '''
        Given the Cityscapes mask file, this converts the ids into rgb colors.
        This is needed as we are interested in a sub-set of labels, thus can't just use the
        standard color output provided by the dataset.
        '''
        rgbimg = torch.zeros((3, mask.size()[0], mask.size()[1]), dtype=torch.uint8)
        for k in self.mappingrgb:
            rgbimg[0][mask == k] = self.mappingrgb[k][0]
            rgbimg[1][mask == k] = self.mappingrgb[k][1]
            rgbimg[2][mask == k] = self.mappingrgb[k][2]
        return rgbimg

    def class_to_rgb(self, mask):
        '''
        This function maps the classification index ids into the rgb.
        For example after the argmax from the network, you want to find what class
        a given pixel belongs too. This does that but just changes the color
        so that we can compare it directly to the rgb groundtruth label.
        '''
        mask2class = dict((v, k) for k, v in self.mapping.items())
        rgbimg = torch.zeros((3, mask.size()[0], mask.size()[1]), dtype=torch.uint8)
        for k in mask2class:
            rgbimg[0][mask == k] = self.mappingrgb[mask2class[k]][0]
            rgbimg[1][mask == k] = self.mappingrgb[mask2class[k]][1]
            rgbimg[2][mask == k] = self.mappingrgb[mask2class[k]][2]
        return rgbimg

    def __getitem__(self, index):

        # first load the RGB image
        image = Image.open(self.images[index]).convert('RGB')

        # next load the target
        target = Image.open(self.targets[index]).convert('L')

        # If augmenting, apply random transforms
        # Else we should just resize the image down to the correct size
        if self.augment:
            # Resize
            image = TF.resize(image, size=(128+10, 256+10), interpolation=InterpolationMode.BILINEAR)
            target = TF.resize(target, size=(128+10, 256+10), interpolation=InterpolationMode.NEAREST)
            # Random crop
            i, j, h, w = transforms.RandomCrop.get_params(image, output_size=(128, 256))
            image = TF.crop(image, i, j, h, w)
            target = TF.crop(target, i, j, h, w)
            # Random horizontal flipping
            if random.random() > 0.5:
                image = TF.hflip(image)
                target = TF.hflip(target)
            # Random vertical flipping
            # (I found this caused issues with the sky=road during prediction)
            # if random.random() > 0.5:
            #    image = TF.vflip(image)
            #    target = TF.vflip(target)
        else:
            # Resize
            image = TF.resize(image, size=(128, 256), interpolation=InterpolationMode.BILINEAR)
            target = TF.resize(target, size=(128, 256), interpolation=InterpolationMode.NEAREST)

        # convert to pytorch tensors
        # target = TF.to_tensor(target)
        target = torch.from_numpy(np.array(target, dtype=np.uint8))
        image = TF.to_tensor(image)

        # convert the labels into a mask
        targetrgb = self.mask_to_rgb(target)
        targetmask = self.mask_to_class(target)
        targetmask = targetmask.long()
        targetrgb = targetrgb.long()

        # finally return the image pair
        return image, targetmask, targetrgb
