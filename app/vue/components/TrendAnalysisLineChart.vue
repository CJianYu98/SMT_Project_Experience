<script>
  import { Line } from 'vue-chartjs';

  export default {
    extends: Line,
    // mixins: [mixins.reactiveProp],
    props:{
      data:{
        type: Object,
        required: true
      }
    },
    data: (instance) => {
      return {
        // chartData: {
        //   labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //   "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", 
        //   "Dec 2021", "Jan 2022"],
        //   datasets: [
        //     {
        //       label: 'Line Chart',
        //       data: [600,	1150,	342,	6050,	2522,	3241,	1259,	157,	1545, 5000, 8500, 9841],
        //       fill: false,
        //       borderColor: '#392A9B',
        //       backgroundColor: '#392A9B',
        //       borderWidth: 1
        //     }
        //   ]
        // },
        chartData: instance.data.chartData,
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
    // methods: {
    //   onChange:function onChange(){
    //       this.$emit('changeChart',this.chartData);
    //   }
    // },
    mounted () {
      this.renderChart(this.chartData, this.options);
    },
    watch: {
      data () {
        // this._chart.destroy();
        this.renderChart(this.data.chartData, this.options);
        // this.update();
      }
    },
  }
</script>