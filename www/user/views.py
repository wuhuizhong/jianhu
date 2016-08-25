# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import logging, json
from user.models import Bind, Profile, ProfileExt
from logic.models import Job
from user_tools import sns_userinfo_with_userinfo, get_userid_by_openid, get_user_profile_by_user_id
from common import convert, str_tools


@sns_userinfo_with_userinfo
def recommand_list(request):
    template = get_template('user/recommand_list.html')
    return HttpResponse(template.render({}, request))


@sns_userinfo_with_userinfo
def collection_list(request):
    template = get_template('user/collection_list.html')
    return HttpResponse(template.render({}, request))


@sns_userinfo_with_userinfo
def fabu_list(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    profile = get_user_profile_by_user_id(user_id=user_id, need_default=False)
    if not profile:
        logging.error('Cant find user profile by user_id: %s when fabu_list' % user_id)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    job_from_point = convert.str_to_int(request.GET.get('from', '0'), 0)  # 有from时，则为翻页，无时，则为首页
    number_limit = convert.str_to_int(request.GET.get('limit', '10'), 10)  # 异常情况下，或者不传的情况下，默认为10
    jobs = Job.objects.filter(user_id=user_id).order_by('-id')[job_from_point:number_limit + job_from_point]

    job_list = []
    for my_job in jobs:
        city = my_job.city + " " + my_job.district
        job = {'city': city, 'company_name': my_job.company_name, 'job_title': my_job.job_title,
               'education': my_job.education, 'work_experience': my_job.work_experience, 'salary': my_job.salary,
               'create_time': convert.format_time(my_job.create_time), 'username': profile.real_name, 'portrait': profile.portrait}
        job_list.append(job)

    if job_from_point == 0:  # 首页，需要返回页面
        template = get_template('user/fabu_list.html')
        return HttpResponse(template.render({'job_list': json.dumps(job_list)}, request))
    else:  # 加载下一页，ajax请求
        return HttpResponse(json.dumps(job_list), content_type='application/json')


@sns_userinfo_with_userinfo
def yinping_list(request):
    template = get_template('user/yinping_list.html')
    return HttpResponse(template.render({}, request))


@sns_userinfo_with_userinfo
def recommand_detail(request):
    template = get_template('user/recommand_detail.html')
    return HttpResponse(template.render({}, request))


@sns_userinfo_with_userinfo
def collection_detail(request):
    template = get_template('user/collection_detail.html')
    return HttpResponse(template.render({}, request))


@sns_userinfo_with_userinfo
def fabu_detail(request):
    template = get_template('user/fabu_detail.html')
    return HttpResponse(template.render({}, request))


@sns_userinfo_with_userinfo
def yingpin_detail(request):
    template = get_template('chat/chat.html')
    return HttpResponse(template.render({}, request))


@sns_userinfo_with_userinfo
def edit_userinfo(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    profile = get_user_profile_by_user_id(user_id=user_id, need_default=False)
    if not profile:
        logging.error('Cant find user profile by user_id: %s when edit_userinfo' % user_id)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    info = {'title': '编辑资料', 'tint': '真实信息，有利于相互信任！'}
    info['real_name'] = profile.real_name
    info['company_name'] = profile.company_name
    info['user_title'] = profile.title
    info['desc'] = profile.desc
    info['city'] = profile.city

    template = get_template('user/edit_userinfo.html')
    return HttpResponse(template.render({'info': json.dumps(info)}, request))


@sns_userinfo_with_userinfo
def post_userinfo(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    profile = get_user_profile_by_user_id(user_id=user_id, need_default=False)
    if not profile:
        logging.error('Cant find user profile by user_id: %s when post_userinfo' % user_id)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    profile.real_name = request.POST.get('real_name')
    profile.company_name = request.POST.get('company_name')
    profile.title = request.POST.get('title')
    profile.desc = request.POST.get('jianli')
    profile.city = request.POST.get('city')
    profile.save()

    return HttpResponseRedirect('/user/me')


@sns_userinfo_with_userinfo
def me(request):
    user_id = get_userid_by_openid(request.openid)
    if not user_id:
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")

    profile = get_user_profile_by_user_id(user_id=user_id, need_default=False)
    if not profile:
        logging.error('Cant find user profile by user_id: %s when me' % user_id)
        return HttpResponse("十分抱歉，获取用户信息失败，请重试。重试失败请联系客服人员")
    
    if profile.real_name == '':
        info = {'title': '完善资料', 'tint': '请先完善您的资料吧！'}
        template = get_template('user/edit_userinfo.html')
        return HttpResponse(template.render({'info': json.dumps(info)}, request))

    user = {'nick': profile.real_name, 'portrait': profile.portrait, 'user_company': profile.company_name,
            'user_title': profile.title, 'user_city': profile.city, 'user_desc': profile.desc}

    template = get_template('user/me.html')
    return HttpResponse(template.render({'user': json.dumps(user)}, request))

