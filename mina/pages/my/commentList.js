var app = getApp();
Page({
    data: {
        commentList: [],
        userid: null,

    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载
        var that = this;
        var userid = options.userid;
        this.setData({
            userid: options.userid
        });
    },
    onShow: function () {
        var that = this;
    }
});
