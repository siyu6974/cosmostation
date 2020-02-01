---
title: 嫦娥4号科学数据熟肉
date: 2020-01-31 23:23:37
tags: 探月 release
---
{% asset_img 0001_blended_fused.jpg "ChangE-4_lander" %}

大家久等了，我终于整理完嫦娥4号任务科学数据的熟肉了。我还做了个视频 [任务回顾+拼接全景展示](https://www.bilibili.com/video/av85766941/)

<!-- more -->

## 背景
[探月工程官网](http://moon.bao.ac.cn)在2020年1月3日发布了以下载荷的PDS格式科学数据。
- 着陆器（嫦娥4号）
    - TCAM 地形地貌相机 
    - LCAM 着陆相机 
- 巡视器（玉兔2号）
    - PCAM 全景相机
    - VNIS 红外成像光谱仪 
    - LPR 测月雷达 

> LCAM的数据很有观赏性但没有可靠的批量下载方法，暂且搁置。（不过官方给出了着陆过程的全分辨率视频）
> VNIS和LPR过于硬核，我缺乏相关知识无法解读。（此外，我感觉VNIS在没有监视相机的辅助下很难发挥科学价值）

## 熟肉说明
我的熟肉包含这次公布数据的[TCAM](http://siyu.china-vo.org/ChangE-4/TCAM/)和[PCAM](http://siyu.china-vo.org/ChangE-4/PCAM/)部分。点击链接即可跳转。

发布的形式类似于外国大佬 Emily Lakdawalla 对嫦娥3号任务做的整理。这些数据也很有意思，链接：[TCAM](http://planetary.s3.amazonaws.com/data/change3/tcam.html), [PCAM](http://planetary.s3.amazonaws.com/data/change3/pcam.html)。

## 制作
由于数据量较大，我编写了python脚本进行批量转换，代码已经[开源](https://github.com/siyu6974/ChangE_4_data_playground)。
具体的处理过程我也许会找时间做个视频或者写下来。

当然了，作为一个懒人，我的数据发布页也是用代码生成的。代码也[开源了](https://github.com/siyu6974/cosmostation/tree/master/source/ChangE-4)。
（其实这不是懒不懒的问题，PCAM几千张图片的链接手动输入可能要写到明年了）
另外不光是生成发布页的代码，你看到的整个网站的代码都是开源的！


