# ud4d

USB Device Detector for Docker usage. Support Linux only because of [cgroups](https://en.wikipedia.org/wiki/Cgroups).

## Why

![adb](pics/adb.svg)

- Build for sharing devices among docker containers.
- Split `/dev/bus/usb` into pieces, for better control, in different container.
- By `volumes-from`, other (upper) container can operate android devices via these containers.

## How it works

Based on subsystems of cgroups, we can easily use `udevadm` to detect usb actions.

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

Analyse it, and turn it into some PyObject for better usage.

## License

[MIT](LICENSE)
