//获取应用实例
var app = getApp();
Page({
    data: {
        content: "~~",
        score: 5,
        order_sn: "",
        id: 0,
        userid: null,
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            id: e.id,
            userid: e.userid
        });


    },

    scoreChange: function (e) {
        this.setData({
            score: e.detail.value
        });
    },
    contentChange: function (e) {
        this.setData({
            content: e.detail.value
        });
    },
    doComment: function () {
        var that = this;

        wx.request({
            url: app.buildUrl("/commodity/comment_add"),
            header: app.getRequestHeader(),
            data: {
                id: that.data.id,
                score: that.data.score,
                content: that.data.content
            },
            success: function (res) {
                var resp = res.data;
                // app.alert({"content": resp});
                setTimeout(function(){
                   wx.showToast({
                    title: resp.msg,
                    duration: 1000,
                    mask: true
                    });
                },1000);

                wx.navigateBack();


            }
        });
    }
});