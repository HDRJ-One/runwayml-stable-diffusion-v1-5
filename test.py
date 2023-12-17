import cv2
import h5py
import copy
import os
import random

import numpy
import numpy as np
from PIL import Image


def gettext(index):
    with h5py.File('/root/lihui/StoryVisualization/pororo.h5', 'r') as h5:
        story = list()
        h5 = h5['test']
        # 读取当前索引处的文本，并使用decode方法将其解码为UTF-8
        texts = h5['text'][index].decode('utf-8').split('|')
        symbol = '\n'
        texts = symbol.join(texts)
    texts = 'Story<' + str(index) + '> :' + '\n' + texts
    print(texts)
    return texts


# for i in range(1000):
#     gettext(i)

# 截取前100的数据集
#                                 ###正确的##############
# # import h5py
# # import numpy as np
# # from PIL import Image
# #
# #
# # # 创建名为“images”的子目录来保存图像
# # os.makedirs("train_images", exist_ok=True)
# #
# # 创建一个h5文件
# nf = h5py.File('/root/lihui/StoryVisualization/pororo_100.h5', "w")
# with h5py.File('/root/lihui/StoryVisualization/pororo.h5', 'r') as f:
#     test_group = f['test']
#     texts = np.array(test_group['text'][()])
#     ngroup = nf.create_group('test')
#     ntext = ngroup.create_dataset('text', (100,), dtype=h5py.string_dtype(encoding='utf-8'))
#     for i in range(100):
#         ntext[i]=texts[i]
#         print(f"样本 {i}:")
#         # for j in range(5):
#         #     # 创建一个固定的文件名来保存图像
#         #     # filename = os.path.join("images", f"image_{i}_{j}.png")
#         #     # # 将HDF5文件中的图像数据保存到文件中
#         #     # with open(filename, "wb") as img_file:
#         #     #     img_file.write(test_group[f'image{j}'][i])
#         #     # 打印文本信息和文件名
#         #     ntext[i]='|'.join(texts[i].decode('utf-8').split('|')[j])
#         # print(f"图像{j}已保存到文件：{filename}")
#         print(ntext[i])
# nf.close()

#保存测试集图像，随机截取视频帧
with h5py.File(r'C:\Users\zjlab\Desktop\StoryVisualization\pororo.h5', 'r') as h5:
    h5 = h5['test']

    for index in range(len(h5['text'])):   #len(h5['text'])
        # index = int(index + 1)
        # print(index)
        images = list()
        for i in range(5):
            # 从h5文件中读取一组图像和对应的文本。
            im = h5['image{}'.format(i)][index]
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
        # ori_images = copy.deepcopy(images)
        # 保存test原始图像

    # for i, im in enumerate(images):
    #     file_path = 'C:/Users/zjlab/Desktop/StoryVisualization/test_images/group{:02d}_image{:02d}.png'.format(
    #             index + 1,
    #             i + 1)
    #     cv2.imwrite(file_path, im)

            ori_images_pil = Image.fromarray(images[i])#numpy.uint8(images[i].detach().cpu().squeeze().float().numpy())).convert("RGB")
            ori_images_pil.save(
              os.path.join('C:/Users/zjlab/Desktop/StoryVisualization/test_images',
                     'group{:02d}_image{:02d}.png'.format(index + 1,i + 1)))