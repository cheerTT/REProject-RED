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
        activeCategoryId: '0',
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        arpages:0,
        toprecommendations :[],
        allrecommendations :[],
        imagePath : app.globalData.imagePath,
        processing: false,
        p:1,
    },
    onLoad: function () {
        var that = this;
        this.getHotCommodityList();
        if (getApp().globalData.user_id == "not_user")
        {
          that.setData({
            toprecommendations: this.goods.slice(0, 5)
          })
        }
        else{
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
        }

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
        if (getApp().globalData.user_id == "not_user") {
          that.setData({

            categories: [
              { id: 0, name: "爆款！！！" },
            ],
            activeCategoryId: '0',
            //loadingMoreHidden: false
          });
        }
        else{
          that.setData({
            
              categories: [
                  {id: 0, name: "爆款！！！"},
                  {id: 1, name: "猜你喜欢"},
              ],
              activeCategoryId: '0',
              //loadingMoreHidden: false
          });
        }
    },
    onShow: function () {
      // this.getType();
      var that = this
        this.setData({
          p: 1,
          arpages:0,
          goods: [],
          loadingMoreHidden: true
        });
      switch (that.data.activeCategoryId){
        case'0':
          this.getHotCommodityList();
          break;
        case'1':
          this.getallrecommendations();
          break;
        default :
      }
        //this.getHotCommodityList();

      },

    typeClick:function(e){
      var that  = this
      this.setData({
        activeCategoryId: e.currentTarget.id
      })
      switch (e.currentTarget.id) {
        case "0":
          this.setData({
            loadingMoreHidden: true,
            goods: [],
            activeCategoryId: e.currentTarget.id,
            p: 1
          });
          that.getHotCommodityList()
          break;
        case "1":
          this.setData({
            loadingMoreHidden: true,
            goods: [],
            activeCategoryId: e.currentTarget.id,
            arpages:0
          });
          that.getallrecommendations()
          break;
          default:
      }

    },

    toDetailsTap: function (e) {
      wx.navigateTo({
        url: "/pages/commodity/info?id=" + e.currentTarget.dataset.id
      });
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
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
              url: "/pages/commodity/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
      console.log(e.currentTarget.dataset.id)
        wx.navigateTo({
          url: "/pages/commodity/info?id=" + e.currentTarget.dataset.id
        });
    },
    onReachBottom: function () { //下拉刷新
      var that = this;
      console.log(that.data.activeCategoryId)
      switch (that.data.activeCategoryId){
        case '0':
        setTimeout(function () {
          that.getHotCommodityList();
        }, 500);
        break;
        case '1':
          setTimeout(function () {
            that.getallrecommendations();
          }, 500);
        break;
        default:
      }
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
        var goods = res.data.data;
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
  },
   
});
