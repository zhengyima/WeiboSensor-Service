from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
import requests
import operator

import jieba
import jieba.analyse
import time

@csrf_exempt
def emotion(request):

    key = request.GET["key"]
    url = 'http://183.174.228.90:9993/solr/weibonow2_slave/select?q=Text%3A'+key+'&wt=json&rows=10000&indent=true'
    r = requests.get(url, verify=False)
    r = r.json()["response"]["docs"]
    # print(r)
    positive = 0
    negative = 0
    medium = 0
    key = []
    value = []
    Date = dict()
    for item in r:
        #print(item["Opinion"])
        try:
            if item["Opinion"] == 1:
                #print("hhh")
                # if Date.has_key(item["Date"]):
                if item["Date"] in Date:
                    Date[item["Date"]][2] += 1
                    Date[item["Date"]][3] += 1
                else:
                    Date[item["Date"]] = [0,0,1,1]
                positive += 1
            if item["Opinion"] == -1:
                #print("hhhh")
                if item["Date"] in Date:
                    #print("llll")
                    Date[item["Date"]][0] += 1
                    Date[item["Date"]][3] += 1
                else:
                    # print("aaaa")
                    Date[item["Date"]]  = [1,0,0,1]
                negative += 1
            if item["Opinion"] == 0:
                #print("rrrr")
                if item["Date"] in Date:
                    Date[item["Date"]][1] += 1
                    Date[item["Date"]][3] += 1
                else:
                    Date[item["Date"]]  = [0,1,0,1]
                medium += 1
        except:

            continue
    res = list(sorted(Date.items(),key=lambda d:d[0],reverse=False))
    # print(res)
    for i in res:
        key.append(i[0])
        value.append(i[1])
    context = {'key':key, 'value':value}
    #print(key)
    #print(value)
    # print(context)

    response = HttpResponse(json.dumps(context))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response
    # return render(request, 'dc/message.html',context)

