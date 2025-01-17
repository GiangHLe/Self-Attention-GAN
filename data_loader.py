import torch
import torchvision.datasets as dsets
from torchvision import transforms

from glob import glob
import os
import cv2
import numpy as np
class Cifar(torch.utils.data.Dataset):
    def __init__(self, image_path):
        super().__init__()
        self.X = glob(os.path.join(image_path, '*.png'))
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        image = cv2.imread(self.X[idx]).astype(np.float32)
        image = (image/127.5) - 1
        return torch.tensor(image).permute(2,0,1).float(), torch.Tensor([1])


class Data_Loader():
    def __init__(self, train, dataset, image_path, image_size, batch_size, shuf=True):
        self.dataset = dataset
        self.path = image_path
        self.imsize = image_size
        self.batch = batch_size
        self.shuf = shuf
        self.train = train

    def transform(self, resize, totensor, normalize, centercrop):
        options = []
        if centercrop:
            options.append(transforms.CenterCrop(160))
        if resize:
            options.append(transforms.Resize((self.imsize,self.imsize)))
        if totensor:
            options.append(transforms.ToTensor())
        if normalize:
            options.append(transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)))
        transform = transforms.Compose(options)
        return transform

    def load_lsun(self, classes='church_outdoor_train'):
        transforms = self.transform(True, True, True, False)
        dataset = dsets.LSUN(self.path, classes=[classes], transform=transforms)
        return dataset

    def load_celeb(self):
        transforms = self.transform(True, True, True, True)
        dataset = dsets.ImageFolder(self.path+'/CelebA', transform=transforms)
        return dataset


    def loader(self):
        if self.dataset == 'lsun':
            dataset = self.load_lsun()
        elif self.dataset == 'celeb':
            dataset = self.load_celeb()

        elif self.dataset == 'cifar':
            dataset= Cifar(self.path)

        loader = torch.utils.data.DataLoader(dataset=dataset,
                                              batch_size=self.batch,
                                              shuffle=self.shuf,
                                              num_workers=2,
                                              drop_last=True)
        return loader

