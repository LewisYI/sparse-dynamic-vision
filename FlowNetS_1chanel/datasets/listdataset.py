import torch.utils.data as data
import os
import os.path
from imageio import imread
import numpy as np
import torch
import pandas as pd
from pygments.lexer import combined


def load_img_from_csv(csv_path):
    # 读取csv
    df = pd.read_csv(csv_path, header=None)
    # 计算最大值和最小值
    max_value = df.max().max()
    min_value = df.min().min()
    # 归一化到 [-1, 1]
    normalized_df = 2 * (df - min_value) / (max_value - min_value) - 1
    # normalized_df = df / 10e-5
    # 映射到 0-255 之间（灰度图像）
    # image_data = ((normalized_df + 1) / 2 * 255).astype(np.uint8)
    # 转换为 NumPy 数组
    # image_array = image_data.to_numpy()
    # print(np.expand_dims(normalized_df.to_numpy(), axis=2).shape)
    return np.expand_dims(normalized_df.to_numpy(), axis=2) # 384x512x1

def load_flo(path):
    with open(path, "rb") as f:
        magic = np.fromfile(f, np.float32, count=1)
        assert 202021.25 == magic, "Magic number incorrect. Invalid .flo file"
        h = np.fromfile(f, np.int32, count=1)[0]
        w = np.fromfile(f, np.int32, count=1)[0]
        data = np.fromfile(f, np.float32, count=2 * w * h)
    # Reshape data into 3D array (columns, rows, bands)
    data2D = np.resize(data, (w, h, 2))
    return data2D


def default_loader(root, path_imgs, path_flo):
    imgs = [os.path.join(root, path) for path in path_imgs]
    flo = os.path.join(root, path_flo)
    return [imread(img).astype(np.float32) for img in imgs], load_flo(flo)


def ran_default_loader(root, path_imgs, path_flo):
    imgs = [os.path.join(root, path) for path in path_imgs]
    flo = os.path.join(root + "data", path_flo)
    # return [load_img_from_csv(imgs[0]), imread(imgs[1]).astype(np.float32)], load_flo(flo)
    return [load_img_from_csv(img) for img in imgs], load_flo(flo)


class ListDataset(data.Dataset):
    def __init__(
        self,
        root,
        path_list,
        transform=None,
        target_transform=None,
        co_transform=None,
        loader=ran_default_loader, #  这里重点要修改
    ):

        self.root = root
        self.path_list = path_list
        self.transform = transform
        self.target_transform = target_transform
        self.co_transform = co_transform
        self.loader = loader

    def __getitem__(self, index):
        inputs, target = self.path_list[index]

        inputs, target = self.loader(self.root, inputs, target)

        if self.co_transform is not None:
            inputs, target = self.co_transform(inputs, target)
        if self.transform is not None:
            inputs[0] = self.transform(inputs[0])
            # inputs[1] = self.transform(inputs[1])
        if self.target_transform is not None:
            target = self.target_transform(target)

        return inputs, target

    def __len__(self):
        return len(self.path_list)
