#!/bin/sh

# dataset path and datalist path
dataset_path="datasets/cityscapes"

filelist_path="deeplabv2_resnet101_cityscapes/data/list"

img_path=${filelist_path}/cityscapes_test.txt
gt_path=${filelist_path}/cityscapes_test_gt.txt
find ${dataset_path}/leftImg8bit/test -iname "*.png" > ${img_path}
find ${dataset_path}/gtFine/test -iname "*.png" > ${gt_path}

img_path=${filelist_path}/cityscapes_train.txt
gt_path=${filelist_path}/cityscapes_train_gt.txt
find ${dataset_path}/leftImg8bit/train -iname "*.png" > ${img_path}
find ${dataset_path}/gtFine/train -iname "*.png" > ${gt_path}

img_path=${filelist_path}/cityscapes_val.txt
gt_path=${filelist_path}/cityscapes_val_gt.txt
find ${dataset_path}/leftImg8bit/val -iname "*.png" > ${img_path}
find ${dataset_path}/gtFine/val -iname "*.png" > ${gt_path}

echo "File construction complete"
