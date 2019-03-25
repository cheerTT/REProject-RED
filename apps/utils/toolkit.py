'''生成工作台各种统计数据'''
# @Time   : 2019年3月9日16:50:29
# @Author : ttwen
# @Remark   : 生成工作台各种统计数据


import calendar
import datetime
from datetime import date, timedelta
from commodity.models import Commodity
from order.models import Transaction
from api.models import Member

def get_month_member_count():
    """生成月度用户统计"""
    months = range(1, 13)
    filters = dict()
    month_member_count = []

    count = []
    for month in months:
        start_date = date.today().replace(month=month, day=1)
        _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
        end_date = start_date + timedelta(days_in_month -1)
        filters['joined_date2__range'] = (start_date, end_date)
        month_member = Member.objects.filter(**filters).count()
        count.append(month_member)
    data = {
        'count': count
    }
    month_member_count.append(data)
    return month_member_count

def  get_member_gender():
    '''生成用户性别数据'''
    filters = dict()
    member_gender = []

    count = []
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

def get_monthly_sale_count():
    """生成当月销售数据统计"""
    this_year = datetime.datetime.now().year #获取当前年份
    this_month = datetime.datetime.now().month #获取当前月份
    this_month_days = calendar.monthrange(this_year, this_month)[1] #根据年份和月份获取这个月的天数 31

    ret = []
    order_num = 0
    for i in range(1, this_month_days+1):
        currentday_profit = 0
        currentday_trans = Transaction.objects.filter(joined_date__startswith=datetime.date(this_year, this_month, i)) #获取当前天数的交易
        for trans in currentday_trans:
            commo_id = trans.commodity_id
            commo_price = Commodity.objects.filter(id=commo_id).first().present_price
            currentday_profit += commo_price
            order_num += 1
        ret.append(round(currentday_profit, 2))

    # 顺便统计一下当月新增商品数
    filters = dict()
    start_date = date.today().replace(month=this_month, day=1)
    end_date = start_date + timedelta(this_month_days -1)
    filters['warrantyDate__range'] = (start_date, end_date)
    new_commo_num = Commodity.objects.filter(**filters).count()

    #统计当月售出商品的各种类的数量
    filters1 = dict()
    filters1['joined_date__range'] = (start_date, end_date)
    commo_list = Transaction.objects.filter(**filters1)
    type_list = []
    type_num_result = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    for commo in commo_list:
        single_type = Commodity.objects.filter(id=commo.commodity_id).first().categories_id
        type_list.append(single_type)
    for i in type_list:
        type_num_result[i] += 1

    # 统计全年12个月份8种类商品的销量
    commo_num_array = [[0 for i in range(12)] for i in range(8)]
    fields = ['num', 'joined_date', 'commodity_id', 'commodity_id__categories_id']
    filters = dict()
    commo_list_year = Transaction.objects.filter(**filters).values(*fields)  #今年所有的商品
    for commo in commo_list_year:
        # 种类为commo_type的在commo_month的有commo_num个
        commo_type = int(commo['commodity_id__categories_id'])
        commo_month = int(commo['joined_date'].month)
        commo_num = int(commo['num'])
        commo_num_array[commo_type-1][commo_month-1] += commo_num
    return ret, order_num, new_commo_num, type_num_result, commo_num_array