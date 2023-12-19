#!/bin/bash
#SBATCH -o job.%j.out          
#SBATCH --partition=gpulab02
#SBATCH --qos=gpulab02
#SBATCH -J myFirstGPUJob
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=6
#SBATCH --gres=gpu:1
#SBATCH --job-name=Unet

nvidia-smi

python3 script_eval_iou.py --datadir ../datasets/cityscapes --batch_size 1
# python deeplabv2_resnet101_cityscapes/test_cuda.py
