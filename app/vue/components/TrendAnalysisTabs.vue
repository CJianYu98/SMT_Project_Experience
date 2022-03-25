<template>
  <!-- <v-card>
    <v-tabs
      background-color="deep-purple"
      center-active
      dark
    >
      <v-tab><v-img src="facebook_icon.png"></v-img>Facebook</v-tab>
      <v-tab><v-img src="instagram_icon.png"></v-img>Instagram</v-tab>
      <v-tab><v-img src="reddit_icon.png"></v-img>Reddit</v-tab>
      <v-tab><v-img src="twitter_icon.png"></v-img>Twitter</v-tab>
      <v-tab><v-img src="youtube_icon.png"></v-img>Youtube</v-tab>
    </v-tabs>
  </v-card> -->

  <v-card>
    <v-tabs
        v-model="tabs"
        centered
    >
        <v-tab
            v-for="media in medias"
            :key="media"
        >
            <v-img 
              v-if="media !== 'all'" 
              :src="`/${media}_icon.png`"
              max-height="30px"
              max-width="30px"
            >
            </v-img>
            &nbsp;
            {{ media }}
        </v-tab>
        <v-tab-item
          v-for="view in mediasMetrics" 
          :key="view"  
        >
        <!-- <v-card v-if="view === 'all'"> -->
          <v-card flat>
            <v-container fluid class="px-4 mt-n4 pb-0">
              <v-row no-gutters align="stretch">
                <v-col class="d-flex">
                  <v-card-title class="text-h5">
                    Number of Posts
                  </v-card-title>
                  <v-spacer></v-spacer>
                  <DropDownSelect :viewFilter="view.view" :label="label"></DropDownSelect>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
          <v-card >
            <line-chart class="chartBox" :chartData="view.chartData"></line-chart>
          </v-card>  
        <!-- </v-card> -->
        </v-tab-item>
    </v-tabs>
    
    <!-- <v-tabs-items v-model="tabs">
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-4 mt-n4 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect :viewFilter="allView" :label="label"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
        <v-card>
          <line-chart class="chartBox" :chartData="allChartData"></line-chart>
        </v-card>
      </v-tab-item>

      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-4 mt-n4 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect :viewFilter="facebookView" :label="label"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
        <v-card>
          <line-chart class="chartBox" :chartData="facebookChartData"></line-chart>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-4 mt-n4 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect :viewFilter="redditView" :label="label"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
        <v-card>
          <line-chart class="chartBox" :chartData="redditChartData"></line-chart>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-4 mt-n4 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect :viewFilter="twitterView" :label="label"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
        <v-card>
          <line-chart class="chartBox" :chartData="twitterChartData"></line-chart>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-4 mt-n4 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect :viewFilter="youtubeView" :label="label"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
        <v-card>
          <line-chart class="chartBox" :chartData="youtubeChartData"></line-chart>
        </v-card>
      </v-tab-item>
    </v-tabs-items> -->
  </v-card>

</template>

