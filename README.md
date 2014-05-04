funscripts
==========

## getMakeUseOfCheatSheet*.py

爬取静态网页[MakeUseOf Cheat Sheets](http://www.makeuseof.com/pages/downloads)
的下载链接，下载数不多，又是静态的，所以难度不大。

`Python`可以用两种方式进行下载：

1. 使用`urllib,urllib2,urllib3,requests`下载
2. 使用`os.system()`调用`shell`命令下载

两个脚本分别作了实现。
## getDZoneRefCardz.py

此脚本用于下载[DZone RefCardz](http://refcardz.dzone.com/)所有的`pdf`文档，需要此网站注册账号支持。由于此网站注册非常严格，甚至被网友称为[Worst registration form on the internet? DZone.com](http://scott.blomqui.st/2012/07/worst-registration-form-on-the-internet-dzone-com/)，所以注册时我个人推荐使用信息生成器，你懂的。

主要实现了python模拟登陆、网页使用BeautifulSoup4解析与搜索、日记记录、文件名提取
和下载链接数据库存取。

所有相关的文件都存储在'RefCardz'目录下。

由于下载文件较多，因此推荐在网络空闲时段下载。如果中途下载失败，可以重新开始下载
，由于随机搜索的机制，程序不会重新按部就班开始，而是随机选择链接，如果已经下载并
并记录则放弃。


## 爬虫编写的实践积累

### 动态网页分析是难点和重点

静态网页抓取难度不大，而动态网页抓取难点和重点都在分析POST、模拟提交表单上面，
做好了第一步，脚本的编写反而简单了。

### 日志和数据库

推荐使用面向过程方式，对脚本执行每一步做好日志记录，可以省去很多DEBUG的时间。对于
抓取对象很多的情况，用数据库存储链接是很有效的方法，一来保证程序即便中断也不会
重复不必要的操作，二来可以用于后续的处理。

### 网页解析

虽然正则表达式很强大，但是基于两点理由它并不好使：

1. 写出精确匹配健壮性好的表达式很难，尤其是HTML这种有大量重复标签的场合
2. 网页结构经常发生改变

我个人更喜欢BeautifulSoup的解析，基于标签的搜索很容易分析，健壮性也很好。

提取链接或者其它标签时，`find_all()`方法是很常用的，但它往往返回的是一个
按部就班搜索得到的列表。如果脚本中断，重新执行时又会按顺序处理，如果网站对
某个链接的单位时间访问设了限制，就很容易被屏蔽。一个解决思路是利用
`random.shuffle(list)`方法打乱列表内元素顺序，这样每次都是随机开始处理，避免了
个别链接被持续访问的尴尬。
