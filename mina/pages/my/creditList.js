var app = getApp()

Page({
    data: {
        userid: null,
        creditlist: null,
        totalpoints: 0,
        integralPage: 0, // 控制是否展开 0:显示主页 1:显示积分规则页
        // 积分规则
        integralRule: {
        convertNum: 100, // 100积分对应1元
        consumeNum: 1, // 消费1元积累1积分
        loginNum: 2, // 每天登录送2积分
        postCommentNum: 2, // 对于购买过的商品评论送2积分
        shareNum: 3, // 每天首次分享商品给好友送3积分
      },
    },

    onLoad: function (options) {
        // 生命周期函数--监听页面加载
        var that = this;
        var userid = options.userid;

        this.setData({
            userid: options.userid,
        })
        wx.getStorage({
            key: 'userid',
            success: function (res) {
                //console.log("res.data:",res.data)
            },
        })
    },
    onReady: function () {
        // 生命周期函数--监听页面初次渲染完
    },
    onShow: function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/member/credit_list?userid=" + this.data.userid),
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data
                var totalpoints = 0
                for (var i = 0; i < resp.data.length; i++) {
                    var ai = resp.data[i];
                    if (ai.credittype == '0') {
                        totalpoints += parseInt(ai.creditpoints)
                        ai.creditpoints = "+" + ai.creditpoints
                    } else {
                        totalpoints -= parseInt(ai.creditpoints)
                        ai.creditpoints = "-" + ai.creditpoints
                    }
                    if (ai.behave == '0') {
                        ai.behave = "每日首次登录送积分"
                    } else if (ai.behave == '1') {
                        ai.behave = '消费送积分'
                    } else if (ai.behave == '2') {
                        ai.behave = '每日首次分享送积分'
                    } else if (ai.behave == '3') {
                        ai.behave = '发表评论送积分'
                    } else if (ai.behave == '4') {
                        ai.behave = '消费抵扣积分'
                    }
                    ai.createtime = ai.createtime.substr(0, [19]) //截取时间
                }
                that.setData({
                    creditlist: resp,
                    totalpoints: totalpoints
                })
            }
        })
    },

    // 积分规则：打开积分详情
    showIntegralRule: function () {
        this.setData({
            'integralPage': 1
        });
    },
    // 积分规则：关闭积分详情(返回:个人积分主页)
    hideIntegralRule: function () {
        this.setData({
            'integralPage': 0
        });
    }
})