<script>
import DropDownSelect from "./DropDownSelect.vue"
import LineChart from '@/components/TrendAnalysisLineChart'

  export default {
    props: {
      medias: {
        type: Object,
        required: true
      },
      mediasMetrics: {
        type: Array,
        required: true
      }
    },
    components: {
        LineChart,
        DropDownSelect,
    },
    data: () => {
      return {
        tabs: null,
        label: 'View',
        // medias: ['all','facebook','reddit','twitter','youtube'],
        // mediaMetrics: { 
        //   all: {
        //     view: ['Number of Likes'],
        //     chartData: {
        //       labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //       "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //       datasets: [
        //         {
        //           label: 'Facebook',
        //           data: [600,	1150,	342,	6050,	2522,	3241,	1259,	157,	1545, 5000, 8500, 9841],
        //           fill: false,
        //           borderColor: '#3949AB',
        //           backgroundColor: '#3949AB',
        //           borderWidth: 1,
        //           // tension: 0.1
        //         },
        //         {
        //           label: 'Reddit',
        //           data: [7700,	1150,	342,	7050,	5522,	341,	259,	1577,	2345, 6000, 8000, 9041],
        //           fill: false,
        //           borderColor: '#EF6C00',
        //           backgroundColor: '#EF6C00',
        //           borderWidth: 1,
        //         },
        //         {
        //           label: 'Twitter',
        //           data: [2300,	150,	4342,	7050,	1522,	3841,	1559,	657,	1445, 3000, 4500, 6641],
        //           fill: false,
        //           borderColor: '#42A5F5',
        //           backgroundColor: '#42A5F5',
        //           borderWidth: 1
        //         },
        //         {
        //           label: 'Youtube',
        //           data: [6880,	550,	2342,	6070,	522,	2241,	1259,	3157,	1545, 6000, 8500, 9841],
        //           fill: false,
        //           borderColor: '#C62828',
        //           backgroundColor: '#C62828',
        //           borderWidth: 1
        //         },
        //       ]
        //     },
        //   }, 
        //   facebook: {
        //     view: ['Number of Likes', 'Number of Comments', 'Number of Shares'],
        //     chartData: {
        //        labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //       "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //       datasets: [
        //         {
        //           label: 'Facebook',
        //           data: [600,	1150,	342,	6050,	2522,	3241,	1259,	157,	1545, 5000, 8500, 9841],
        //           fill: false,
        //           borderColor: '#3949AB',
        //           backgroundColor: '#3949AB',
        //           borderWidth: 1,
        //         }
        //       ]
        //     }
        //   }, 
        //   reddit: {
        //     view: ['Number of Net Votes', 'Number of Comments', 'Number of Awards'],
        //     chartData: {
        //       labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //       "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //       datasets: [
        //         {
        //           label: 'Reddit',
        //           data: [7700,	1150,	342,	7050,	5522,	341,	259,	1577,	2345, 6000, 8000, 9041],
        //           fill: false,
        //           borderColor: '#EF6C00',
        //           backgroundColor: '#EF6C00',
        //           borderWidth: 1
        //         }
        //       ]
        //     }
        //   },         
        //   twitter: {
        //     view: ['Number of Likes','Number of Retweets','Number of Replies'],
        //     chartData: {
        //       labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //       "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //       datasets: [
        //         {
        //           label: 'Twitter',
        //           data: [2300,	150,	4342,	7050,	1522,	3841,	1559,	657,	1445, 3000, 4500, 6641],
        //           fill: false,
        //           borderColor: '#42A5F5',
        //           backgroundColor: '#42A5F5',
        //           borderWidth: 1
        //         }
        //       ]
        //     }
        //   }, 
        //   youtube: {
        //     view: ['Number of Likes', 'Number of Views', 'Number of Comments'],
        //     chartData: {
        //       labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //       "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //       datasets: [
        //         {
        //           label: 'Youtube',
        //           data: [6880,	550,	2342,	6070,	522,	2241,	1259,	3157,	1545, 6000, 8500, 9841],
        //           fill: false,
        //           borderColor: '#C62828',
        //           backgroundColor: '#C62828',
        //           borderWidth: 1
        //         }
        //       ]
        //     }
        //   }
        // },
        // allView: [{view: 'Number of Likes'}],
        // facebookView: [{view: 'Number of Likes'}, {view: 'Number of Comments'}, {view: 'Number of Shares'}],
        // redditView: [{view: 'Number of Net Votes'}, {view: 'Number of Comments'}, {view: 'Number of Awards'}],        
        // twitterView: [{view: 'Number of Likes'}, {view: 'Number of Retweets'}, {view: 'Number of Replies'}],
        // youtubeView: [{view: 'Number of Likes'}, {view: 'Number of Views'}, {view: 'Number of Comments'}],
        // allChartData: {
        //   labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //   "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //   datasets: [
        //     {
        //       label: 'Facebook',
        //       data: [600,	1150,	342,	6050,	2522,	3241,	1259,	157,	1545, 5000, 8500, 9841],
        //       fill: false,
        //       borderColor: '#3949AB',
        //       backgroundColor: '#3949AB',
        //       borderWidth: 1,
        //       // tension: 0.1
        //     },
        //     {
        //       label: 'Reddit',
        //       data: [7700,	1150,	342,	7050,	5522,	341,	259,	1577,	2345, 6000, 8000, 9041],
        //       fill: false,
        //       borderColor: '#EF6C00',
        //       backgroundColor: '#EF6C00',
        //       borderWidth: 1,
        //     },
        //     {
        //       label: 'Twitter',
        //       data: [2300,	150,	4342,	7050,	1522,	3841,	1559,	657,	1445, 3000, 4500, 6641],
        //       fill: false,
        //       borderColor: '#42A5F5',
        //       backgroundColor: '#42A5F5',
        //       borderWidth: 1
        //     },
        //     {
        //       label: 'Youtube',
        //       data: [6880,	550,	2342,	6070,	522,	2241,	1259,	3157,	1545, 6000, 8500, 9841],
        //       fill: false,
        //       borderColor: '#C62828',
        //       backgroundColor: '#C62828',
        //       borderWidth: 1
        //     },
        //   ]
        // },
        // facebookChartData: {
        //   labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //   "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //   datasets: [
        //     {
        //       label: 'Facebook',
        //       data: [600,	1150,	342,	6050,	2522,	3241,	1259,	157,	1545, 5000, 8500, 9841],
        //       fill: false,
        //       borderColor: '#3949AB',
        //       backgroundColor: '#3949AB',
        //       borderWidth: 1,
        //       // tension: 0.1
        //     }
        //   ]
        // },
        // redditChartData: {
        //   labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //   "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //   datasets: [
        //     {
        //       label: 'Reddit',
        //       data: [7700,	1150,	342,	7050,	5522,	341,	259,	1577,	2345, 6000, 8000, 9041],
        //       fill: false,
        //       borderColor: '#EF6C00',
        //       backgroundColor: '#EF6C00',
        //       borderWidth: 1
        //     }
        //   ]
        // },
        // twitterChartData: {
        //   labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //   "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //   datasets: [
        //     {
        //       label: 'Twitter',
        //       data: [2300,	150,	4342,	7050,	1522,	3841,	1559,	657,	1445, 3000, 4500, 6641],
        //       fill: false,
        //       borderColor: '#42A5F5',
        //       backgroundColor: '#42A5F5',
        //       borderWidth: 1
        //     }
        //   ]
        // },
        // youtubeChartData: {
        //   labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
        //   "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        //   datasets: [
        //     {
        //       label: 'Youtube',
        //       data: [6880,	550,	2342,	6070,	522,	2241,	1259,	3157,	1545, 6000, 8500, 9841],
        //       fill: false,
        //       borderColor: '#C62828',
        //       backgroundColor: '#C62828',
        //       borderWidth: 1
        //     }
        //   ]
        // },
      }
    },
  }
</script>

<style>
  /* .chartBox {
    width: 800px;
    height: 360px;
  } */
</style>