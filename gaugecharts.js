import * as echarts from 'echarts';

var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;

option = {
  series: [
    {
      type: 'gauge',
      progress: {
        show: true,
        width: 18
      },
      itemStyle: {
        color: '#7CFFB2'
      },
      axisLine: {
        lineStyle: {
          width: 18,
          color: [[1, '#fd666d']]
        }
      },
      pointer: {
        itemStyle: {
          color: '#000'
        }
      },
      axisTick: {
        show: false
      },
      splitLine: {
        length: 15,
        lineStyle: {
          width: 2,
          color: '#999'
        }
      },
      axisLabel: {
        distance: 25,
        color: '#999',
        fontSize: 20
      },

      title: {
        show: false
      },
      detail: {
        valueAnimation: true,
        fontSize: 80,
        offsetCenter: [0, '70%']
      },
      data: [
        {
          value: 0.9
        }
      ],
      min: -1,
      max: 1
    }
  ]
};

option && myChart.setOption(option);
