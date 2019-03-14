var app = getApp();
Page({
    data: {
      userid : null,
      orderlist : null,
        // statusType: ["待付款", "待发货", "待收货", "待评价", "已完成","已关闭"],
        // status:[ "-8","-7","-6","-5","1","0" ],
        // currentType: 0,
        // tabClass: ["", "", "", "", "", ""]
    },
    // statusTap: function (e) {
    //     var curType = e.currentTarget.dataset.index;
    //     this.data.currentType = curType;
    //     this.setData({
    //         currentType: curType
    //     });
    //     this.onShow();
    // },
    orderDetail: function (e) {
        wx.navigateTo({
            url: "/pages/my/order_info"
        })
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载
        var that = this;
        var userid = options.userid
        // console.log("options:",options.userid) //43
        this.setData({
          userid:options.userid
        })
        // console.log("userid:",userid)
        wx.getStorage({
          key: 'userid',
          success: function(res) {
            // console.log("res.data:",res.data)
          },
        })

    },
    onReady: function () {
        // 生命周期函数--监听页面初次渲染完
    },
    onShow: function () {
        var that = this;
        wx.request({
          url: app.buildUrl("/member/order?userid="+this.data.userid),
          header: app.getRequestHeader(),
          success: function (res) {
            var resp = res.data
            console.log("resp",resp)
            var map = {},
              dest = [];
            for (var i = 0; i < resp.length; i++) {
              var ai = resp[i];
              if (!map[ai.orderid]) { 
                dest.push({
                  id: ai.orderid, 
                  data: [ai]
                });
                map[ai.orderid] = ai; 
              } else {
                for (var j = 0; j < dest.length; j++) {
                  var dj = dest[j];
                  if (dj.id == ai.orderid) { 
                    dj.data.push(ai);
                    break;
                  }
                }
              }
            }
            console.log(dest);
            
            that.setData({
              orderlist:dest
            })
          }

        })
    },
    onHide: function () {
        // 生命周期函数--监听页面隐藏

    },
    onUnload: function () {
        // 生命周期函数--监听页面卸载

    },
    onPullDownRefresh: function () {
        // 页面相关事件处理函数--监听用户下拉动作

    },
    onReachBottom: function () {
        // 页面上拉触底事件的处理函数

    }
})
