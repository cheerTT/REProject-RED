var app = getApp();
Page({
    data: {
      userid : null,
      orderlist : null,
    },
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
            //按照订单号分组
            var map = {},
              dest = [];
            for (var i = 0; i < resp.length; i++) {
              var ai = resp[i];
              if (!map[ai.orderid]) { 
                var orderprice = 0;
                dest.push({
                  id: ai.orderid, 
                  orderprice: ai.presentprice,
                  data: [ai],
                });
                map[ai.orderid] = ai; 
              } else {
                for (var j = 0; j < dest.length; j++) {
                  var dj = dest[j];
                  var orderprice = null; 
                  if (dj.id == ai.orderid) { 
                      dj.orderprice += parseFloat(ai.presentprice)*parseInt(ai.num)
                      //保留两位小数
                      dj.orderprice = Math.round(dj.orderprice*100)/100 
                    dj.data.push(ai);
                    break;
                  }
                }
              }
            }
            
            that.setData({
              orderlist:dest
            })
          }

        })
    },
    toDetailsTap: function (e) {
      console.log("shangpingid:", e.currentTarget.dataset.id)
      wx.navigateTo({
        url: "/pages/commodity/info?id=" + e.currentTarget.dataset.id
      });
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
