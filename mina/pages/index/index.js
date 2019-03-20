//login.js
//获取应用实例
var app = getApp();
Page({
  data: {
    remind: '加载中',
    angle: 0,
    userInfo: {},
    regFlag: true,
    codeVerify: '',
    bol: false
  },
  goToIndex:function(){
    wx.switchTab({
      url: '/pages/recommendations/index',
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
  // changeName: function(e) {
  //   app.alert({'content': '请输入验证码'});
  // },
  show: function() {
    this.setData({
      bol:true
    })
  },
  checkLogin: function(){
      var that = this;
      var app = getApp();
      wx.login({
          success: function (res) {
            if (!res.code) {
                app.alert({'content': '登陆失败，请再次点击' });
                return;
            }
            console.log('checkLogin')
            console.log('11' + that.data.codeVerify)
            wx.request({
              url: app.buildUrl('/member/checkreg'),
              header: app.getRequestHeader(),
              method: 'POST',

              data: {'code': res.code, 'codeVerify': that.data.codeVerify},
                success: function (res) {
                  console.log(res.data)
                  if (res.data.code != 200) {
                    console.log('regflag = false');
                    
                    app.alert({'content': '您还不是会员，赶快到店里获取会员码吧！'})
                    that.setData({
                      
                      regFlag: false
                    });
                    return;
                  }
                  console.log(app.globalData.user_id)
                  getApp().globalData.user_id =  res.data.user_id
                  console.log(getApp().globalData.user_id)
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