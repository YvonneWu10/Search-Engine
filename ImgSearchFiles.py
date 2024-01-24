# SJTU EE208

import time

import numpy as np
import torch

import torchvision
import torchvision.transforms as transforms
from torchvision.datasets.folder import default_loader
import numpy as np
import math


start = time.time()

model = torchvision.models.resnet50(pretrained=True)

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
trans = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    normalize,
])


def features(x):
    x = model.conv1(x)
    x = model.bn1(x)
    x = model.relu(x)
    x = model.maxpool(x)
    x = model.layer1(x)
    x = model.layer2(x)
    x = model.layer3(x)
    x = model.layer4(x)
    x = model.avgpool(x)
    return x


def calSimilarity(arr1, arr2):
    list1 = []
    list2 = []
    for i in range(2048):
        list1.append(arr1[0][i][0][0])
        list2.append(arr2[0][i][0][0])
    arr1 = np.array(list1)
    arr2 = np.array(list2)
    return np.inner(np.array(arr1), np.array(arr2)) / (np.linalg.norm(arr1) * np.linalg.norm(arr2))


imginfo = dict()
rf = open("code/img index.txt", "r", encoding = "utf-8")
while True:
    line = rf.readline()
    if len(line) == 0:
        break
    info = line.split("\t")
    info[-1] = info[-1].rstrip("\n")
    index = int(info[0])
    src = info[1]
    url = info[2]
    imginfo[index] = [src, url]


def searchimg(search_image):
    search_image = default_loader(search_image)
    input_image=trans(search_image)
    input_image=torch.unsqueeze(input_image,0)
    search_feature=features(input_image)
    search_feature=search_feature.detach().numpy()
    similar = []
    for i in range(30001, 44565):
        feature = np.load('imgsearch/features/' + str(i) + '.npy', encoding = "latin1")
        s = calSimilarity(search_feature, feature)
        similar.append([i, s])
    for i in range(1,14197):
        feature = np.load('imgsearch/features/' + str(i) + '.npy', encoding = "latin1")
        s = calSimilarity(search_feature, feature)
        similar.append([i, s])
    similar = sorted(similar, reverse = True, key = lambda x: x[1])


    result=[]#按照顺序相关性从大到小存储single_result

    total = len(similar)
    for i in range(1, 20):
        if i > total:
            break
        single_result=dict()#用dict存储
        single_result['url']=imginfo[similar[i-1][0]][1]
        single_result['img']=imginfo[similar[i-1][0]][0]
        result.append(single_result)
    return result
   
