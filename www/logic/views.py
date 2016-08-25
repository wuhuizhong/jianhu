# -*- coding: utf-8 -*-

import json
import logging
import datetime
from django.template import RequestContext 
from django.template.loader import get_template
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from common.oss_tools import OSSTools
from common import convert, str_tools
from wx_base.backends.common import CommonHelper
from wx_base.backends.dj import Helper
from wx_base import WxPayConf_pub
from user.user_tools import sns_userinfo_with_userinfo, get_userid_by_openid, is_vip, get_user_profile_by_user_id
from user.models import Bind, Profile, ProfileExt
from models import Job, VipJobList

@sns_userinfo_with_userinfo
def index(request):
	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

	vip_job_from_point = convert.str_to_int(request.GET.get('from', '0'), 0)  # 有from时，则为翻页，无时，则为首页
	number_limit = convert.str_to_int(request.GET.get('limit', '10'), 10)  # 异常情况下，或者不传的情况下，默认为10
	own_job = {}
	user_info_map = {}
	# 取本人发布过的，并且有效的简历
	if vip_job_from_point != 0:  # 不是首页的话，翻页不需要继续找own_jobs了
		own_job = []
	else:  # 首页
		own_jobs = Job.objects.filter(user_id=user_id).order_by('-id')[:1]
		if len(own_jobs) == 1:  # 自己发过职位
			own_job = model_to_dict(own_jobs[0],
				exclude=['id', 'user_id', 'is_valid', 'create_time', 'update_time', 'city', 'province', 'district',
				         'piclist', 'skill', ])
			own_job['city'] = own_jobs[0].city + " " + own_jobs[0].district
			own_job['create_time'] = convert.format_time(own_jobs[0].create_time)
			profile = Profile.objects.filter(id=user_id)[0]
			own_job['username'] = profile.real_name
			own_job['portrait'] = profile.portrait

			userinfo = {}
			userinfo['nick'] = own_job['username']
			userinfo['portrait'] = own_job['portrait']
			userinfo['user_company'] = profile.company_name
			userinfo['user_title'] = profile.title
			userinfo['user_desc'] = profile.desc

			profile_exts = ProfileExt.objects.filter(user_id=user_id)[:1]
			if not profile_exts:
				return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")
			profile_ext = profile_exts[0]
                        citys = profile_ext.city.split(' ')
                        if len(citys) > 1:
                            userinfo['user_city'] = citys[1]
                        else:
                            userinfo['user_city'] = profile_ext.city
			user_info_map[own_job['uuid']] = userinfo


	# 按发布时间去取VIP发布简历 －－ 以后从缓存中取
	vip_jobs = VipJobList.objects.all().order_by('-pub_time')[vip_job_from_point:number_limit + vip_job_from_point]
	job_id_list = [job.job_id for job in vip_jobs]
	vip_jobs = Job.objects.filter(id__in=job_id_list)
	job_list = []
	for my_job in vip_jobs:
		profile = Profile.objects.filter(id=my_job.user_id)[0]
		username = profile.real_name
		portrait = profile.portrait
		city = my_job.city + " " + my_job.district
		job = {'city': city, 'company_name': my_job.company_name, 'job_title': my_job.job_title,
		       'education': my_job.education, 'work_experience': my_job.work_experience, 'salary': my_job.salary,
		       'create_time': convert.format_time(my_job.create_time), 'username': username, 'portrait': portrait,
		       'job_uuid': my_job.uuid}

		userinfo = {}
		userinfo['nick'] = profile.real_name
		userinfo['portrait'] = portrait
		userinfo['user_company'] = profile.company_name
		userinfo['user_title'] = profile.title
		userinfo['user_desc'] = profile.desc

		profile_exts = ProfileExt.objects.filter(user_id=user_id)[:1]
		if not profile_exts:
			return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")
		profile_ext = profile_exts[0]
                citys = profile_ext.city.split(' ')	
                if len(citys) > 1:
                    userinfo['user_city'] = citys[1]
                else:
                    userinfo['user_city'] = profile_ext.city
		user_info_map[my_job.uuid] = userinfo

		job_list.append(job)
	job_list.reverse()
	page_data = {'own_job': json.dumps(own_job), 'job_list': json.dumps(job_list),
	             'user_info_map': json.dumps(user_info_map)}

	# 请把own_jobs和vip_jobs渲染到页面上
	if vip_job_from_point == 0:  # 首页，需要返回页面
                template = get_template('index.html')
                return HttpResponse(template.render(page_data, request))
		#return render_to_response('index.html', page_data, context_instance=RequestContext(request))
	else:  # 加载下一页，ajax请求
		return HttpResponse(json.dumps(job_list), content_type='application/json')


