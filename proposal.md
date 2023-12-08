<h1 align = "center">2D Semantic Segmentation in Urban Scenes</h1>
<center>11911612 Haoyu Wang</center>  

<center>12012524 Zhangjie Chen</center>

<center>12011923 Xudong Zhang</center>

<center>12011231 Xuyuan Li</center>

*Dec 2023*

## Research Problem
Autonomous driving, also known as self-driving or driverless technology, represents a revolutionary advancement in the automotive industry. It involves vehicles capable of navigating and operating without human intervention. Autonomous vehicles leverage a combination of sensors, cameras, radar and artificial intelligence to perceive their environment and make real-time decisions, enabling them to navigate roads independently. The development of autonomous vehicles is based on key elements, including environmental perception, data processing, path planning, and control systems. These elements work cohesively to ensure a safe and comfortable autonomous driving experience.

Environmental perception is a pivotal function in autonomous driving, focusing on vehicles' ability to interpret and understand its surrounding. However, the uncertainty in environmental states creates challenges for autonomous driving systems. Factors like unpredictable road conditions and dynamic scenarios require advanced perception technologies to adapt and make accurate decisions.

In order to meet the challenges, we apply semantic segmentation for environmental perception. Semantic segmentation is a perception method that categorizes pixels in an image into different semantic classes, such as road, pedestrians, vehicles, and obstacles, enabling the vehicle to understand its environment. The primary purpose of semantic segmentation in autonomous driving is to provide a detailed understanding of the surrounding environment, aiding decision-making processes for self-driving vehicles.

## Research Objectives
Semantic segmentation is a crucial process for the environmental perception of autonomous driving, involving associating each pixel of an image with predefined class.  In this task, we will apply U-net model to complete semantic segmentation.

U-Net is a popular architecture for semantic segmentation. The down/up-sampling technique became an important design idea and later was adopted by AIGC as well. Although initially designed for biomedical applications, its powerful performance goes beyond. U-net can be trained end-to-end from very few images and outperforms the prior best method (a sliding-window convolutional network) on the ISBI challenge for segmentation of neuronal structures[^1]. To effectively leverage label information, we will use the fully-supervised batch contrastive approach, which will pull clusters of points belonging to the same class together in embedding classes while pushing apart clusters of samples from different classes[^2].

Meanwhile, in order to improve the performance under the situation without any human labels, an approach, named Cut-and-LEaRn (CutLER) will be used for training unsupervised object detection and segmentation models. CutLER first generate coarse masks for multiple objects in an image and then learns a detector on theses masks using robust loss function[^3].



## Research Design and Methods



## Initial Results

After data processing, we applied a U-net model to manage the street scene semantic segmentation task. Here we chose 'train' folder of Cityscapes dataset to be the source domain. Meanwhile, 'test' folder of Cityscapes dataset is used as target domain to evaluate the model. Our basic experiment evaluated the model.

We trained our model with the following parameters:

| Parameters         | Explanation                                           | Values  |
| ------------------ | ----------------------------------------------------- | ------- |
| batch size per GPU | Train batch size(Modified according to different GPU) | 4       |
| epochs             | Number of epochs during training                      | 100     |
| lr                 | Learning rate                                         | 0.0002  |
| img_size           | Size of image(resized) in training and evaluating     | 128*256 |

We observed the descending loss by epoch:

[insert picture]

Below is an example of semantic segmentation result:

[insert picture]

We evaluated the model in two ways: one is pixel-level accuracy, and the other is IoU (Intersection over Union) for each class.

**Pixel-Level Accuracy**: *0.8443*

IoU result of different labels:
| ID   | IoU        | Object Type          |
| ---- | ---------- | -------------------- |
| 0    | N/A        | unlabeled            |
| 1    | **0.8170** | **ego vehicle**      |
| 2    | 0.5637     | rectification border |
| 3    | 0.0193     | out of roi           |
| 4    | 0.0851     | static               |
| 5    | 0.0547     | dynamic              |
| 6    | 0.0610     | ground               |
| 7    | **0.8951** | **road**             |
| 8    | 0.5937     | sidewalk             |
| 9    | 0.2419     | parking              |
| 10   | N/A        | rail track           |
| 11   | **0.7786** | **building**         |
| 12   | 0.2226     | wall                 |
| 13   | 0.1992     | fence                |
| 14   | N/A        | guard rail           |
| 15   | 0.2725     | bridge               |
| 16   | 0.0000     | tunnel               |
| 17   | 0.3443     | pole                 |
| 18   | 0.0000     | polegroup            |
| 19   | 0.2746     | traffic light        |
| 20   | 0.3951     | traffic sign         |
| 21   | **0.8210** | **vegetation**       |
| 22   | 0.4440     | terrain              |
| 23   | **0.8090** | **sky**              |
| 24   | **0.4578** | **person**           |
| 25   | 0.0114     | rider                |
| 26   | **0.8112** | **car**              |
| 27   | 0.1822     | truck                |
| 28   | 0.3999     | bus                  |
| 29   | N/A        | caravan              |
| 30   | N/A        | trailer              |
| 31   | 0.0055     | train                |
| 32   | 0.0643     | motorcycle           |
| 33   | 0.4022     | bicycle              |

In summary, our model has a high accuracy, it performs well on several categories which takes up a large proportion of street view images, for example, car, road and sky. However, it shows room for improvement in other categories. 

We identify the cause of poor segmentation performance in certain categories due to small input image size. When the input image size is too small, the model may struggle to capture intricate details, leading to lower IoU scores, especially for objects or structures that require finer spatial resolution. 

Further enhancements in performance could be achieved through applying other model, augmenting training data, and tuning train parameters.



## Staffing Plan

All the staffing information are provided in the following.

- Haoyu Wang：
  - Survey on 2D semantic segmentation
  - Construct cityscapes dataset
  - Train the model
- Zhangjie Chen
  - Train the model
  - Evaluate test performance
  - Try better Performance
- Xudong Zhang
  - Choose model and estimate memory consumption
  - Evaluate test performance
  - Try better Performance
- Xuyuan Li
  - Construct self-sampled SUSTech dataset
  - Data preprocessing
  - Try better Performance

## Timeline

| Week | Task                                                         |
| :--: | :----------------------------------------------------------- |
|  12  | - Survey on 2D semantic segmentation<br />- Starting training U-Net |
|  13  | - Construct cityscapes dataset<br />- Train the initial results of semantic segmentation |
|  14  | - Improve the accuracy of U-Net<br />- Collect SUSTech datasets for U-Net<br />- Clean and label the SUSTech datasets |
|  15  | - Get the results on SUSTech datasets<br />- Analyze the final results<br />- No-predefined label |
|  16  | - Visualize the final results<br />- PPT, Report and Presentation |



### Reference
[^1]: Olaf Ronneberger, Philipp Fisher and M. Kozubek. U-Net: Convolutional Networks for Biomedical Image Segmentation[J]  .arXiv e-prints arXiv:1505.04597,2015.
[^2]: Prannay Khosla, Piotr Teterwak and Chen Wang. Supervised Contrastive Learning[J] .arXiv e-prints arXiv:2004.11362,2021.
[^3]: Xudong Wang, Rohit Girdhar, Stella X. Yu, and Ishan Misra. Cut and Learn for Unsupervised Object Detection and Instance Segmentation[J]. arXiv pre-prints arXiv:2301.11320,2023.