@csrf_exempt
def transform(request):
    print(time.asctime( time.localtime(time.time()) ))
    key = request.GET["key"]
    url = 'http://183.174.228.90:9993/solr/weibonow2_slave/select?q=Text%3A'+key+'&wt=json&rows=10000&indent=true&&fl=PntData_tags%2CEntity_pers%2CEntity_orgs%2COWord_neg%2CDataS_p_location%2COpinion%2COWord_pos%2CDate'
    r = requests.get(url, verify=False)
    r = r.json()["response"]["docs"]
    print(time.asctime( time.localtime(time.time()) ))
    positive = 0
    negative = 0
    medium = 0
    emotionkey = []
    emotionpos = []
    emotionner = []
    emotionneg = []
    emotionall = []
    emotionvalue = []
    topickey = []
    topicvalue = []
    personkey = []
    personvalue = []
    orgkey = []
    orgvalue = []
    poskey = []
    posvalue = []
    negkey = []
    negvalue = []
    opinionkey = []
    opinionvalue = []
    prokey = []
    provalue = []
    citykey = []
    cityvalue = []
    china = []
    Date = dict()
    topic = dict()
    person = dict()
    organize = dict()
    posword = dict()
    negword = dict()
    pro = dict()
    city = dict()
    with open("/home/dou/d_province.json",'r') as load_f:
        load_dict = json.load(load_f)
    for item in load_dict:
        name = item['name'].rstrip(u'省').rstrip(u'市').rstrip(u'自治区').rstrip(u'回族自治区').rstrip(u'壮族自治区').rstrip(u'维吾尔自治区')
        pro[name] = 0
    pro['香港'] = 0
    pro['澳门'] = 0
    pro['台湾'] = 0
    for item in r:
        try:
            for i in item["PntData_tags"]:
                if i in topic:
                    topic[i] += 1
                else:
                    topic[i] = 1
        except:
            pass
        try:
            for i in item["Entity_pers"]:
                if i in person:
                    person[i] += 1
                else:
                    person[i] = 1
        except:
            pass
        try:
            for i in item["Entity_orgs"]:
                if i in organize:
                    organize[i] += 1
                else:
                    organize[i] = 1
        except:
            pass
        try:
            for i in item["OWord_pos"]:
                if i in posword:
                    posword[i] += 1
                else:
                    posword[i] = 1
        except:
            pass
        try:
            for i in item["OWord_neg"]:
                if i in negword:
                    negword[i] += 1
                else:
                    negword[i] = 1
        except:
            pass
        try:
            aa = item["DataS_p_location"].split(' ')
            for a in aa:
                if a in pro:
                    pro[a] += 1
        except:
            pass
        try:
            aa = item["DataS_p_location"].split(' ')
            if (len(aa) == 2) and (aa[0] in pro):
                if aa[1] in city:
                    city[aa[1]] += 1
                else:
                    city[aa[1]] = 1
        except:
            pass
        try:
            if item["Opinion"] == 1:
                if item["Date"] in Date:
                    Date[item["Date"]][2] += 1
                    Date[item["Date"]][3] += 1
                else:
                    Date[item["Date"]] = [0,0,1,1]
                positive += 1
            if item["Opinion"] == -1:
                if item["Date"] in Date:
                    Date[item["Date"]][0] += 1
                    Date[item["Date"]][3] += 1
                else:
                    Date[item["Date"]]  = [1,0,0,1]
                negative += 1
            if item["Opinion"] == 0:
                if item["Date"] in Date:
                    Date[item["Date"]][1] += 1
                    Date[item["Date"]][3] += 1
                else:
                    Date[item["Date"]]  = [0,1,0,1]
                medium += 1
        except:
            continue
    emotiondic = list(sorted(Date.items(),key=lambda d:d[0],reverse=False))
    topicdic = list(sorted(topic.items(),key=lambda d:d[1],reverse=False))
    persondic = list(sorted(person.items(),key=lambda d:d[1],reverse=False))
    orgdic = list(sorted(organize.items(),key=lambda d:d[1],reverse=False))
    posdic = list(sorted(posword.items(),key=lambda d:d[1],reverse=False))
    negdic = list(sorted(negword.items(),key=lambda d:d[1],reverse=False))
    prodic = list(sorted(pro.items(),key=lambda d:d[1],reverse=False))
    citydic = list(sorted(city.items(),key=lambda d:d[1],reverse=False))
    for i in emotiondic:
        emotionkey.append(i[0])
        emotionneg.append(i[1][0])
        emotionner.append(i[1][1])
        emotionpos.append(i[1][2])
        emotionall.append(i[1][3])
    emotionvalue.append(emotionneg)
    emotionvalue.append(emotionner)
    emotionvalue.append(emotionpos)
    emotionvalue.append(emotionall)
    for i in topicdic[-10:]:
        topickey.append(i[0])
        topicvalue.append(i[1])
    for i in persondic[-10:]:
        personkey.append(i[0])
        personvalue.append(i[1])
    for i in orgdic[-10:]:
        orgkey.append(i[0])
        orgvalue.append(i[1])
    for i in posdic[-10:]:
        poskey.append(i[0])
        posvalue.append(i[1])
    for i in negdic[-10:]:
        negkey.append(i[0])
        negvalue.append(i[1])
    for i in prodic[-10:]:
        prokey.append(i[0])
        provalue.append(i[1])
    for i in citydic[-10:]:
        citykey.append(i[0])
        cityvalue.append(i[1])
    for i in prodic:
        china.append({'name':i[0],'value':i[1]})
    if positive>negative:
        opinionkey.append('负面')
        opinionkey.append('正面')
        opinionkey.append('中性')
        opinionvalue.append(negative)
        opinionvalue.append(positive)
        opinionvalue.append(medium)
    else:
        opinionkey.append('正面')
        opinionkey.append('负面')
        opinionkey.append('中性')
        opinionvalue.append(positive)
        opinionvalue.append(negative)
        opinionvalue.append(medium)
    context = {'emotion':{'key':emotionkey, 'value':emotionvalue}, 'subtopic':{'key':topickey,'value':topicvalue},'person':{'key':personkey,'value':personvalue},
                'org':{'key':orgkey,'value':orgvalue}, 'posword':{'key':poskey,'value':posvalue}, 'negword':{'key':negkey,'value':negvalue}, 'Opinion':{'key':opinionkey,'value':opinionvalue},
                'province':{'key':prokey,'value':provalue},'city':{'key':citykey,'value':cityvalue},'chinamap':china}
    response = HttpResponse(json.dumps(context))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    print(time.asctime( time.localtime(time.time()) ))

    return response




@csrf_exempt
def getContentList(request):
    key = request.GET["key"]
    url = 'http://183.174.228.90:9993/solr/weibonow2_slave/select?q=Text%3A'+key+'&sort=Meta_zhan+desc&rows=10000&wt=json&indent=true'
    r = requests.get(url, verify=False)
    r = r.json()["response"]["docs"]
    contentList=[]
    for item in r:
        try:
            content = {}
            content['touxiang']=item['DataS_tou_xiang']
            content['nick_name']=item['DataS_nick_name']
            content['date']=item['Date']
            content['device']=item['DataS_device']
            content['text']=item['Text']
            content['ping']=item['Meta_ping']
            content['zhuan']=item['Meta_zhuan']
            content['zan']=item['Meta_zhan']
        except:
            continue
        contentList.append(content)
    

    response = HttpResponse(json.dumps(contentList))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response



