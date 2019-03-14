//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {},
    regFlag: true,
    codeVerify: ''
  },
  goToIndex:function(){
    wx.switchTab({
      url: '/pages/commodity/index',
    });
  },
  onLoad:function(){
    wx.setNavigationBarTitle({
      title: app.globalData.shopName
    });
    this.checkLogin();
    //this.login();
  },
  onShow:function(){

  },
  onReady: function(){
    var that = this;
    setTimeout(function(){
      that.setData({
        remind: ''
      });
    }, 1000);
    wx.onAccelerometerChange(function(res) {
      var angle = -(res.x*30).toFixed(1);
      if(angle>14){ angle=14; }
      else if(angle<-14){ angle=-14; }
      if(that.data.angle !== angle){
        that.setData({
          angle: angle
        });
      }
    });
  },
  listenerCodeInput: function (e) {
    this.setData({
      codeVerify: e.detail.value
    });
  },
  checkLogin: function(){
      
      var that = this;
      wx.login({
          success: function (res) {
            if (!res.code) {
                app.alert({'content': '登陆失败，请再次点击' });
                return;
            }
            console.log('checkLogin')
            console.log(that.data.codeVerify)
            wx.request({
              url: app.buildUrl('/member/checkreg'),
              header: app.getRequestHeader(),
              method: 'POST',

              data: {'code': res.code, 'codeVerify': that.data.codeVerify},
                success: function (res) {
                  if (res.data.code != 200) {
                      that.setData({
                          regFlag: false
                      });
                      return;
                  }
                  app.setCache("token", res.data.data.token);
                  that.goToIndex();
                }
              });
          }
      });
  },
  login: function(e){
    var that = this;
    if (!e.detail.userInfo) {
        app.alert({'content': '登陆失败，请再次点击'});
        return;
    }
    var data = e.detail.userInfo;
    wx.login({
        success: function(res) {
          if (!res.code) {
              app.alert({'content': '登陆失败，请再次点击'});
              return;
          }
          data['code'] = res.code;
          data['codeVerify'] = that.data.codeVerify;
          wx.request({
              url: app.buildUrl('/member/login'),
              header: app.getRequestHeader(),
              method: 'POST',
              data: data,
              success: function (res) {
                if (res.data.code != 200) {
                    app.alert({'content': res.data.msg});
                    return;
                }
                app.setCache("token", res.data.data.token);
                that.goToIndex();
              }
          });
        }
    })


      
  }
});