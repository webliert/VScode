# -*- coding:utf-8 -*-
import hashlib
import hmac
import base64
import json
import time

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class AIPPT():

    def __init__(self,APPId,APISecret,Text,templateId):
        self.APPid = APPId
        self.APISecret = APISecret
        self.text = Text
        self.header = {}
        self.templateId = templateId


    #获取签名
    def get_signature(self, ts):
        try:
            # 对app_id和时间戳进行MD5加密
            auth = self.md5(self.APPid + str(ts))
            # 使用HMAC-SHA1算法对加密后的字符串进行加密
            return self.hmac_sha1_encrypt(auth,self.APISecret)
        except Exception as e:
            print(e)
            return None

    def hmac_sha1_encrypt(self, encrypt_text, encrypt_key):
        # 使用HMAC-SHA1算法对文本进行加密，并将结果转换为Base64编码
        return base64.b64encode(hmac.new(encrypt_key.encode('utf-8'), encrypt_text.encode('utf-8'), hashlib.sha1).digest()).decode('utf-8')

    def md5(self, text):
        # 对文本进行MD5加密，并返回加密后的十六进制字符串
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    #创建PPT生成任务
    def create_task(self):
        url = 'https://zwapi.xfyun.cn/api/ppt/v2/create'
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)
        # body= self.getbody(self.text)

        formData = MultipartEncoder(
            fields={
                "file": ("AIPPTtest.docx", open("E:\\Documents\\AIPPTtest.docx", 'rb'), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),  # 如果需要上传文件，可以将文件路径通过path 传入
                # "fileUrl":"E:\Documents\AIPPTtest.docx",   #文件地址（file、fileUrl、query必填其一），文件网络地址
                "fileName":"AIPPTtest.docx",   # 文件名(带文件名后缀；如果传file或者fileUrl，fileName必填)
                # "query": self.text,
                "templateId":"20240718489569D", # 模板的ID,从PPT主题列表查询中获取
                "author":"lxy",    # PPT作者名：用户自行选择是否设置作者名
                "isCardNote" :str(True),   # 是否生成PPT演讲备注, True or False,演讲备注就是在幻灯片播放时，小屏幕上会显示的提示词
                "search" :str(True),      # 是否联网搜索,True or False
                "isFigure" :str(False),   # 是否自动配图, True or False
                "aiImage" :"normal"   # ai配图类型： normal、advanced （isFigure为true的话生效）； normal-普通配图，20%正文配图；advanced-高级配图，50%正文配图
            }
        )

        print(formData)

        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": formData.content_type
        }
        self.header = headers
        print(headers)
        response = requests.request(method="POST",url=url, data= formData,headers=headers).text
        print("生成PPT返回结果：",response)
        resp = json.loads(response)
        if(0 == resp['code']):
            return resp['data']['sid']
        else:
            print('创建PPT任务失败')
            return None

    #构建请求body体
    def getbody(self,text):
        body = {
            "query":text,
            "templateId":self.templateId  #  模板ID举例，具体使用 /template/list 查询
        }
        return body
		
		
	#轮询任务进度，返回完整响应信息
    def get_process(self,sid):
        # print("sid:" + sid)
        if(None != sid):
            response = requests.request("GET",url=f"https://zwapi.xfyun.cn/api/ppt/v2/progress?sid={sid}",headers=self.header).text
            print(response)
            return response
        else:
            return None



    #获取PPT，以下载连接形式返回
    def get_result(self):

        #创建PPT生成任务
        task_id = self.create_task()
        # PPTurl = ''
        #轮询任务进度
        while(True):
            response = self.get_process(task_id)
            resp = json.loads(response)
            pptStatus = resp['data']['pptStatus']
            aiImageStatus = resp['data']['aiImageStatus']
            cardNoteStatus = resp['data']['cardNoteStatus']


            if('done' == pptStatus and 'done' == aiImageStatus and 'done' == cardNoteStatus):
                PPTurl = resp['data']['pptUrl']
                break
            else:
                time.sleep(3)
        return PPTurl

    def getHeaders(self):
        timestamp = int(time.time())
        signature = self.get_signature(timestamp)
        # body = self.getbody(self.text)

        headers = {
            "appId": self.APPid,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": "application/json; charset=utf-8"
        }
        return headers
    


    def getTheme(self):
        url ="https://zwapi.xfyun.cn/api/ppt/v2/template/list"
        self.header = self.getHeaders()
        body = {
            "payType": "not_free",
            "style": "简约",    # 支持按照类型查询PPT 模板
            "color": "蓝色",   #  支持按照颜色查询PPT 模板
            "industry": "教育培训",    # 支持按照颜色查询PPT 模板
            "pageNum": 2 ,
            "pageSize": 10
            }
        
        response = requests.request("GET", url=url, headers=self.header).text
        print(response)
        return response
        return body







if __name__ == '__main__':
    #控制台获取 
    APPId = "10ce6dd0"
    APISecret = "MThkMDFmZmQ1MzNiMDE5YzFjODk3ZDg1"

    # 查询PPT主题列表
    # demo1 = AIPPT(APPId,APISecret,'','')
    # templateId = demo1.getTheme()

    #PPT 主题描述
    Text="请帮我写一份PPT： 主题是AGV小车的调度算法汇报，内容参考我提供给你的文件"
    templateId= "2024071754A6ADE"   # 该模板ID，需要通过getTheme() 方法获取模板列表，然后从中挑选
    # 2024071800368C7 红色商务 20240718489569D-黄色科技 202407176CA9161- 黄色科技？不是蓝色学院 20240718822FE12-红色商务 2024071754A6ADE-未测试
    demo = AIPPT(APPId,APISecret,Text,templateId)


    result = demo.get_result()
    # result = demo1.getTheme()
    print("生成的PPT请从此地址获取：\n" + result)
    # print("PPT主题列表：\n" + result)



