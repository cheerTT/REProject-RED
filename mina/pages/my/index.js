//获取应用实例
var app = getApp();
Page({
    data: {
      user_info:null
    },
    onLoad() {

    },
    onShow() {
      this.getInfo();
    },
    getInfo:function() {
      var that = this;
      wx.request({
        url: app.buildUrl("/member/info"),
        header: app.getRequestHeader(),
        success: function (res) {
          var resp = res.data;
          that.setData({
            userInfo: resp
          });
          
        }
      });
    }
});