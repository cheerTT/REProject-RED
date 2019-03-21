# @Time   : 2019年3月9日16:50:29
# @Author : ttwen
# @Remark   : 生成工作台各种统计数据


import calendar
import datetime
from datetime import date, timedelta

from commodity.models import Commodity
from order.models import Transaction
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
    this_year = datetime.datetime.now().year #获取当前年份
    this_month = datetime.datetime.now().month #获取当前月份
    this_month_days = calendar.monthrange(this_year,this_month)[1] #根据年份和月份获取这个月的天数 31

    ret = []
    order_num = 0
    commo_type_num = {}
    for i in range(1,this_month_days+1):
        currentday_profit = 0
        currentday_trans = Transaction.objects.filter(joined_date__startswith=datetime.date(this_year,this_month,i)) #获取当前天数的交易
        for trans in currentday_trans:
            commo_id = trans.commodity_id
            commo_price = Commodity.objects.filter(id=commo_id).first().present_price
            currentday_profit += commo_price

            order_num += 1

        ret.append(round(currentday_profit,2))

    # 顺便统计一下当月新增商品数
    filters = dict()
    start_date = date.today().replace(month=this_month, day=1)
    end_date = start_date + timedelta(this_month_days -1 )
    filters['warrantyDate__range'] = (start_date, end_date)
    new_commo_num = Commodity.objects.filter(**filters).count()

    #统计当月售出商品的各种类的数量
    filters1 = dict()
    filters1['joined_date__range']  = (start_date, end_date)
    commo_list = Transaction.objects.filter(**filters1)
    type_list = []
    type_num_result = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for commo in commo_list:
        single_type = Commodity.objects.filter(id=commo.commodity_id).first().categories_id
        type_list.append(single_type)
    for i in type_list:
        type_num_result[i] += 1
    # print(type_num_result) # {0: 0, 1: 13, 2: 0, 3: 9, 4: 1, 5: 0, 6: 1, 7: 0, 8: 0}

    return ret, order_num, new_commo_num, type_num_result

