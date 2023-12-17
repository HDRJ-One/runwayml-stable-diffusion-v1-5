import copy
import os
import random
from PIL import Image
import cv2
import h5py
import numpy as np
import torch
from torch.utils.data import Dataset
from torchvision import transforms
from transformers import CLIPTokenizer

from models.blip_override.blip import init_tokenizer


class StoryDataset(Dataset):
    """
    A custom subset class for the LRW (includes train, val, test) subset
    """
    # StoryDataset 类的构造函数
    def __init__(self, subset, args):
        # 用来调用父类 Dataset 的初始化函数，确保该类能够继承 Dataset 类的所有方法和属性。
        super(StoryDataset, self).__init__()
        # args 则是该类的其他参数，是一个命名空间（namespace）对象
        self.args = args
        # 一个 HDF5 文件的路径，存储了训练、验证和测试集的图像和文本数据。
        # ——args.get(args.dataset)表示从命名空间对象args中获取指定数据集（训练集、验证集或测试集）的参数。
        self.h5_file = args.get(args.dataset).hdf5_file
        # 初始化函数中 subset 表示要读取的子集的类型（如训练集、验证集、测试集）
        self.subset = subset

        # 一个图像变换函数序列（transform），用来对图像进行预处理，包括将图像转化为 PIL 格式，调整图像大小，将图像转换为 Tensor，并进行归一化。
        self.augment = transforms.Compose([
            transforms.ToPILImage(),
           # transforms.Resize([256, 256]),
            transforms.Resize([512, 512]),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5])
        ])
        # 表示当前数据集的类型（训练集、验证集或测试集）
        self.dataset = args.dataset
        # 最大的 caption 长度,在进行tokenize操作时，caption中的单词数量将被填充到该长度。
        self.max_length = args.get(args.dataset).max_length
        # 一个使用CLIP模型进行tokenize的tokenizer
        self.clip_tokenizer = CLIPTokenizer.from_pretrained('runwayml/stable-diffusion-v1-5', subfolder="tokenizer")
        # 一个自定义的tokenizer，用于处理文本输入
        self.blip_tokenizer = init_tokenizer()
        msg = self.clip_tokenizer.add_tokens(list(args.get(args.dataset).new_tokens))
        print("clip {} new tokens added".format(msg))
        msg = self.blip_tokenizer.add_tokens(list(args.get(args.dataset).new_tokens))
        print("blip {} new tokens added".format(msg))

        # 一个用于对输入的图像进行处理的函数序列，包括转换为PIL图像、重置图像大小、转换为tensor、归一化等。
        self.blip_image_processor = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize([224, 224]),
            transforms.ToTensor(),
            transforms.Normalize([0.48145466, 0.4578275, 0.40821073], [0.26862954, 0.26130258, 0.27577711])
        ])

    #  打开与数据集对应的h5文件
    def open_h5(self):
        h5 = h5py.File(self.h5_file, "r")
        self.h5 = h5[self.subset]

    # 用于按索引获取数据。

    # 对于每个图像，都进行数据增强操作，以进行数据增强。
    # 然后，将文本输入的caption进行tokenize操作，
    # 使用CLIP tokenizer和自定义tokenizer分别进行tokenize。
    # 最后，将处理好的图像、caption和attention mask返回
    def __getitem__(self, index):
        # 首先调用open_h5()打开数据集的h5文件
        if not hasattr(self, 'h5'):
            self.open_h5()
        #index = 1
        images = list()
        for i in range(5):
            # 从h5文件中读取一组图像和对应的文本。
            im = self.h5['image{}'.format(i)][index]
            # print(im)
            # pil_img = Image.fromarray(im)
            # # 保存图像
            # pil_img.save(os.path.join('/root/lihui/StoryVisualization/ori_test_images', '{:04d}.png'.format(i)))
            # 对每个图像解码
            im = cv2.imdecode(im, cv2.IMREAD_COLOR)
            # 随机选择一个128像素的图像切片
            idx = random.randint(0, im.shape[0] / 128 - 1)
            # 将切片后的图像加到images列表中
            images.append(im[idx * 128: (idx + 1) * 128])
        # 深拷贝，后续不随images变化
        ori_images = copy.deepcopy(images)
        # 保存test原始图像

        # for i, im in enumerate(images):
        #     file_path = '/root/lihui/StoryVisualization/ori_test_images/group{:02d}_image{:02d}.png'.format(index + 1,
        #                                                                                                     i + 1)
        #     cv2.imwrite(file_path, im)
        # 将图像转换为张量
        source_images = torch.stack([self.blip_image_processor(im) for im in images])
        # 如果为continuation任务，将列表中的第一个图像从images中移除
        images = images[1:] if self.args.task == 'continuation' else images
        # 如果subset的值为train/val，则使用augment方法对images列表中的所有图像进行数据增强，并将其转换为张量
        # 否则使用numpy.array方法将images列表转换为张量，并进行转置操作
        images = torch.stack([self.augment(im) for im in images]) \
            if self.subset in ['train', 'val'] else torch.from_numpy(np.array(images)).permute(0, 3, 1, 2)
        ######################
        # 读取当前索引处的文本，并使用decode方法将其解码为UTF-8
        texts = self.h5['text'][index].decode('utf-8').split('|')
        # print(f"index: {index}")
        # for text in texts:
        #     print(f"texts: {text}")

        # tokenize caption using default tokenizer
        tokenized = self.clip_tokenizer(
            texts[1:] if self.args.task == 'continuation' else texts,
            padding="max_length",
            max_length=self.max_length,
            truncation=False,
            return_tensors="pt",
        )
        captions, attention_mask = tokenized['input_ids'], tokenized['attention_mask']

        tokenized = self.blip_tokenizer(
            texts,
            padding="max_length",
            max_length=self.max_length,
            truncation=False,
            return_tensors="pt",
        )
        source_caption, source_attention_mask = tokenized['input_ids'], tokenized['attention_mask']
        return images, captions, attention_mask, source_images, source_caption, source_attention_mask, texts, ori_images

    # 返回数据集中样本的数量
    # 如果是测试集，则返回100，否则返回对应的数据集中的样本数量
    def __len__(self):
        if not hasattr(self, 'h5'):
            self.open_h5()
        if self.subset == 'test':
            #print('')
            return 1
        # if self.subset == 'test':
        #     return 100
        return len(self.h5['text'])