@csrf_exempt
def getk(request):
    key = request.GET["key"]
    tags = getKeywords(key)


    response = HttpResponse(json.dumps({"keywords":tags}))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response
    
@csrf_exempt
def getKeywords(query):

    url = "http://183.174.228.90:9993/solr/weibonow2_slave/select?q=Text%3A" + query + "&wt=json&indent=true&rows=10000&fl=Text"
    r = requests.get(url, verify=False)
    r = r.json()["response"]["docs"]
    contentList = []
    sent = ""
    for d in r:
        contentList.append(d["Text"])
        sent += d["Text"] + "。"
    # print(sent)

    tags = jieba.analyse.extract_tags(sent, topK=100,withWeight=True)

    tags_r = []
    for t in tags:
        tags_r.append({"name":t[0],"value":t[1]})

    # print(tags)
    return tags_r
    

@csrf_exempt
def getCountry(request):
    key = request.GET["key"]
    url = 'http://183.174.228.90:9993/solr/weibonow2_slave/select?q=Text%3A' + key + '&wt=json&rows=10000&indent=true'
    r = requests.get(url, verify=False)
    r = r.json()["response"]["docs"]
    Location = {}
    Location[u'中国'] = 0
    for item in r:
        try:
            if item['DataS_p_location'][0:2] == u'海外':
              temp_loc  = item['DataS_p_location'][3:]
              if(temp_loc==''):
                  continue
              if temp_loc in Location:
                  Location[temp_loc] += 1
              else:
                  Location[temp_loc]=1
            elif item['DataS_p_location'] == u'其他':
                  continue
            else:
                  Location[u'中国']+=1
        except:
            continue
    Country=[]
    Location = sorted(Location.items(), key=operator.itemgetter(1), reverse=False)
    for item in Location:
        country_temp = {}
        country_temp['name']=item[0]
        country_temp['value'] = item[1]
        Country.append(country_temp)
    response = HttpResponse(json.dumps(Country))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response

@csrf_exempt
def getOpinionCount(request):
    key = request.GET["key"]
    url = 'http://183.174.228.90:9993/solr/weibonow2_slave/select?q=Text%3A' + key + '&wt=json&rows=10000&indent=true&group=true&group.field=Opinion&group.limit=0'
    r = requests.get(url, verify=False)
    r = r.json()["grouped"]['Opinion']
    statics={}
    statics['num_match'] = r['matches']
    r = r['groups']
    for item in  r:
        if(item['groupValue']==-1):
            statics['negative'] = item['doclist']['numFound']
        elif(item['groupValue']==0):
            statics['neutral'] = item['doclist']['numFound']
        elif(item['groupValue']==1):
            statics['positive'] = item['doclist']['numFound']
    statics['score'] = round(float(statics['negative']*-1+statics['positive'])/(statics['negative']+statics['positive']),4)
    response = HttpResponse(json.dumps(statics))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response


@csrf_exempt
def getLocation(request):
    key = request.GET["key"]
    url = 'http://183.174.228.90:9993/solr/weibonow2_slave/select?q=Text%3A' + key + '&wt=json&rows=10000&indent=true&fl=DataS_p_location'
    r = requests.get(url, verify=False)
    r = r.json()["response"]["docs"]
    key=[]
    value=[]
    Location = {}
    Location[u'其他']=0
    Location[u'中国']=0
    for item in r:
        try:
           if item['DataS_p_location'][0:2] == u'海外':
              temp_loc  = item['DataS_p_location'][3:]
              if(temp_loc==''):
                  continue
              if temp_loc in Location:
                  Location[temp_loc] += 1
              else:
                  Location[temp_loc]=1
           elif item['DataS_p_location'] == u'其他':
                  Location[u'其他']+=1
           else:
                  Location[u'中国']+=1
        except:
            continue
    new_Location = sorted(Location.items(),key=operator.itemgetter(1),reverse=False)
    for item in new_Location:
        key.append(item[0])
        value.append(item[1])
        # print item[0].strip('u')+":"+str(item[1])
    Location_last={'key':key[-10:],'value':value[-10:]}
    # print(Location_last)
    response = HttpResponse(json.dumps(Location_last))
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"

    return response