# -*- coding: utf-8 -*-

import json
import logging
import datetime
from django.shortcuts import render_to_response
from common import convert, str_tools
from django.http import HttpResponse
from models import Job, VipJobList
from common.oss_tools import OSSTools
from wx_base.backends.common import CommonHelper
from wx_base.backends.dj import Helper
from wx_base import WxPayConf_pub
from user.user_tools import sns_userinfo_with_userinfo, get_userid_by_openid, is_vip
from django.forms.models import model_to_dict

@sns_userinfo_with_userinfo
def index(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    vip_job_from_point = convert.str_to_int(request.GET.get('from', '0'), 0)  # 有from时，则为翻页，无时，则为首页
    number_limit = convert.str_to_int(request.GET.get('limit', '10'), 10)  # 异常情况下，或者不传的情况下，默认为10

    # 取本人发布过的，并且有效的简历
    if vip_job_from_point != 0:
        own_jobs = []
    else:
        own_jobs = Job.objects.filter(user_id=user_id).order_by('-id')[:1]

    # 按发布时间去取VIP发布简历 －－ 以后从缓存中取
    vip_jobs = VipJobList.objects.all().order_by('-pub_time')[vip_job_from_point:number_limit]
    job_id_list = [job.job_id for job in vip_jobs]
    vip_jobs = Job.objects.filter(id__in=job_id_list)

    # 请把own_jobs和vip_jobs渲染到页面上
    return render_to_response('index.html')


@sns_userinfo_with_userinfo
def msg(request):
    return render_to_response('chat/mesg.html')


@sns_userinfo_with_userinfo
def get_job(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    data = {}

    job_uuid = request.GET.get('job_uuid', '')
    job_detail = Job.objects.filter(uuid=job_uuid)[:1]
    if job_detail:
		data = model_to_dict(job_detail, exclude=['is_vip', ])
    else:
        logging.error("uid(%s) try to get not exsit job(%s), maybe attack" % (uid, job_uuid))
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    url = "http://" + request.get_host() + request.path
    sign = Helper.jsapi_sign(url)
    sign["appId"] = WxPayConf_pub.APPID
    data['jsapi'] = json.dumps(sign)

    return render_to_response('job/job_detail.html', data)


#暂时规避跨站攻击保护
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@sns_userinfo_with_userinfo
def post_job(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    company_name = request.POST.get('company_name')
    job_title = request.POST.get('job_title')
    work_experience = request.POST.get('work_experience')
    salary = request.POST.get('salary')
    education = request.POST.get('education')
    city = request.POST.get('city')

    if not (company_name and job_title and work_experience and salary and education and city):
        return HttpResponse("十分抱歉，你输入的参数缺失，请检查确认后重试。重试失败请联系客服人员")

    skill = request.POST.get('skill1') + "," + request.POST.get('skill2') + "," + request.POST.get(
        'skill3') + "," + request.POST.get('skill4') + "," + request.POST.get('skill5') + "," + request.POST.get(
        'skill6')

    piclist = ''
    OSSUgcRes = OSSTools('ugcres')
    access_token = CommonHelper.access_token
    for i in range(1, 7):
        media_id = request.POST.get('img_url%s' % i)
        if media_id:
            url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (access_token, media_id)
            picname = str_tools.gen_short_uuid()
            OSSUgcRes.upload_from_url(picname, url)
            if piclist:
                piclist = '%s,%s' % (piclist, picname)
            else:
                piclist = picname

    job = Job(uuid=str_tools.gen_uuid(), user_id=user_id, company_name=company_name, job_title=job_title,
        work_experience=work_experience, salary=salary, education=education, city=city, skill=skill, piclist=piclist)
    job.save()

    if is_vip(user_id):
        vip_job = VipJobList(job_id=job.id, user_id=user_id, pub_time=datetime.datetime.now())
        vip_job.save()

    url = "http://" + request.get_host() + request.path
    sign = Helper.jsapi_sign(url)
    sign["appId"] = WxPayConf_pub.APPID
    return render_to_response('job/job_success.html', {"jsapi": json.dumps(sign)})


@sns_userinfo_with_userinfo
def fabu_job(request):
    # todo 从数据库中获取默认值, 需要杨同学把这些值写到页面上, 判断图片是否是上次已经传过, 如果是，则不再重复上传
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    job_detail = Job.objects.filter(user_id=user_id)[:1][0]

    data = {}
    if job_detail:
		data = model_to_dict(job_detail, exclude=['is_vip', 'is_valid', 'update_time', 'create_time'])

    url = "http://" + request.get_host() + request.path
    sign = Helper.jsapi_sign(url)
    sign["appId"] = WxPayConf_pub.APPID

    data['jsapi'] = json.dumps(sign)
    return render_to_response('job/job_fabu.html', data)


@sns_userinfo_with_userinfo
def recommand_job(request):
    return render_to_response('job/job_recommand.html')


@sns_userinfo_with_userinfo
def chat(request):
    return render_to_response('chat/chat.html')
