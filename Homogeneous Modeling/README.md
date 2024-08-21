该项目使用modeller进行手动同源建模(Homology Modeling)对缺失部位(在loop区)局部建模(因为确实部位离空腔远，全局相关影响理论上少)补全残基。

流程：

1. 根据官网上信息使用conda安装modeller、添加序列号
2. 使用0_alignment_generator.py生成alignment文件需要的初步信息文件
3. 手动填写alignment文件内容
4. 使用1_modelling-local.py进行局部同源建模



参考：

[About MODELLER (salilab.org)](https://salilab.org/modeller/); [MODELLER初级教程中译 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/404157642);

