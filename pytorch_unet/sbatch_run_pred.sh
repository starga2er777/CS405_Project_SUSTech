#!/bin/bash
#SBATCH -o job.%j.out          
#SBATCH --partition=gpulab02
#SBATCH --qos=gpulab02
#SBATCH -J myFirstGPUJob
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=6
#SBATCH --gres=gpu:1
#SBATCH --job-name=test

nvidia-smi

python3 script_predict.py --datadir ../datasets/testimgs/ --num_gpu 1 --losstype segment
# python deeplabv2_resnet101_cityscapes/test_cuda.py
