from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import time
import requests
from urllib import *

def hello(request):
    return HttpResponse("Hello world")


@csrf_exempt
def fakeImgUpload(request):

    dic = {'nickNameUrl':'https://weibo.com/u/5408596403','nickName':'湖人中文网','avatarUrl':"https://tva2.sinaimg.cn/crop.266.37.762.762.180/005U1UZRjw8fblumsm1c8j30zk0m8tcf.jpg",'url':'https://wx4.sinaimg.cn/mw690/a79720d4gy1g3il4jr0ldj20u014lgu9.jpg','d':1,'text':'#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​#我每天的社交状态#，多伦多大学心理学教授Jordan Peterson教你如何克服社交恐惧和社交焦虑，如果#有社交恐惧的人如何交朋友#[doge]#全球热搞笑榜# L搞笑味的微博视频 ​​​​'}
    docs = [dic,dic,dic,dic,dic,dic,dic,dic,dic,dic,dic,dic]
    response = HttpResponse(json.dumps(docs))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response




@csrf_exempt
def imguploadBeta(request):

    tmpfilename = "test"
    try:
        f = request.FILES['upload']

        timestamp_f = int(time.time())
        
        root_dir = '/home/dou/django-static-files/common_static/images/'
        tmpfilename = root_dir + str(timestamp_f) + f.name
        print(tmpfilename)

        with open(tmpfilename,"wb+") as des:
            for chunk in f.chunks():
                des.write(chunk)


        # imgtxtf = open("/home/dou/weiboImageSpider2/img0603.txt.bk.mini","r")
        imgtxtf = open("/home/dou/weiboImageSpider2/img0603.txt","r")
        imgtxtLines = imgtxtf.readlines()

        imgdict = {}
        for l in imgtxtLines:
            if len(l.split("\t")) == 1:
                continue
            
            path,Id,url,imgurl,txt,nickname,avatarurl,nicknameurl = l.split("\t")
            pid = path.split("/")[-1]
            imgdict[pid] = [path,Id,url,imgurl,txt,nickname,avatarurl,nicknameurl]

        # tmpFileUrl = "http://183.174.228.100:1242/static/images/1559755469i1.jpg"
        tmpFileUrl = "http://183.174.228.100:1241/static/images/" + str(timestamp_f) + f.name

        # solrlireUrl = "http://127.0.0.1:8983/solr/lire/lireq?ms=false&fl=*&field=oh&url="+tmpFileUrl+"&rows=20&accuracy=0.05&candidates=1000"
        # solrlireUrl = "http://127.0.0.1:8983/solr/lire/lireq?ms=false&fl=*&field=jc&url="+tmpFileUrl + "&candidates=100000&accuracy=0.8"
        solrlireUrl = "http://127.0.0.1:8983/solr/lire/lireq?ms=false&url="+tmpFileUrl + "&candidates=100000&accuracy=1&field=" + request.POST["select"]
        r = requests.get(solrlireUrl,verify=False)
        r = r.json()
        print(r)
        # r = json.loads(r)
        docs = r["response"]["docs"]

        for i in range(len(docs)):
            doc = docs[i]
            # docid = doc["id"].split("/")[-1]
            docid = doc["id"].split("/")[-1]

            # docurl = "http://183.174.228.100:1241/static/flickr30k-images/" + docid
            try:
                docurl = imgdict[docid][3]
            except:
                continue
            # docurl = "https://wx1.sinaimg.cn/mw690/" + docid
            # docs[i]["url"] = docurl
            docs[i]["url"] = "http://183.174.228.100:1241/static/downloads2/" + imgdict[docid][0]
            docs[i]['nickNameUrl'] = 'https://weibo.com/u/' + str(imgdict[docid][7])
            docs[i]["Text"] = imgdict[docid][4]
        
            docs[i]['nickName'] = imgdict[docid][5]
            docs[i]["avatarUrl"] = imgdict[docid][6]
        
        docs = sorted(docs,key=lambda e:e["d"], reverse=False)

    except:
        traceback.print_exc()
    
    response = HttpResponse(json.dumps(docs))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response

@csrf_exempt
def imgupload(request):

    tmpfilename = "test"
    try:
        f = request.FILES['upload']

        timestamp_f = int(time.time())
        
        root_dir = '/home/dou/django-static-files/common_static/images/'
        tmpfilename = root_dir + str(timestamp_f) + f.name
        print(tmpfilename)

        with open(tmpfilename,"wb+") as des:
            for chunk in f.chunks():
                des.write(chunk)


        imgtxtf = open("/home/dou/weiboImageSpider2/img0603.txt","r")
        imgtxtLines = imgtxtf.readlines()

        imgdict = {}
        for l in imgtxtLines:
            path,Id,url,imgurl = l.split("\t")
            pid = path.split("/")[-1]
            imgdict[pid] = imgurl

        # tmpFileUrl = "http://183.174.228.100:1242/static/images/1559755469i1.jpg"
        tmpFileUrl = "http://183.174.228.100:1241/static/images/" + str(timestamp_f) + f.name

        # solrlireUrl = "http://127.0.0.1:8983/solr/lire/lireq?ms=false&fl=*&field=oh&url="+tmpFileUrl+"&rows=20&accuracy=0.05&candidates=1000"
        # solrlireUrl = "http://127.0.0.1:8983/solr/lire/lireq?ms=false&fl=*&field=jc&url="+tmpFileUrl + "&candidates=100000&accuracy=0.8"
        solrlireUrl = "http://127.0.0.1:8983/solr/lire/lireq?ms=false&url="+tmpFileUrl + "&candidates=100000&accuracy=1"
        r = requests.get(solrlireUrl,verify=False)
        r = r.json()
        print(r)
        # r = json.loads(r)
        docs = r["response"]["docs"]

        for i in range(len(docs)):
            doc = docs[i]
            # docid = doc["id"].split("/")[-1]
            docid = doc["id"].split("/")[-1]

            # docurl = "http://183.174.228.100:1241/static/flickr30k-images/" + docid
            # docurl = imgdict[docid]
            docurl = "https://wx1.sinaimg.cn/mw690/" + docid
            docs[i]["url"] = docurl
        
        docs = sorted(docs,key=lambda e:e["d"], reverse=False)

    except:
        traceback.print_exc()
    
    response = HttpResponse(json.dumps(docs))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response