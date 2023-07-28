### 实验报告
---
#### 网页用户登录
1.有关用户名的规范问题：
- 限制在15 个字符以内（包括中英文以及特殊符号）
    通过在网页端通过 JS 进行关键字屏蔽检测并反馈提醒消息

2.登录密码的规范问题：
- 需要同时包含大、小写字母和数字
- 长度不小于8位不大于15位
    通过 JS 设计口令强度检测并反馈，将口令强度设计为 弱-中-强 三级，成功注册需要至少中及以上等级
    使用了zxcvbn 作为使用方法

3.禁止明文储存
- 禁止明文储存，使用Mysql作为后端数据库储存用户名和密码
    用PBKDF2密钥生成器（基本原理是通过一个伪随机函数（例如HMAC函数），把明文和一个盐值作为输入参数，然后重复进行运算，并最终产生密钥）的方式保存
![](/用户名和密码数据库.png)
    可看出对用户的账号和密码都是进行了加密的

- 用 文件储存方式 储存用户上传的文件
    从前端开始，使用 js 对上传文件的文件名和类型进行检测 后端使用 python、反向代理等对上传文件的文件名和类型进行检测
    
    ```
    fileTypeWhiteList=['jpg','png','gif','jpeg','bmp','doc','docx','xls','xlsx','ppt','pptx']
    ...
    assert fileExtension not in fileTypeWhiteList,'不允许的文件类型'
    ```

    后端存储过程：
        -文件上传将先在前端由 js 对内容进行 hash，然后将文件和 hash 值都传递至服务器。
        -服务器接收到后，先用相同的 hash 函数对收到的文件进行完整性验证，若失败则返回上传失败，成功则继续执行。
        -后先将文件保存到temp目录下，获取文件的各种信息，owner_uid 通过session 获得，随后将文件对应的元信息存入数据库中。
        -随后将文件的原文件名抹去后缀后追加文件名的hash值在其他目录下进行储存。
        -最后将文件内容以对称加密方式进行加密存储，对称密钥的密钥种子采用上传用户的信息的 hash 值进行生成

#### 数据库的设计
查询和管理员的账号均为本地（localhost）账号
- 创建数据库
    create DATABASE bigflydb
- 创建用户
- 创建用户信息表
    ```
    CREATE TABLE `bigflydb`.`user_info` (
    `uid` INT NOT NULL,
    `name` VARCHAR(512) NULL,
    `email` VARCHAR(512) NULL,
    `tele` VARCHAR(512) NULL,
    `password` VARCHAR(512) NULL,
    `wechat` VARCHAR(512) NULL,
    `weibo` VARCHAR(512) NULL,
    `ischeck` TINYINT ZEROFILL NULL DEFAULT 0,
    `isfrozen` TINYINT ZEROFILL NULL DEFAULT 0,
    PRIMARY KEY (`uid`),
    UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
    UNIQUE INDEX `tele_UNIQUE` (`tele` ASC) VISIBLE,
    UNIQUE INDEX `wechat_UNIQUE` (`wechat` ASC) VISIBLE);
    ```

- 创建文件上传信息表
    ```
    CREATE TABLE `bigflydb`.`file_info` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `filename` VARCHAR(45) NOT NULL,
  `owner_uid` INT NOT NULL,
  `upload_date` DATE NOT NULL,
  `filehash` VARCHAR(512) NOT NULL,
  `invalid_date` DATE NOT NULL,
  `isshared` TINYINT DEFAULT 0, 
  `filesize` INT NOT NULL,
  PRIMARY KEY (`id`));
    ```

#### 基于网页的用户注册和重置密码的安全验证

这一部分主要是用户在注册和重置密码阶段所需要的邮箱验证码功能
- 需要配置一个邮件服务器
    首先注册一个邮箱，本次实验所用邮箱服务器为xiaobaibaiyang@163.com
    注册完毕后需要去邮箱里设置授权密码（得到后记录下来）
    这样在代码部分将邮箱填写真实的发邮件服务器用户名、密码
    ```
    user = 'xiaobaibaiyang@163.com'
    password = '******'(此为所得到的授权密码，为保护隐私，不展示出来)
    ```
- 用Python使用SMTP发送邮件
    https://www.runoob.com/python/python-email.html（参考网址）

#### flask框架的构建
- 借用了网上的模板
- 关于自签发证书
    该功能未能实现，在参考了网上的资料后仍然未能成功，浏览器均认定证书不安全，网页URL栏会显示红色

#### 问题与反思
- 1.邮件服务器的配置过程中，起初并不知道需要填的password部分为邮箱里的授权密码，导致发送邮箱出现了失败的情况，后在网上查询后得知是需要这个才能实现。最终成功
- 2.但是关于上述邮件服务器的配置问题，虽然配置成功，但是在注册的发送验证码环节，却出现了注册的邮箱并不能接收到验证码的情况 
    在登录发送方邮箱后，发现出现了如下报错：
    ![](/问题1.png)
    因为该邮箱为163邮箱，而注册的邮箱为qq邮箱，于是在尝试用163邮箱注册后，又能注册成功，尚不知道问题出在哪
- 3.有关数据库的运用
    在建立数据库后，不知是否是下载的数据库软件问题（使用的mysql和naclcat），出现了注册无效的情况，后发现是因为naclcat处于启动的状态，此状态下并不能修改数据库，需要将naclcat关闭之后才能成功注册，使数据进入数据库之中。

