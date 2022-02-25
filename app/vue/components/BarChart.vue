<script>
  import { Bar } from 'vue-chartjs'
  export default {
    extends: Bar,
    data() {
      return {
        chartData: {
          // labels: ["2015-01"
          // ],
          datasets: [
            {
              label: 'Negative',
              data: [10],
              backgroundColor: 'rgba(255, 99, 132, 0.2)',
            },
            {
              label: 'Neutral',
              data: [50],
              backgroundColor: 'rgba(255, 206, 86, 0.2)',
            },
            {
              label: 'Positive',
              data: [40],
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
            }
          ]
        },
        options: {
          scales: {
            yAxes: [{
              // ticks: {
              //   beginAtZero: true
              // },
              gridLines: {
                display: false
              },
              stacked: true
            }],
            xAxes: [{
              gridLines: {
                display: false
              },
              stacked: true
            }]
          },
          legend: {
            display: false
          },
          responsive: true,
          maintainAspectRatio: false
        }
      }
    },
    mounted() {
      this.renderChart(this.chartData, this.options)
    }
  }
</script>