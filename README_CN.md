# 基于docker的android设备治理策略

## 起因

近期在将一些工程容器化的过程中发现，目前docker层面上的设备管理是比较棘手的。一般来说，比较流行的方式是：

```shell
sudo docker run -d --privileged -v /dev/bus/usb:/dev/bus/usb your_image:latest
```

这样做会将 `/dev/bus/usb` 所有设备都挂载到容器上。如果你有多个容器并行，这意味着每个容器都能够操作所有设备，这是不安全且不稳定的。基于这一点，我们希望做到的是：每个容器都**能且只能**使用特定的设备。

## 只在linux上运作

后续所有内容将只在linux系统上讨论，原因大概如下：

- docker本身的实现方式强依赖于linux（例如cgroups与namespace），在其他系统上的运行方式实际上在原生系统上运行了linux虚拟机。
- 就目前而言，在设备管理层面，在windows与mac系统上的坑相当多。除此之外，这两个系统上并不能通过挂载 `/dev/bus/usb` 的方式在容器间共享设备。而且windows的虚拟化方式 `hyper-v` 天生不支持usb设备挂载（[参考](https://forums.docker.com/t/docker-for-windows-usb-support/38693)）
- 下文提供的策略是基于 cgroups 的，而 cgroups 是 linux 的基础内容。[cgroups介绍](https://en.wikipedia.org/wiki/Cgroups)

那么，基于 cgroups，我们可以做什么事？

## cgroups 与 udevadm

利用udevadm，我们可以获取到usb设备的插拔事件。

```shell
➜  udevadm monitor -u --subsystem-match=usb --environment

monitor will print the received events for:
UDEV - the event which udev sends out after rule processing

UDEV  [14578.455127] unbind   /devices/pci0000:00/0000:00:11.0/0000:02:03.0/usb1/1-1/1-1:1.0 (usb)
ACTION=unbind
DEVPATH=/devices/pci0000:00/0000:00:11.0/0000:02:03.0/usb1/1-1/1-1:1.0
DEVTYPE=usb_interface
INTERFACE=255/255/0
PRODUCT=22d9/2774/409
SEQNUM=11716
SUBSYSTEM=usb
TYPE=0/0/0
USEC_INITIALIZED=2145543432

UDEV  [14578.496302] remove   /devices/pci0000:00/0000:00:11.0/0000:02:03.0/usb1/1-1/1-1:1.2 (usb)
ACTION=remove
DEVPATH=/devices/pci0000:00/0000:00:11.0/0000:02:03.0/usb1/1-1/1-1:1.2
DEVTYPE=usb_interface
INTERFACE=255/66/1
MODALIAS=usb:v22D9p2774d0409dc00dsc00dp00icFFisc42ip01in02
PRODUCT=22d9/2774/409
SEQNUM=11730
SUBSYSTEM=usb
TYPE=0/0/0
USEC_INITIALIZED=14578479756
```

在执行命令之后，udevadm将开始持续监听所有的设备插拔事件并打印出来。那么基于此，我们只需要对输出进行过滤分类，就能够获取：

- 设备的插拔事件
- 设备的id（`adb devices`的输出）
- 设备绑定位置（类似`/dev/bus/usb`）

## 在容器间共享设备

既然我们已经知道设备对应的绑定路径，那我们就可以通过 `--device` 或 `-v` 将指定设备挂载到容器中。

### 关于 [ud4d](https://github.com/doringland/ud4d)

这个工具的设计初衷是为了将设备id与它的绑定位置关联起来，在jenkins构建时将其绑定到container中，完成精确管理。

![](pics/adb.svg)

项目主页：https://github.com/doringland/ud4d

### 使用

直接使用官方的docker镜像：

```shell
sudo docker run -d --privileged -v /dev/bus/usb:/dev/bus/usb -v /usr/bin/docker:/bin/docker -v /var/run/docker.sock:/var/run/docker.sock -v /run/udev:/run/udev:ro --net=host --name ud4d_detector williamfzc/ud4d
```

这么做之后，你可以通过9410端口获取到设备对应信息：

```shell
curl http://127.0.0.1:9410/api/device?serial_no=123456F

# if existed, return something like
/dev/bus/usb/001/009

# else
null
```

在生成容器时将其绑定进去即可：)
