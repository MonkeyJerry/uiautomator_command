# uiautomator_command
基于python，封装uiautomator常用命令，可在unix系统终端直接调用



## 依赖

```
pip install uiautomator2
pip install merry
```



## 添加alias

如我的脚本放在如下目录`~/Documents/pyscripts/uiautomator_command.py`，则可在.zshrc中添加alias如下：

```
alias click="python ~/Documents/pyscripts/uiautomator_command.py click"
alias double_click="python ~/Documents/pyscripts/uiautomator_command.py double_click"
alias long_click="python ~/Documents/pyscripts/uiautomator_command.py long_click"
alias swipe="python ~/Documents/pyscripts/uiautomator_command.py swipe"
alias press="python ~/Documents/pyscripts/uiautomator_command.py press"
```



## 说明

- 仅支持click、double_click、long_click、swipe、press命令
- 仅支持单设备
- 需要安装的库`pip install uiautomator2`、`pip install merry`
- click支持text（需要能用text定位的元素，否则异常）和坐标
- press仅支持home键和back键，需要支持其他keyevent，请自行扩展
- 封装后可结合shell脚本对手机进行操作



## 扩展阅读

- [多线程支持多设备](https://github.com/openatx/uiautomator2/issues/93)
- [uiautomator2](https://github.com/openatx/uiautomator2)
- [我的博客：自定义uiautomator命令行](https://1eq066.coding-pages.com/post/uiautomator_command/)