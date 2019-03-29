//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');
var utils = require('../../utils/util.js');
Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        good: {},
        shopType: "addShopCar",
        id: 0,
        shopCarNum: 4,
        commentCount: 2,
        imagePath: app.globalData.imagePath,
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            id: e.id
        });
        console.log(e.id)
    },
    onShow: function () {
        this.getInfo();
        this.getComments();
    },
    goShopCar: function () {
        wx.navigateTo({
            url: "/pages/cart/index"
        });
    },
    addShopCar: function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/commodity/cart_add"),
            header: app.getRequestHeader(),
            method: 'GET',
            data: {
                id: that.data.id
            },
            success: function (res) {

                var resp = res.data.msg;

                wx.showToast({
                    title: resp,
                    duration: 1000,
                    mask: true
                })

            }
        });
    },

    getInfo: function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/commodity/commodity_info"),
            header: app.getRequestHeader(),
            data: {
                id: that.data.id
            },
            success: function (res) {
                var resp = res.data;
                that.setData({
                    good: resp.data[0],
                });
            }
        });
    },

    getComments: function () {
        var that = this;
        console.log(that.data.id)
        wx.request({
            url: app.buildUrl("/commodity/commodity_comments"),
            header: app.getRequestHeader(),
            data: {
                id: that.data.id
            },
            success: function (res) {
                var resp = res.data;
                that.setData({
                    commentList: resp.data,
                    commentCount: resp.data.length,
                });
            }
        });
    },

    onShareAppMessage: function () {
        var that = this;
        console.log("分享")
        return {
            title: that.data.good.title,
            path: '/pages/commodity/info?id=' + that.data.good.id,
            success: function (res) {
                //转发成功
                wx.request({
                    url: app.buildUrl("/member/credit_share"),
                    header: app.getRequestHeader(),
                    method: 'POST',
                    data: {
                        url: utils.getCurrentPageUrlWithArgs(),
                        'csrfmiddlewaretoken': '{{ csrf_token }}'
                    },
                    success: function (res) {
                        console.log(res.data)
                    }
                });
            },
            fail: function (res) {
                // 转发失败
            }
        }
    }

});
