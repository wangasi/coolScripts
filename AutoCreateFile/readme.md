##描述
- 该脚本用于快速创建react-native文件，减少重复性工作
## 使用
- 给文件执行权限 chmod 777 autoCreateFile.py
- ./autoCreateFile.py -o test --desc "new text for test"
- 暂时desc不能包含中文，会报错
##config
- header中添加固定不变的需要添加的头部内容，默认添加FileName,Description和Create时间。
- body，需要添加的父类函数，true添加，false不添加.默认会添加render()函数和constructor(props)函数
