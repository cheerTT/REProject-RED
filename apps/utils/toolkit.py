# @Time   : 2019年3月9日16:50:29
# @Author : ttwen
# @Remark   : 生成工作台各种统计数据


import calendar
from datetime import date, timedelta

from django.core.mail import send_mail

from personal.models import WorkOrder
from reporjectred.settings import EMAIL_FROM
from api.models import Member

def get_month_member_count(value=0):
    """
    生成月度用户统计
    """

    months = range(1, 13)
    filters = dict()
    month_member_count = []

    count = []
    for month in months:
        start_date = date.today().replace(month=month, day=1)
        # print("start_date = ",start_date)
        _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
        end_date = start_date + timedelta(days_in_month -1 )
        # print("end_date", end_date)
        filters['joined_date2__range'] = (start_date, end_date)
        month_member = Member.objects.filter(**filters).count()
        count.append(month_member)
    data = {
        'count': count
    }
    # print("data = ",data)
    month_member_count.append(data)
    return month_member_count

def  get_member_gender(value=0):
    '''
    生成用户性别数据
    '''
    filters = dict()
    member_gender = []

    count = []
    # start_date = date.today().replace(month=month, day=1)
    # _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    # end_date = start_date + timedelta(days_in_month - 1)
    filters['gender'] = '1'
    member_gender1 = Member.objects.filter(**filters).count()
    count.append(member_gender1)

    filters['gender'] = '2'
    member_gender2 = Member.objects.filter(**filters).count()
    count.append(member_gender2)
    data = {
        'count': count
    }
    member_gender.append(data)
    return member_gender

def get_monthly_sale_count(value=0):
    """
    生成当月销售数据统计
    """

    print("这个月的天数：",calendar.monthrange(2019,3)[1])
    # filters = dict()
    # year_work_order_count = []
    # for user in users:
    #     start_year = date.today().replace(month=1, day=1)
    #     end_year = date.today().replace(year=(start_year.year + 1), month=1, day=1)
    #     filters['add_time__range'] = (start_year, end_year)
    #     if value == 0:
    #         filters['proposer_id'] = user['id']
    #     else:
    #         filters['receiver_id'] = user['id']
    #     year_work_order = WorkOrder.objects.filter(**filters).count()
    #     data = {
    #         'name': user['name'],
    #         'count': year_work_order
    #     }
    #     year_work_order_count.append(data)
    #
    # return year_work_order_count


