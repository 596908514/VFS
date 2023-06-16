# 使用教程(chrome + chromedriver + anaconda + python + selenium)

## 安装 chrome

安装chrome：[点击这里](https://www.google.com/chrome/)
安装完成后，打开chrome要查看你的Chrome版本，在浏览器中输入chrome://version/

## 安装 chromedriver

[点击这里](https://chromedriver.storage.googleapis.com/index.html)找到版本的chromedriver下载，windows 选择 **chromedriver_win32.zip**。下载完毕之后解压安装，建议将 chromedriver.exe 文件放置在代码目录下，方便引用

## 安装 anaconda + python

[详细知乎教程](https://zhuanlan.zhihu.com/p/32925500)

## 下载代码安装环境

 1. 配置 conda 环境 ```conda create -n vfsbot python=3.8```
 2. 激活环境 ```conda activate vfsbot```
 3. git项目代码 ```git clone git@github.com:596908514/VFS.git```
 4. 在 vfsbot 环境内安装依赖包 ```pip install -r requirements.txt```
 5. 循环执行指令 ```for /l %a in (0,0,1) do python vfs_v1.py```

## 细节部分

修改 vfs_v1.py 中的 chrome 和 chromedriver 的文件位置

```python
options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'```
browser = webdriver.Chrome(service=c_Service(r'C:\Users\潘克豪\Desktop\vfs_appointment\chromedriver.exe'), options=options)
```
