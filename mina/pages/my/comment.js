//获取应用实例
var app = getApp();
Page({
    data: {
        content:"很好，你已经引起了我的注意~~",
        score:5,
        order_sn:"",
        id: 0,
    },
    onLoad: function (e) {
         var that = this;
        that.setData({
            id: e.id
        });
    },

    scoreChange:function( e ){
        this.setData({
            score:e.detail.value
        });
    },
    contentChange:function( e ){
        this.setData({
            content:e.detail.value
        });
    },
    doComment:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/commodity/comment_add"),
            header: app.getRequestHeader(),
            data: {
                id: that.data.id,
                score:that.data.score,
                content:that.data.content
            },
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