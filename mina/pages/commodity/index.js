//index.js
//获取应用实例
var app = getApp();

Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 1,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        p: 1,
        processing: false,
      imagePath: app.globalData.imagePath,

    },
    onLoad: function () {
        var that = this;
        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
        // that.setData({
        //     imagePath:app.globalData.imagePath
        // });
        //
        // console.log("fdshfyuasgfy");
        // console.log(imagePath);

    },
    //每次展示都会调用这个方法
    onShow: function () {
       this.setData({
            p: 1,
            goods: [],
            loadingMoreHidden: true
        });
        this.getType();

    },

    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    listenerSearchInput: function (e) {
        this.setData({
            searchInput: e.detail.value
        });
    },
    toSearch: function (e) {
        this.setData({
            p: 1,
            goods: [],
            loadingMoreHidden: true
        });
        this.getCommodityList();
    },
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        wx.navigateTo({
            url: "/pages/commodity/info?id=" + e.currentTarget.dataset.id
        });
    },
    getType: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/commodity/commodity_type'),
            data: {},
            header: {
                'content-type': 'application/json' // 默认值
            },
            success(res) {
                console.log(res['data'].data);
                that.setData({
                    categories: res['data'].data
                });
                that.getCommodityList();
            },

        });
    },
    typeClick: function (e) {
        this.setData({
            activeCategoryId: e.currentTarget.id
        });
        this.setData({
            loadingMoreHidden: true,
            p: 1,
            goods: []
        });
        this.getCommodityList();
    },
    onReachBottom: function () { //下拉刷新
        var that = this;
        setTimeout(function () {
            that.getCommodityList();
        }, 500);
    },

    getCommodityList: function () {
        var that = this;
        if (that.data.processing) {
            return;
        }

        if (!that.data.loadingMoreHidden) {
            return;
        }

        that.setData({
            processing: true
        });

        wx.request({

            url: app.buildUrl('/commodity/commodity_list'),
            header: app.getRequestHeader(),

            data: {
                commodity_id: that.data.activeCategoryId,
                mix_kw: that.data.searchInput,
                p: that.data.p,
            },
            success: function (res) {
                console.log(res.data.data)
                var goods=res.data.data;
                that.setData({
                    goods: that.data.goods.concat(goods),
                    p: that.data.p + 1,
                    processing: false
                });

                if (res.data.has_more == false) {
                    that.setData({
                        loadingMoreHidden: false
                    });
                }
            }


        });
    }
});
