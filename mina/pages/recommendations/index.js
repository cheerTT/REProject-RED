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
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        arpages:0,
        toprecommendations :[],
        allrecommendations :[],
        imagePath : app.globalData.imagePath,
        processing: false,
    },
    onLoad: function () {
        var that = this;

        wx.request({
          url: app.buildUrl('/recommendations/toprecommendations'),
          header: app.getRequestHeader(),
          method: 'get',
          data: {
          },
          success: function (res) {
            console.log(res.data.data),
            that.setData({
              toprecommendations: res.data.data
            }
            )
              }
            
            
        });
        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });

        that.setData({
           
            categories: [
                {id: 0, name: "全部"},
                {id: 1, name: "猜你喜欢"},
            ],
            activeCategoryId: 0,
            //loadingMoreHidden: false
        });
    },
    typeClick:function(e){
      var that  = this
      this.setData({
        activeCategoryId: e.currentTarget.id
      })
      console.log(e.currentTarget.id)
      switch (e.currentTarget.id) {
        case "0":
        break;
        case "1":
          that.getallrecommendations()
          break;
          default:
      }

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
	listenerSearchInput:function( e ){
        this.setData({
            searchInput: e.detail.value
        });
	 },
	 toSearch:function( e ){
        this.setData({
            p:1,
            goods:[],
            loadingMoreHidden:true
        });
        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
              url: "/pages/recommendations/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        wx.navigateTo({
          url: "/pages/recommendations/info?id=" + e.currentTarget.dataset.id
        });
    },
    onReachBottom: function () { //下拉刷新
      var that = this;
      setTimeout(function () {
        that.getallrecommendations();
      }, 500);
    },
    getallrecommendations: function () {
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
        url: app.buildUrl('/recommendations/allrecommendations'),
        header: app.getRequestHeader(),
        method: 'get',
        data: {
          mix_kw: that.data.searchInput,
          p: that.data.arpages
        },
        success: function (res) {
          
          console.log(res.data),
            that.setData({
              goods: that.data.goods.concat(res.data.data),
              arpages: that.data.arpages + 1,
              processing: false
            })
            if (res.data.has_more == false) {
              that.setData({
                loadingMoreHidden: false
              });
            }
            }
      });
  }
});
