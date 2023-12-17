### 一、基于叙事文本的跨模态序列图像生成模型

## 安装环境
conda create -n arldm python=3.8
conda activate arldm
conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch-lts
cd /root/lihui/StoryVisualization
pip install -r requirements.txt
## 数据准备
Download the PororoSV dataset here.
To accelerate I/O, using the following scrips to convert your downloaded data to HDF5
python data_script/pororo_hdf5.py
--data_dir /path/to/pororo_data
--save_path /path/to/save_hdf5_file
## 配置文件config.yaml

#device
mode: sample # train sample
ckpt_dir: /root/lihui/StoryVisualization/save_ckpt_epoch5_new # checkpoint directory
run_name: ARLDM # name for this run

#train
train_model_file: /root/lihui/StoryVisualization/save_ckpt_3last50/ARLDM/last.ckpt # model file for resume, none for train from scratch

#sample
test_model_file: /root/lihui/StoryVisualization/save_ckpt_3last50/ARLDM/last.ckpt # model file for test
sample_output_dir: /root/lihui/StoryVisualization/save_samples_128_epoch50 # output directory
## 训练
在 config.yaml 中指定您的目录和设备配置并运行：
python main.py
## 采样
在 config.yaml 中指定您的目录和设备配置并运行：
python main.py
## 引用
@article{pan2022synthesizing,
  title={Synthesizing Coherent Story with Auto-Regressive Latent Diffusion Models},
  author={Pan, Xichen and Qin, Pengda and Li, Yuhong and Xue, Hui and Chen, Wenhu},
  journal={arXiv preprint arXiv:2211.10950},
  year={2022}
}


### 二、基于Real-ESRGAN的超分算法
Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data
 [论文]   [项目主页]   [YouTube 视频]   [B站视频]   [Poster]   [PPT]
Xintao Wang, Liangbin Xie, Chao Dong, Ying Shan 
Tencent ARC Lab; Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences
## 环境
Python >= 3.7 (推荐使用Anaconda或Miniconda)
PyTorch >= 1.7
## 安装
1、直接进入已配好的文件夹
cd /root/lihui/StoryVisualization/Real-ESRGAN
2、或 把项目克隆到本地
bash git clone https://github.com/xinntao/Real-ESRGAN.git cd Real-ESRGAN
3、 安装各种依赖
 ```bash
   安装 basicsr - https://github.com/xinntao/BasicSR
   #我们使用BasicSR来训练以及推断
   pip install basicsr
   #facexlib和gfpgan是用来增强人脸的
   pip install facexlib pip install gfpgan pip install -r requirements.txt python setup.py develop 
   ```
## 训练
训练好的模型: RealESRGAN_x4plus_anime_6B
有关waifu2x的更多信息和对比在anime_model.md中。
## 下载模型
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P weights
## 推断
python inference_realesrgan.py -n RealESRGAN_x4plus_anime_6B -i inputs
结果在results文件夹
## BibTeX 引用
@Article{wang2021realesrgan,
    title={Real-ESRGAN: Training Real-World Blind Super-Resolution with Pure Synthetic Data},
    author={Xintao Wang and Liangbin Xie and Chao Dong and Ying Shan},
    journal={arXiv:2107.10833},
    year={2021}
}


### 三、基于YOLOv5的目标角色检测算法
## 安装
克隆 repo，并要求在 Python>=3.7.0 环境中安装 requirements.txt ，且要求 PyTorch>=1.7 。
git clone https://github.com/ultralytics/yolov5  # clone
cd /root/lihui/StoryVisualization
cd yolov5
pip install -r requirements.txt  # install
## 转换图片
cd /root/lihui/StoryVisualization
python transtoyolo.py
## 使用 detect.py 推理
detect.py 在各种来源上运行推理， 模型 自动从 最新的YOLOv5 release 中下载，并将结果保存到 runs/detect 。
python detect.py --weights yolov5s.pt --source 0                               # webcam
                                               img.jpg                         # image
                                               vid.mp4                         # video
                                               screen                          # screenshot
                                               path/                           # directory
                                               list.txt                        # list of images
                                               list.streams                    # list of streams
                                               'path/*.jpg'                    # glob
                                               'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                               'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream
## 训练
 最新的 模型 和 数据集 将自动的从 YOLOv5 release 中下载。 YOLOv5n/s/m/l/x 在 V100 GPU 的训练时间为 1/2/4/6/8 天（ 多GPU 训练速度更快）。 尽可能使用更大的 --batch-size ，或通过 --batch-size -1 实现 YOLOv5 自动批处理 。下方显示的 batchsize 适用于 V100-16GB。
python train.py --data xxx.yaml --epochs 500 --weights '' --cfg yolov5l --batch-size 64
# xx.yaml文件为转换后的数据

## 许可
YOLOv5 在两种不同的 License 下可用：
AGPL-3.0 License： 查看 License 文件的详细信息。
企业License：在没有 AGPL-3.0 开源要求的情况下为商业产品开发提供更大的灵活性。典型用例是将 Ultralytics 软件和 AI 模型嵌入到商业产品和应用程序中。在以下位置申请企业许可证 Ultralytics 许可 。


### 四、演示系统

## 指定文件目录并运行：
cd /root/lihui/StoryVisualization/visualsystem
python main.py


#
Your identification has been saved in             .
Your public key has been saved in C:\Users\30254/.ssh/id_ed25519.pub.