@sns_userinfo_with_userinfo
def msg(request):
	return render_to_response('chat/mesg.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def get_job(request):
	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

	page_data = {}
	job_uuid = request.GET.get('job_uuid', '')
	job_details = Job.objects.filter(uuid=job_uuid)[:1]
	if job_details:
		page_data = model_to_dict(job_details[0], exclude=['id', 'user_id', 'is_valid', 'create_time', 'update_time', ])
		page_data['time'] = convert.format_time(job_details[0].create_time)
		page_data['city'] = job_details[0].city + " " + job_details[0].district
		profile = get_user_profile_by_user_id(user_id=job_details[0].user_id, need_default=True)
		page_data['username'] = profile.real_name
		page_data['portrait'] = profile.portrait
		page_data['user_title'] = profile.title
		page_data['user_company'] = profile.company_name

		page_data['nick'] = profile.real_name
		page_data['portrait'] = profile.portrait
		page_data['user_company'] = profile.company_name
		page_data['user_title'] = profile.title
		page_data['user_desc'] = profile.desc

		profile_exts = ProfileExt.objects.filter(user_id=user_id)[:1]
		if not profile_exts:
			return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")
		profile_ext = profile_exts[0]
                citys = profile_ext.city.split(' ')
                if len(citys) > 1:
                    page_data['user_city'] = citys[1]
                else:
                    page_data['user_city'] = profile_ext.city
	else:
		logging.error("uid(%s) try to get not exsit job(%s), maybe attack" % (user_id, job_uuid))
		return HttpResponse("十分抱歉，获取职位信息失败，请重试。重试失败请联系客服人员")

	url = "http://" + request.get_host() +request.get_full_path()
	sign = Helper.jsapi_sign(url)
	sign["appId"] = WxPayConf_pub.APPID
	page_data['jsapi'] = json.dumps(sign)

	return render_to_response('job/job_detail.html', page_data, context_instance=RequestContext(request))


# 暂时规避跨站攻击保护
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
	addrs = request.POST.get('city').split(' ')
	province = addrs[0]
	city = addrs[1]
	district = ''
	if len(addrs) == 3:  # 防止有些地方没有区，数组越界异常
		district = addrs[2]

	if not (company_name and job_title and work_experience and salary and education and addrs):
		return HttpResponse("十分抱歉，你输入的参数缺失，请检查确认后重试。重试失败请联系客服人员")

	skills = ""
	for i in range(1, 7):
		skill = request.POST.get('skill%s' % i)
		if skill != "":
			skills += skill + ","
	skills = skills[:-1]

	piclist = ''
	OSSUgcRes = OSSTools('ugcres')
	access_token = CommonHelper.access_token
	for i in range(1, 7):
		media_id = request.POST.get('img_url%s' % i)
		if media_id:
			url = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (
			access_token, media_id)
			picname = str_tools.gen_short_uuid() + ".jpg"
			OSSUgcRes.upload_from_url(picname, url)
			if piclist:
				piclist = '%s,%s' % (piclist, picname)
			else:
				piclist = picname

	job = Job(uuid=str_tools.gen_uuid(), user_id=user_id, company_name=company_name, job_title=job_title,
		work_experience=work_experience, salary=salary, education=education, province=province, city=city,
		district=district, skill=skills, piclist=piclist)
	job.save()

	if is_vip(user_id):
		vip_job = VipJobList(job_id=job.id, user_id=user_id, pub_time=datetime.datetime.now())
		vip_job.save()

	url = "http://" + request.get_host() + request.path
	sign = Helper.jsapi_sign(url)
	sign["appId"] = WxPayConf_pub.APPID

	page_data = {}
	page_data = model_to_dict(job, exclude=['id', 'user_id', 'is_valid', 'create_time', 'update_time', ])
	page_data['time'] = convert.format_time(job.create_time)
	page_data['city'] = job.city + " " + job.district
	profile = Profile.objects.filter(id=job.user_id)[0]
	page_data['username'] = profile.real_name
	page_data['portrait'] = profile.portrait
	page_data['user_title'] = profile.title
	page_data['user_company'] = profile.company_name
	page_data['jsapi'] = json.dumps(sign)

	page_data['post_success'] = 1
	return render_to_response('job/job_detail.html', page_data, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def fabu_job(request):
	# todo 从数据库中获取默认值, 需要杨同学把这些值写到页面上, 判断图片是否是上次已经传过, 如果是，则不再重复上传
	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

	# job_details = Job.objects.filter(user_id=user_id)[:1]
	# if not job_details:
	# 	return HttpResponse("十分抱歉，获取失败,请联系客服人员")
	#
	# job_detail = job_details[0]

	page_data = {}
	# if job_detail:
	# 	page_data = model_to_dict(job_detail, exclude=['is_vip', 'is_valid', 'update_time', 'create_time'])

	url = "http://" + request.get_host() + request.path
	sign = Helper.jsapi_sign(url)
	sign["appId"] = WxPayConf_pub.APPID

	page_data['jsapi'] = json.dumps(sign)
	return render_to_response('job/job_fabu.html', page_data, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def recommand_job(request):
	return render_to_response('job/job_recommand.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def chat(request):
	return render_to_response('chat/chat.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def get_job_luyin(request):
	return render_to_response('job/job_detail_luyin.html', {}, context_instance=RequestContext(request))
