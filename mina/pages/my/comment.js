//获取应用实例
var app = getApp();
Page({
    data: {
        "content":"非常愉快的订餐体验~~",
        "score":10,
        "order_sn":"",
        id: 0,
    },
    onLoad: function (e) {

    },
    scoreChange:function( e ){
        this.setData({
            "score":e.detail.value
        });
    },
    doComment:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/commodity/comment_add"),
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                that.setData({
                   user_info:resp.data.info
                });
            }
        });
    }
});