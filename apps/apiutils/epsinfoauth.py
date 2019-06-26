import json
import requests
import urllib


class EnterpriseInfoAuthInterface(object):
    """
    企业认证第三方接口
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.send_url = "http://v.juhe.cn/youshu/query"

    def send_auth(self, name):
        # 定义企业认证所需的参数字典
        params = {}

        # 根据参数说明，按需添加所需的参数
        params['key'] = self.api_key  # 必填
        params['name'] = name  # 必填
        
        # 拼接企业认证请求url
        url = self.send_url + "?" + urllib.parse.urlencode(params)

        # 通过urllib发送请求
        request = urllib.request.Request(url)
        result = urllib.request.urlopen(request)

        # 接口返回数据
        jsonarr = json.loads(result.read().decode('utf-8'))

        return jsonarr
