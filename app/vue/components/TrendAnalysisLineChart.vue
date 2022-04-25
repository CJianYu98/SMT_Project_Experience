<script>
  import { Line } from 'vue-chartjs';

  export default {
    extends: Line,
    props:{
      data:{
        type: Object,
        required: true
      }
    },
    data: (instance) => {
      return {
        chartData: instance.data,
        options: {
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Count'
              },
              ticks: {
                beginAtZero: true
              },
              gridLines: {
                display: true
              }
            }],
            xAxes: [ {
              gridLines: {
                display: false
              }
            }]
          },
          legend: {
            display: true
          },
          responsive: true,
          maintainAspectRatio: false,
        }
      }
    },
    mounted () {
      this.renderChart(this.chartData, this.options);
    },
    watch: {
      data (to,from) {
        this.renderChart(this.chartData, this.options);
      }
    },
  }
</script>