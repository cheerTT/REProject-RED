var app = getApp();
Page({
    data: {
      userid : null,
      orderlist : null,

      imagePath: app.globalData.imagePath,

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
        this.setData({
          userid:options.userid
        })
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

    toDetailsTap: function (e) {
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
