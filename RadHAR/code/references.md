# 关键参考文献列表

## 1. 基础理论文献

### 1.1 Vision Transformer相关
1. **An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale**
   - 作者：Dosovitskiy et al.
   - 发表：ICLR 2021
   - 贡献：提出Vision Transformer基础架构
   - 应用：为本项目的基础模型架构提供理论支持

2. **Swin Transformer: Hierarchical Vision Transformer using Shifted Windows**
   - 作者：Liu et al.
   - 发表：ICCV 2021
   - 贡献：提出层次化Vision Transformer架构
   - 应用：启发本项目的多尺度特征提取设计

### 1.2 注意力机制相关
1. **Squeeze-and-Excitation Networks**
   - 作者：Hu et al.
   - 发表：CVPR 2018
   - 贡献：提出通道注意力机制
   - 应用：用于特征重校准模块设计

2. **CBAM: Convolutional Block Attention Module**
   - 作者：Woo et al.
   - 发表：ECCV 2018
   - 贡献：提出空间和通道注意力的组合机制
   - 应用：启发时空特征注意力设计

### 1.3 域适应相关
1. **Domain-Adversarial Training of Neural Networks**
   - 作者：Ganin et al.
   - 发表：JMLR 2016
   - 贡献：提出域对抗训练框架
   - 应用：指导域适应模块设计

2. **Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks**
   - 作者：Zhu et al.
   - 发表：ICCV 2017
   - 贡献：提出循环一致性损失
   - 应用：用于跨域特征映射

## 2. 技术实现参考

### 2.1 特征提取相关
1. **Feature Pyramid Networks for Object Detection**
   - 作者：Lin et al.
   - 发表：CVPR 2017
   - 贡献：提出特征金字塔网络
   - 应用：多尺度特征提取架构设计

2. **EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks**
   - 作者：Tan et al.
   - 发表：ICML 2019
   - 贡献：提出高效网络架构设计方法
   - 应用：模型轻量化设计参考

### 2.2 雷达信号处理相关
1. **RadHAR: Human Activity Recognition from Point Clouds Generated through a Millimeter-wave Radar**
   - 作者：Singh, A. D., Sandha, S. S., Garcia, L., & Srivastava, M.
   - 发表：ACM Workshop on Millimeter-Wave Networks and Sensing Systems (mmNets) 2019
   - 贡献：提出基于毫米波雷达点云的人体活动识别方法
   - 应用：提供数据集和基准实现
   - 引用：@inproceedings{singh2019radhar,
     title={RadHAR: Human Activity Recognition from Point Clouds Generated through a Millimeter-wave Radar},
     author={Singh, Akash Deep and Sandha, Sandeep Singh and Garcia, Luis and Srivastava, Mani},
     booktitle={Proceedings of the 3rd ACM Workshop on Millimeter-wave Networks and Sensing Systems},
     pages={51--56},
     year={2019},
     organization={ACM}
   }

2. **mmMesh: Towards 3D Real-Time Dynamic Human Mesh Construction Using Millimeter-Wave**
   - 作者：Wei et al.
   - 发表：MobiCom 2020
   - 贡献：提出毫米波雷达3D重建方法
   - 应用：启发时空特征建模

## 3. 应用实践参考

### 3.1 实时系统实现
1. **TensorRT: A Platform for High-Performance Deep Learning Inference**
   - 作者：NVIDIA
   - 类型：技术白皮书
   - 贡献：提供深度学习推理优化方案
   - 应用：模型部署优化参考

2. **Deep Learning Inference in Real-time**
   - 作者：Facebook AI Research
   - 类型：技术报告
   - 贡献：实时推理系统设计方法
   - 应用：系统架构设计参考

### 3.2 性能优化相关
1. **MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications**
   - 作者：Howard et al.
   - 发表：arXiv 2017
   - 贡献：提出移动端高效网络设计方法
   - 应用：模型轻量化设计参考

2. **ShuffleNet: An Extremely Efficient Convolutional Neural Network for Mobile Devices**
   - 作者：Zhang et al.
   - 发表：CVPR 2018
   - 贡献：提出高效网络架构
   - 应用：计算效率优化参考

## 4. 最新研究进展

### 4.1 Transformer优化
1. **DeiT: Training Data-efficient Image Transformers & Distillation through Attention**
   - 作者：Touvron et al.
   - 发表：ICML 2021
   - 贡献：提出数据高效的Vision Transformer训练方法
   - 应用：模型训练优化参考

2. **CrossFormer: A Versatile Vision Transformer Based on Cross-scale Attention**
   - 作者：Wang et al.
   - 发表：ICLR 2022
   - 贡献：提出跨尺度注意力机制
   - 应用：多尺度特征处理参考

### 4.2 域适应新进展
1. **TADA: Temporal Adversarial Domain Adaptation**
   - 作者：Wang et al.
   - 发表：NeurIPS 2021
   - 贡献：提出时序域适应方法
   - 应用：时序特征域适应参考

2. **Universal Domain Adaptation through Self Training**
   - 作者：Li et al.
   - 发表：CVPR 2021
   - 贡献：提出自训练域适应方法
   - 应用：域适应训练策略参考
