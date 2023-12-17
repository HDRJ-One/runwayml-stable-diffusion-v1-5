import argparse
import os

import cv2
import h5py
import numpy as np
from PIL import Image
from tqdm import tqdm


def main(args):
    # 使用numpy库的load函数来加载名为descriptions.npy的文件。该文件是一个Python字典对象，因此我们使用item()方法将其转换为字典对象。
    # ——os.path.join函数用于连接文件路径
    # ——args.data_dir作为基础目录，将'descriptions.npy'添加到该目录中
    # ——指定allow_pickle=True，表示允许加载包含Python对象的文件
    # ——指定encoding='latin1'，表示使用拉丁字符编码加载该文件
    descriptions = np.load(os.path.join(args.data_dir, 'descriptions.npy'), allow_pickle=True, encoding='latin1').item()
    # imgs_list包含一组图像文件的路径，
    # followings_list包含每个图像的一些附加信息
    imgs_list = np.load(os.path.join(args.data_dir, 'img_cache4.npy'), encoding='latin1')
    followings_list = np.load(os.path.join(args.data_dir, 'following_cache4.npy'))
    # 使用numpy库的load函数来加载名为train_seen_unseen_ids.npy的文件
    # 该文件包含三个numpy数组：train_ids、val_ids和test_ids，分别代表训练集、验证集和测试集的ID列表。
    # 使用元组来一次性加载这三个数组，并将它们赋值给相应的变量。
    train_ids, val_ids, test_ids = np.load(os.path.join(args.data_dir, 'train_seen_unseen_ids.npy'), allow_pickle=True)
    # 按照ID的顺序逐一排序
    train_ids = np.sort(train_ids)
    val_ids = np.sort(val_ids)
    test_ids = np.sort(test_ids)

    # 创建一个新的HDF5文件，并指定文件名为args.save_path。
    # 使用h5py库的File函数来创建文件对象，指定打开方式为写模式("w")。
    # 在这个文件中存储处理后的图像和文本数据。
    f = h5py.File(args.save_path, "w")
    for subset, ids in {'train': train_ids, 'val': val_ids, 'test': test_ids}.items():
        length = len(ids)

        # 为每个数据集（train、val和test）创建一个组
        # 针对每个数据集都创建了5个数据集，名为'image0'、'image1'、'image2'、'image3'、'image4'，分别对应于当前图像及其相关联的4个图像。
        # 目的：将每个图像及其相关联的图像数据保存到同一个HDF5文件中，并按照一定的组织方式存储，方便后续的数据读取和处理。
        group = f.create_group(subset)
        # 创建一个长度为ids列表长度的空列表images，按照image0-4顺序添加了5个HDF5数据集对象
        images = list()
        # 为当前数据集中的每个图像创建了五个数据集。
        # 每个数据集都使用vlen_dtype(np.dtype('uint8'))作为数据类型，并将其添加到当前组group中。
        # ——vlen_dtype(np.dtype('uint8'))表示可变长度的无符号8位整数数组。
        for i in range(5):
            images.append(
                group.create_dataset('image{}'.format(i), (length,), dtype=h5py.vlen_dtype(np.dtype('uint8'))))
        # 创建一个数据集text，用于存储与当前数据集中图像相关的文本描述。该数据集的数据类型为字符串，编码方式为utf-8，并将其添加到当前组group中。
        text = group.create_dataset('text', (length,), dtype=h5py.string_dtype(encoding='utf-8'))
        # 遍历当前数据集中的每个图像，并将相关数据保存到HDF5文件中
        for i, item in enumerate(tqdm(ids, leave=True, desc="saveh5")):
            # 获取与当前图像相关的所有图像的路径，存储到列表img_paths中。
            # ——imgs_list是一个字典，存储了所有图像的路径
            # ——followings_list是一个字典，存储了与每个图像相关的四张图像的路径
            img_paths = [str(imgs_list[item])[2:-1]] + [str(followings_list[item][i])[2:-1] for i in range(4)]
            # 打开img_paths列表中的每个图像，并将其转换为RGB格式的PIL图像对象。
            imgs = [Image.open(os.path.join(args.data_dir, img_path)).convert('RGB') for img_path in img_paths]
            # 将每个PIL图像对象转换为numpy数组
            for j, img in enumerate(imgs):
                img = np.array(img).astype(np.uint8)
                # 使用OpenCV将其编码为png格式的二进制数据
                img = cv2.imencode('.png', img)[1].tobytes()
                # 将该二进制数据转换为numpy数组
                img = np.frombuffer(img, np.uint8)
                # 将其存储到images列表中与当前图像相关的数据集中
                images[j][i] = img
            # 获取与当前图像相关的所有图像的文件名，并将其存储到列表tgt_img_ids中
            tgt_img_ids = [str(img_path).replace('.png', '') for img_path in img_paths]
            # 根据目标图像的文件名，获取其对应的文本描述，并将其存储到列表txt中。
            txt = [descriptions[tgt_img_id][0] for tgt_img_id in tgt_img_ids]
            # 将txt列表中的所有文本描述合并为一个字符串，并将其中的"\n"、"\t"等无关字符替换为空格。然后，将该字符串存储到数据集text中
            text[i] = '|'.join([t.replace('\n', '').replace('\t', '').strip() for t in txt])
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arguments for flintstones pororo file saving')
    parser.add_argument('--data_dir', type=str, required=True, help='pororo data directory')
    parser.add_argument('--save_path', type=str, required=True, help='path to save hdf5')
    args = parser.parse_args()
    main(args)
