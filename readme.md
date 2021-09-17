# hotjb

## Windows 下通过打包的 msi 安装

[GitHub Release](https://github.com/chaosannals/hotjb/releases) 下载并安装，双击 app.exe 启动。

## 通过 Docker 安装使用

```bash
# 拉去镜像
docker pull chaosannals/hotjb:0.1.0

# 直接启动
docker run -itd -p 30000:30000 --name hotjb chaosannals/hotjb:0.1.0
```

## 开发

```bash
docker build -t chaosannals/hotjb:0.1.0 .
```

```bash
python setup.py bdist_msi
```

注：排除打包的 cx_Freeze 。

```ini
cx-Freeze==6.8
cx-Logging==3.0
importlib-metadata==4.8.1
zipp==3.5.0
```
