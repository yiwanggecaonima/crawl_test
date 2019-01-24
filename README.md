# crawl_test

basicSpider.py文件是一个算是比较严谨的一个请求函数吧，捕获各种异常，UA随机请求头，设置随机代理，最大重试,记录日志等等
basicSpider.log  文件是日志输出文件
UA.py就是随机请求头的一个池子
config.py是一个简单的配置文件

douban.py　是一个小例子，调用basicSpider.py　文件请求url,输出日志

