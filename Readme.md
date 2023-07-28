# 中传放心传

## 文件说明
  - code文件为本次实验的全部代码
  - 其余的0_**为个人的readme
  - 本readme为实验的总readme

## 任务目标
### 分组完成【候选】题目-1 “中传放心传”

- 基于网页的用户注册与登录系统（60分）

  - [ ] 使用https绑定证书到域名而非IP地址 【 *PKI* *X.509* 】

  - [x] 允许用户注册到系统 

    - 用户名的合法字符集范围：中文、英文字母、数字
    - 类似：-、_、.等合法字符集范围之外的字符不允许使用
    - 用户口令长度限制在36个字符之内
    - 对用户输入的口令进行强度校验，禁止使用弱口令

  - [x] 使用合法用户名和口令登录系统

  - [x] 禁止使用明文存储用户口令 ：

    ​	PBKDF2

    ​	散列算法

    ​	慢速散列

    ​	针对散列算法（如MD5、SHA1等）的攻击方法

    - 存储的口令即使被公开，也无法还原/解码出原始明文口令

  - [x] （可选）安全的忘记口令 / 找回密码功能 

  - [ ] （可选）微信/微博/支付宝的OAuth授权登录 / 注册绑定 

  - [x] （可选）双因素认证 

    - OTP: Google Authenticator
    - Email
    - SMS
    - 扫码登录

- 基于网页的文件上传加密与数字签名系统（20分）

  - [ ] 已完成《基于网页的用户注册与登录系统》所有要求
  - [x] 限制文件大小：小于 10MB
  - [x] 限制文件类型：office文档、常见图片类型
  - [x] 匿名用户禁止上传文件
  - [ ] 对文件进行对称加密存储到文件系统，禁止明文存储文件 【 *对称加密* *密钥管理（如何安全存储对称加密密钥）* *对称加密密文的PADDING问题* 】
  - [ ] 系统对加密后文件进行数字签名 【 *数字签名（多种签名工作模式差异）* 】
  - [x] （可选）文件秒传：服务器上已有的文件，客户端可以不必再重复上传了

- 基于网页的加密文件下载与解密（20分）

  - [ ] 已完成《基于网页的文件上传加密与数字签名系统》所有要求
  - [x] 提供匿名用户加密后文件和关联的数字签名文件的下载
    - 客户端对下载后的文件进行数字签名验证 【 *非对称（公钥）加密* *数字签名* 】
    - 客户端对下载后的文件可以解密还原到原始文件 【 *对称解密* *密钥管理* 】
  - [x] 提供已登录用户解密后文件下载
  - [ ] 下载URL设置有效期（限制时间或限制下载次数），过期后禁止访问 【 *数字签名* *消息认证码* *Hash Extension Length Attack* *Hash算法与HMAC算法的区别与联系* 】
  - [x] 提供静态文件的散列值下载，供下载文件完成后本地校验文件完整性 【 *散列算法* 】

### 问题清单
- 同一个用户的不同文件是否使用相同的对称加密密钥？如果是，请说明其中存在的安全风险。如果否，请结合代码展示你们的文件对称加密密钥的存储和提取使用策略
--
    对于同一个用户的不同文件，通常不应使用相同的对称加密密钥。这是因为如果相同的密钥用于加密多个文件，一旦该密钥被泄露或破解，所有使用该密钥加密的文件将处于危险之中。

    使用相同密钥的安全风险包括：

    泄露风险：如果一个文件的密钥被泄露，攻击者可以解密该文件以及其他使用相同密钥加密的文件。
    密钥弱化：如果相同密钥被用于多个文件，破解一个文件的密钥就等于破解了所有文件的密钥。
    限制分发：如果需要与其他人共享文件，但又不希望他们能够访问其他文件，使用单独的密钥可以更好地控制访问权限。
    以下是一个示例代码，展示了如何存储和提取使用不同密钥的文件对称加密密钥：

python
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

##### 加密函数
def encrypt_file(key, filename):
    # 生成随机的初始化向量
    iv = os.urandom(16)

    # 创建密码器对象
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

    # 打开文件并读取内容
    with open(filename, 'rb') as file:
        plaintext = file.read()

    # 加密数据
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # 返回初始化向量和密文
    return iv, ciphertext

##### 解密函数
def decrypt_file(key, iv, ciphertext):
    # 创建密码器对象
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

    # 解密数据
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # 返回明文数据
    return plaintext

##### 生成随机的对称加密密钥
def generate_key():
    salt = os.urandom(16)
    password = b"your_password"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password)
    return key

##### 示例用法
##### 生成不同的密钥用于不同文件
key1 = generate_key()
key2 = generate_key()

##### 加密文件1
iv1, ciphertext1 = encrypt_file(key1, 'file1.txt')
##### 存储iv1和ciphertext1到数据库或文件中

##### 加密文件2
iv2, ciphertext2 = encrypt_file(key2, 'file2.txt')
##### 存储iv2和ciphertext2到数据库或文件中

##### 解密文件1
plaintext1 = decrypt_file(key1, iv1, ciphertext1)

##### 解密文件2
plaintext2 = decrypt_file(key2, iv2, ciphertext2)

---
- 你们的文件下载过期策略是如何设计并实现的？
    文件信息写入时用触发器自动获取上传的日期并且自动设定过期日期

- 请展示并说明你们的数据库表结构设计
    文件：![](/1.png)

    用户：![](/2.png)
    （wechat，weibo未能实现）

### 仓库
[b站视频](https://www.bilibili.com/video/BV1MP41167KE/?spm_id_from=333.999.0.0&vd_source=73db12613f592227bc706b6e996a5ef0)

[github仓库](https://github.com/Sixer126/CUC_iCloud)

