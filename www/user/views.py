# -*- coding: utf-8 -*-
# from django.db import transaction
from django.template import RequestContext 
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import logging, json
from user.models import Bind, Profile, ProfileExt
from logic.models import Job
from user_tools import sns_userinfo_with_userinfo, get_userid_by_openid
from common import convert, str_tools


@sns_userinfo_with_userinfo
def recommand_list(request):
	return render_to_response('user/recommand_list.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def collection_list(request):
	return render_to_response('user/collection_list.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def fabu_list(request):
	user_id = get_userid_by_openid(request.openid)
	job_from_point = convert.str_to_int(request.GET.get('from', '0'), 0)  # 有from时，则为翻页，无时，则为首页
	number_limit = convert.str_to_int(request.GET.get('limit', '10'), 10)  # 异常情况下，或者不传的情况下，默认为10
	jobs = Job.objects.filter(user_id=user_id).order_by('-id')[job_from_point:number_limit + job_from_point]
	job_list = []
	profile = Profile.objects.filter(id=user_id)[0]
	username = profile.real_name
	portrait = profile.portrait
	for my_job in jobs:
		city = my_job.city+" "+my_job.district
		job = {'city': city, 'company_name': my_job.company_name, 'job_title': my_job.job_title,
		       'education': my_job.education, 'work_experience': my_job.work_experience, 'salary': my_job.salary,
		       'create_time': convert.format_time(my_job.create_time), 'username': username, 'portrait': portrait}
		job_list.append(job)
	if job_from_point == 0:  # 首页，需要返回页面
		return render_to_response('user/fabu_list.html', {'job_list': json.dumps(job_list)}, context_instance=RequestContext(request))
	else:  # 加载下一页，ajax请求
		return HttpResponse(json.dumps(job_list), content_type='application/json')


@sns_userinfo_with_userinfo
def yinping_list(request):
	return render_to_response('user/yinping_list.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def recommand_detail(request):
	return render_to_response('user/recommand_detail.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def collection_detail(request):
	return render_to_response('user/collection_detail.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def fabu_detail(request):
	return render_to_response('user/fabu_detail.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def yingpin_detail(request):
	return render_to_response('chat/chat.html', {}, context_instance=RequestContext(request))


@sns_userinfo_with_userinfo
def edit_userinfo(request):
	user_id = get_userid_by_openid(request.openid)
	profiles = Profile.objects.filter(id=user_id)[:1]
	profile_exts = ProfileExt.objects.filter(user_id=user_id)[:1]
	if not profiles or not profile_exts:
		return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")

	info = {'title': '编辑资料', 'tint': '真实信息，有利于相互信任！'}
	profile = profiles[0]
	info['real_name'] = profile.real_name
	info['company_name'] = profile.company_name
	info['user_title'] = profile.title
	info['desc'] = profile.desc

	profile_ext = profile_exts[0]
	info['city'] = profile_ext.city

	return render_to_response('user/edit_userinfo.html', {'info': json.dumps(info)}, context_instance=RequestContext(request))


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
@sns_userinfo_with_userinfo
def post_userinfo(request):
	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

	company_name = request.POST.get('company_name')
	desc = request.POST.get('jianli')
	title = request.POST.get('title')
	real_name = request.POST.get('real_name')
	city = request.POST.get('city')

	# 更新profile表 ,更新两个表应该用事务，这里暂时放下
	profiles = Profile.objects.filter(id=user_id)[:1]
	if not profiles:
		return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")

	profile = profiles[0]
	profile.real_name = real_name
	profile.company_name = company_name
	profile.title = title
	profile.desc = desc
	profile.save()

	# 更新profile_ext表
	profile_exts = ProfileExt.objects.filter(user_id=user_id)[:1]
	if profile_exts:
		profile_ext = profile_exts[0]
		profile_ext.city = city
		profile_ext.save()
	return HttpResponseRedirect('/user/me')

@sns_userinfo_with_userinfo
def me(request):
	user_id = get_userid_by_openid(request.openid)
	if not user_id:
		logging.error('Cant find user_id by openid: %s when post_job' % request.openid)
		return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

	profiles = Profile.objects.filter(id=user_id)[:1]
	if not profiles:
		return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")

	profile = profiles[0]
	if profile.real_name == '':
		info = {'title': '完善资料', 'tint': '请先完善您的资料吧！'}
		return render_to_response('user/edit_userinfo.html', {'info': json.dumps(info)})
	profile_exts = ProfileExt.objects.filter(user_id=user_id)[:1]
	if not profile_exts:
		return HttpResponse("十分抱歉，获取用户信息失败，请联系客服人员")
	profile_ext = profile_exts[0]
	user_city = profile_ext.city.split(' ')[1]
	user = {'nick': profile.real_name, 'portrait': profile.portrait, 'user_company': profile.company_name,
	        'user_title': profile.title, 'user_city': user_city, 'user_desc': profile.desc}
	return render_to_response('user/me.html', {'user': json.dumps(user)}, context_instance=RequestContext(request))

