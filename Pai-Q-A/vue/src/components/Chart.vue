/*
 * @Author: hjj 
 * @Date: 2021-11-10 12:54:45 
 * @Last Modified by: hjj
 * @Last Modified time: 2021-11-16 11:18:25
 */

<template>
  <ve-histogram
    :data="chartData"
    width="1200px"
    height="500px"
    :extend = "chartExtend"
    :legend-visible="false"
  ></ve-histogram>
</template>

<script>
export default {
  name: "Chart",
  data() {
      this.chartExtend = {
      series (v) {
        v.forEach((i, index )=> {
          i.itemStyle = {
            normal: {
              label: {
                  show: true,
                  position:'top',
                  textStyle: {
                      fontSize: '12'
                  },
              },
              color: function(params) {
                // build a color map as your need.
                var colorList = [
                  '#C1232B','#B5C334','#FCCE10','#E87C25','#27727B',
                    '#FE8463','#9BCA63','#FAD860','#F3A43B','#60C0DD',
                    '#D7504B','#C6E579','#F4E001','#F0805A','#26C0C0'
                ];
                return colorList[params.dataIndex]
              },
            }
          }
        })
        return v
      },
    }
    return {
      chartData: {
        columns: ['日期', '收入'],
        rows: [
          { '日期': '1月', '收入': 0, },
          { '日期': '2月', '收入': 0,  },
          { '日期': '3月', '收入': 0,  },
          { '日期': '4月', '收入': 0,  },
          { '日期': '5月', '收入': 0,  },
          { '日期': '6月', '收入': 0,  },
          { '日期': '7月', '收入': 0, },
          { '日期': '8月', '收入': 0,  },
          { '日期': '9月', '收入': 0,  },
          { '日期': '10月', '收入': 0,  },
          { '日期': '11月', '收入': 0,  },
          { '日期': '12月', '收入': 0,  }
        ]
      },
      userMsg: {},
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      //从缓存中获取userMsg
      if(sessionStorage.getItem('userMsg')){
        let userMsg = sessionStorage.getItem('userMsg');
        this.userMsg = JSON.parse(userMsg);
      }
      else{
        this.userMsg = this.$userMsg;
      }
      
      if(this.userMsg.permission == 2){
        this.$http({
          url: this.$url + "api/sendansincome",
          method: 'get',
          params: {
            "username": this.userMsg.username,
          }
        })
        .then((res) => {
          let income = res.data.income;
          let tmp = income.split('#');
          let rows = [
            { '日期': '1月', '收入': parseFloat(tmp[0]), },
            { '日期': '2月', '收入': parseFloat(tmp[1]),  },
            { '日期': '3月', '收入': parseFloat(tmp[2]),  },
            { '日期': '4月', '收入': parseFloat(tmp[3]),  },
            { '日期': '5月', '收入': parseFloat(tmp[4]),  },
            { '日期': '6月', '收入': parseFloat(tmp[5]),  },
            { '日期': '7月', '收入': parseFloat(tmp[6]), },
            { '日期': '8月', '收入': parseFloat(tmp[7]),  },
            { '日期': '9月', '收入': parseFloat(tmp[8]),  },
            { '日期': '10月', '收入': parseFloat(tmp[9]),  },
            { '日期': '11月', '收入': parseFloat(tmp[10]),  },
            { '日期': '12月', '收入': parseFloat(tmp[11]),  }
          ]
          this.chartData.rows = rows;
        })
      }
    }
  },
}
</script>

<style>

</style>