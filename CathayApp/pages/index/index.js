Page({
  data: {
    locations: ['上海 (SHA)', '香港 (HKG)'],
    departure: '上海 (SHA)',
    arrival: '香港 (HKG)',
    date: '选择出发日期',
    cabinClass: '经济舱',
    passengers: '1成人 0儿童 0婴儿'
  },
  bindDepartureChange(e) {
    this.setData({
      departure: this.data.locations[e.detail.value]
    });
  },
  bindArrivalChange(e) {
    this.setData({
      arrival: this.data.locations[e.detail.value]
    });
  },
  bindDateChange(e) {
    this.setData({
      date: e.detail.value
    });
  },
  searchFlights() {
    // 实现搜索逻辑
  }
});