---
title: QuickFits
date: 2021-04-06 08:37:52
tags:
- 开发
- 摄影
---

{% asset_img cover.jpg "cover" %}


{% note success default %}
FITS 图片其实就是有个文件头的 raw 图片
{% endnote %}

断断续续做了一年的 Fits 图片快速预览工具 QuickFits 终于完成了。
<!-- more -->

我一直对 FITS 图片在文件管理器里没有预览图非常不爽，明明是图片，为啥不能像raw一样给个起码的预览呢，QuickFits 是我为了解决这个痛点而写的软件。

在 MacOS 上 QuickFits 以原生 App 形式存在。

在 Windows 上，我把核心部分复用，制作成 [QuickLook for Windows](https://github.com/QL-Win/QuickLook) 的插件，也可以达到接近原生的体验。

功能上，QuickFits 支持
- 自动转色（debayer）
- 自动拉伸（auto stretch）
- 拍摄信息显示
- 图标生成（Mac系统）

QuickFits 的算法部分经过多轮的优化，最新版本 1.1.0 的图片预览速度比最初快了 200%，同时少占用 50% 的内存。可以瞬间打开 4k 分辨率的 294MC 原图。（C++的上限和下限差距真的大啊）

极快的预览速度加上自动的转色拉伸，使 QuickFits 非常适合拍摄现场的曝光检查和后期中的第一轮选片。

## 安装

MacOS 上可以点击[这里](https://apps.apple.com/cn/app/quickfits/id1551075981?mt=12)在 Mac App Store 下载, 如果链接不干活，请搜索 QuickFits 

Windows 平台稍微复杂一些，步骤如下：视频教程：https://www.bilibili.com/video/BV18p4y1872G
1. 以下任一方法 下载并安装 QuickLook for Windows
   - Github [最新版本](https://github.com/QL-Win/QuickLook)
   - [驿站镜像](QuickLook-3.7.3.msi)
2. 以下任一方法 下载我的插件
   - Github [最新版本](https://github.com/siyu6974/QuickLook.Plugin.FitsViewer)
   - [驿站镜像](20240111_QuickLook.Plugin.FitsViewer.qlplugin)
3. 在文件管理器中找到刚刚下载的插件，后缀应该是.qlplugin
4. 单击文件选中，按空格键，在弹出窗口中点击右下的”安装此插件“
5. 重启 QuickLook（或重启电脑）
6. 完成！找一个 fits 文件试试吧

## 源代码

如果你想获得最新版本或者对代码有兴趣，这个项目的代码在[GitHub 上](https://github.com/siyu6974/QuickLook.Plugin.FitsViewer)，给我个 star 呗。