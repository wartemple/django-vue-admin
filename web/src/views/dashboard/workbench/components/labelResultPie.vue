<template>
  <el-card class="card-view">
    <div id="labelChart" :style="{width: pxData.wpx+'px',height: pxData.hpx+'px'}"></div>
  </el-card>
</template>

<script>
import { request } from '@/api/service'

export default {
  sort: 1,
  title: '标注结果统计图',
  name: 'labelResultPie',
  icon: 'el-icon-pie-chart',
  description: '已标注结果统计图',
  height: 36,
  width: 12,
  isResizable: true,
  props: {
    pxData: {
      type: Object,
      require: false,
      default: () => ({
        wpx: 0,
        hpx: 0
      })
    }
  },
  watch: {
    pxData: {
      handler () {
        // eslint-disable-next-line no-unused-expressions
        this.myChart?.resize({ width: this.pxData.wpx, height: this.pxData.hpx })
      },
      immediate: true,
      deep: true
    }
  },
  data () {
    this.myChart = null
    return {
      data: []
    }
  },
  methods: {
    drawLine () {
      const seriesData = this.data
      const option = {
        title: {
          text: '标注结果统计图',
          subtext: '仅统计已标注且同步的数据集内部的标注结果',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{c} ({d}%)'
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true }
          }
        },
        series: [{
          name: '',
          type: 'pie',
          radius: [0, 60],
          center: ['40%', '50%'],
          itemStyle: { borderRadius: 2 },
          label: {
            formatter: '{b}'
          },
          data: seriesData
        }]
      }
      this.myChart.setOption(option)
    },
    initGet () {
      request({
        url: '/api/label/label_results/statistics/'
      }).then((res) => {
        this.data = res.data.data
        this.drawLine(this.data)
      })
    }
  },
  mounted () {
    this.myChart = this.$echarts.init(document.getElementById('labelChart'))
    this.initGet()
    this.drawLine()
    console.log(document.getElementById('labelChart'))
  }
}
</script>

<style scoped lang="scss">
.card-view {
  //border-radius: 10px;
  color: $color-primary;

  .card-content {
    .card-content-label {
      font-size: 1em;
    }

    .card-content-value {
      margin-top: 10px;
      font-size: 1.5em;
      font-weight: bold;
    }
  }
}

.el-icon-user-solid {
  font-size: 30px;
}

.el-card {
  height: 100%;
}
</style>
