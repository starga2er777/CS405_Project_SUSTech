
import time
import os.path
import argparse
import numpy as np
import matplotlib.pyplot as plt
from model_unet import *
from PIL import Image
import torchvision
from torchvision.transforms import InterpolationMode

mappingrgb = {
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



# our CLI parser
parser = argparse.ArgumentParser()
parser.add_argument("--datadir", type=str, default="../datasets/testimgs/", help="directory of images")
parser.add_argument("--batch_size", type=int, default=1, help="batch size")
parser.add_argument("--num_gpu", type=int, default=1, help="number of gpus")
parser.add_argument("--losstype", type=str, default="segment", help="choose between segment & reconstruction")
args = parser.parse_args()


# our transform that is applied to all incoming images
transform_image = torchvision.transforms.Compose([
    torchvision.transforms.Resize(size=(128, 256), interpolation=InterpolationMode.BILINEAR),
    torchvision.transforms.ToTensor()
])


# load the images in the folder
img_data = torchvision.datasets.ImageFolder(root=args.datadir, transform=transform_image)
img_batch = torch.utils.data.DataLoader(img_data, batch_size=args.batch_size, shuffle=False, num_workers=4)
print(img_data)


# load pretrained model if it is there
print("loading unet model...")
file_model = './unet.pkl'
if os.path.isfile(file_model):
    generator = torch.load(file_model)
    print("    - model restored from file....")
    print("    - filename = %s" % file_model)
else:
    print("unable to load unet.pkl model file")
    exit()


# make the result directory
if not os.path.exists('./predict/'):
    os.makedirs('./predict/')


# Loop through the dataset and evaluate how well the network predicts
print("\nevaluating network (will take a while)...")
for idx_batch, (imagergb, labelrgb) in enumerate(img_batch):

    # send to the GPU and do a forward pass
    x = Variable(imagergb).cuda(0)
    y = generator.forward(x)

    # enforce that we are only doing segmentation network type
    if args.losstype != "segment":
        print("this test script only works for \"segment\" unet classification...")
        exit()

    # max over the classes should be the prediction
    # our prediction is [N, classes, W, H]
    # so we max over the second dimension and take the max response
    pred_class = torch.zeros((y.size()[0], y.size()[2], y.size()[3]))
    for idx in range(0, y.size()[0]):
        pred_class[idx] = torch.argmax(y[idx], dim=0).cpu().int()

    colored_image = np.zeros((y.shape[2], y.shape[3], 3), dtype=np.uint8)

    for i in range(0, pred_class.shape[1]):
        for j in range(0, pred_class.shape[2]):
            colored_image[i][j] = (mappingrgb[int(pred_class[0][i][j])])

    colored_image_pil = Image.fromarray(colored_image)

    # colored_image_pil = Image.fromarray(colored_image)

    # unsqueese so we have [N, 1, W, H] size
    # this allows for debug saving of the images to file...
    # pred_class = pred_class.unsqueeze(1).float()

    # debug saving generated classes to file

    colored_image_pil.save("./predict/result_image_{}.png".format(idx_batch))
    v_utils.save_image(x.cpu().data, "./predict/original_image_{}.png".format(idx_batch))
