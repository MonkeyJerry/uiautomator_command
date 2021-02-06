import argparse
import sys
import subprocess
import re
import uiautomator2 as u2
import logging
from merry import Merry

logging.getLogger("uiautomator2").disabled = True  # 关闭uiautomator2的logger打印
logging.getLogger("logzero_default").disabled = True  # 关闭uiautomator2初始化时的logger打印

merry = Merry()
merry.logger.disabled = True  # 关闭merry的logger打印


class U2Device:
    def __init__(self):
        uuid_lst = self.get_device_uuid()
        if len(uuid_lst) == 1:
            self.device = u2.connect(uuid_lst[0])
            print(f'{self.device.info.get("displayWidth")} * {self.device.info.get("displayHeight")}')  # 打印屏幕分辨率便于设置相关操作的坐标
        elif len(uuid_lst) > 1:
            raise RuntimeError("more than one device, just support one")
        else:
            raise RuntimeError("please connect your device first")

    @staticmethod
    def get_device_uuid():
        try:
            subprocess.check_output(['adb', 'version'])
        except:
            print('adb not available')
            sys.exit(1)
        stdout, stderr = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                          text=True).communicate()
        pattern = r'([a-z-A-Z0-9]*)\s*device$'
        uuid_lst = re.findall(pattern, stdout, re.M)
        return uuid_lst


def foo(x):
    '''
    命令行输入参数类型转换
    如'1'->1, '2.1'->2.1, 其他保持为原字符串
    '''
    try:
        if x.isdigit():
            return int(x)
        return float(x)
    except:
        return x


parser = argparse.ArgumentParser()

@merry._try
def click(args):
    params = list(map(foo, args.position))
    if len(params) == 1:
        args.u2device.device(text=params[0]).click()
    elif len(params) == 2:
        args.u2device.device.click(params[0], params[1])
    else:
        raise Exception


@merry._try
def double_click(args):
    params = list(map(foo, args.position))
    args.u2device.device.double_click(params[0], params[1])


@merry._try
def long_click(args):
    params = list(map(foo, args.position))
    args.u2device.device.long_click(params[0], params[1])


@merry._try
def swipe(args):
    params_start_point = list(map(foo, args.swipe_start_point))
    params_end_point = list(map(foo, args.swipe_end_point))
    args.u2device.device.swipe(params_start_point[0], params_start_point[1], params_end_point[0], params_end_point[1])


@merry._try
def press(args):
    if args.key_event in ("home", "back"):
        args.u2device.device.press(args.key_event)
    else:
        raise KeyError


def version(args):
    print('0.0.1')


@merry._except(ValueError)
def catch_value_error(e):
    print(f'input parameters error: {e}')


@merry._except(AttributeError)
def catch_attribute_error(e):
    print(f'input parameters error: {e}')


@merry._except(KeyError)
def catch_key_error(e):
    print(f'input parameters error, only supported home or back')


@merry._except(Exception)
def catch_all(e):
    print('input parameters num error or uiautomator error')


def main():
    u2_device = U2Device()
    subparsers = parser.add_subparsers(help='all supported commands')

    click_parser = subparsers.add_parser('click', help='click point or button with text')
    click_parser.add_argument('position', action='store', nargs='*', help='x y or text str')
    click_parser.add_argument('-u2device', action='store', default=u2_device)
    click_parser.set_defaults(func=click)

    double_click_parser = subparsers.add_parser('double_click', help='double click point or button with text')
    double_click_parser.add_argument('position', action='store', nargs=2, help='x y or text')
    double_click_parser.add_argument('-u2device', action='store', default=u2_device)
    double_click_parser.set_defaults(func=double_click)

    long_click_parser = subparsers.add_parser('long_click', help='long click point or button with text')
    long_click_parser.add_argument('position', action='store', nargs=2, help='x y or text')
    long_click_parser.add_argument('-u2device', action='store', default=u2_device)
    long_click_parser.set_defaults(func=long_click)

    swipe_parser = subparsers.add_parser('swipe', help='swipe point a to point b')
    swipe_parser.add_argument('swipe_start_point', action='store', nargs=2, help='start point x y)')
    swipe_parser.add_argument('swipe_end_point', action='store', nargs=2, help='end point x y')
    swipe_parser.add_argument('-u2device', action='store', default=u2_device)
    swipe_parser.set_defaults(func=swipe)

    press_parser = subparsers.add_parser('press', help='press key_event, just support back and home')
    press_parser.add_argument('key_event', action='store',
                              help='key_event,see more at https://github.com/openatx/uiautomator2')
    press_parser.add_argument('-u2device', action='store', default=u2_device)
    press_parser.set_defaults(func=press)

    version_parser = subparsers.add_parser('version', help='print version and exit')
    version_parser.set_defaults(func=version)

    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
else:
    print("this script is intended as a CLI not a package yet")
