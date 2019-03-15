// pages/hotcommend/hotcommend.js
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
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        p: 1,
        processing: false,
        imagePath: ''
    },
    //页面加载时触发。一个页面只会调用一次
    onLoad: function () {
        var that = this;
        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
        that.setData({
            // p: 1,
            goods:[],
            categories:[
                {id: 0, name:"爆款！！"},
                {id: 1, name:"进来康康"},
            ],
            activeCategoriesId:0,
            imagePath: app.globalData.imagePath,
        });
    },
    //解决切换不刷新，每次展示都会调用这个方法,页面显示/切入前台时触发
    onShow: function () {
        // this.getType();
        this.setData({
            p: 1,
            goods: [],
            loadingMoreHidden: true
        });
        this.getHotCommodityList();

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
    typeClick: function (e) {
        this.setData({
            loadingMoreHidden: true,
            goods:[],
            activeCategoryId: e.currentTarget.id,
            p:1
        });
        if (e.currentTarget.id == 0)
        {this.getHotCommodityList();}
    },
    onReachBottom: function () { //下拉刷新
        var that = this;
        setTimeout(function () {
            that.getHotCommodityList();
        }, 500);
    },

    getHotCommodityList: function () {
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

            url: app.buildUrl('/hotcommend/hot_commodity'),
            header: app.getRequestHeader(),

            data: {
                p: that.data.p,
            },
            success: function (res) {
                console.log(res.data.data);
                var goods=res.data.data;
                that.setData({
                    goods: that.data.goods.concat(goods),    //下拉增加商品
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