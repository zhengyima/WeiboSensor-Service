from django.conf.urls import *
from . import view,api
 
urlpatterns = [
    url(r'^imgupload$', view.fakeImgUpload),
    # url(r'^imgupload2$', view.imgupload),
    url(r'^emotion$', api.emotion),
    url(r'^transform$', api.transform),
    url(r'^getContentList$',api.getContentList),
    url(r'^getLocation$',api.getLocation),
    url(r'^getKeywords$',api.getk),
    url(r'^imguploadBeta$', view.imguploadBeta),
    url(r'^getCountry$', api.getCountry),
    url(r'^getOpinionCount$',api.getOpinionCount)
    
]