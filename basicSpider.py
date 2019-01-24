import sys
import logging
import urllib
from urllib import request,error
import random
import time

# 创建日志的实例
logger = logging.getLogger("basicSpider")

# 定制Logger的输出格式
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

# 创建日志:文件日志，终端日志
file_handler = logging.FileHandler('basicSpider.log')
file_handler.setFormatter(formatter)

consle_handler = logging.StreamHandler(sys.stdout)
consle_handler.setFormatter(formatter)

# 设置默认的日志级别
logger.setLevel(logging.INFO)

# 把文件日志和终端日志添加到日志处理器中
logger.addHandler(file_handler)
logger.addHandler(consle_handler)

PROXY_RANGE_MIN = 1
PROXY_RANGE_MAX = 10
PROXY_RANGE = 2
NUM = 10


def downloadHtml(url, headers=None,
                 proxy=None, num_retries=10,
                 timeout=10, decodeInfo="utf-8"):
    """
    爬虫的get请求，考虑了UA等http request head部分的设置；
    支持代理服务器的信息处理；
    返回的状态码不是200，这时怎么处理；
    考虑超时问题，及网页的编码问题
    """
    html = None

    if num_retries <= 0:
        return html

    # 动态的调整代理服务器的使用策略
    if random.randint(PROXY_RANGE_MIN, PROXY_RANGE_MAX) > PROXY_RANGE:
        logger.info("No Proxy")
        proxy = None

    proxy_handler = urllib.request.ProxyHandler(proxy)
    # 替换handler，以实现可以处理Proxy
    opener = urllib.request.build_opener(proxy_handler)
    # 把opener装载进urllib库中，准备使用
    opener.addheaders = headers
    urllib.request.install_opener(opener)
    # 各种异常捕获
    try:
        response = urllib.request.urlopen(url, timeout = timeout)
        html = response.read().decode(decodeInfo)
    except UnicodeDecodeError:
        logger.error("UnicodeDecodeError")
    except urllib.error.URLError or \
           urllib.error.HTTPError as e:
        logger.error("urllib error")
        if hasattr(e, 'code') and 400 <= e.code < 500:
            logger.error("Client Error")  # 客户端问题，通过分析日志来跟踪
        elif hasattr(e, 'code') and 500 <= e.code < 600:
            html = downloadHtml(url,
                                headers = headers,
                                proxy = proxy,
                                timeout = timeout,
                                decodeInfo = decodeInfo,
                                num_retries = num_retries-1)
            time.sleep(PROXY_RANGE)  # 休息的时间可以自己定义一个策略
    except:
        logger.error("Download error")

    return html


if __name__ == "__main__":
    url = "http://www.baidu.com"
    headers = [("User-Agent",
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")]
    proxy = {"http": "113.67.11.20:9000"}

    print(downloadHtml(url=url, headers=headers, proxy=proxy))

logger.removeHandler(file_handler)
logger.removeHandler(consle_handler)
