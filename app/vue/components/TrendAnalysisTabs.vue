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
            <v-img :src="`/${media}_icon.png`">
            </v-img>
            &nbsp;
            {{ media }}
        </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tabs">
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-8 mt-n2 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect v-bind:viewFilter="fbView"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
          <line-chart class="chartBox" v-bind:chartData="fbChartData"></line-chart>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-8 mt-n2 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect v-bind:viewFilter="fbView"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
          <line-chart class="chartBox" v-bind:chartData="instaChartData"></line-chart>
          <!-- <v-img
            :aspect-ratio="2.8"
            :width="width"
            src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img> -->
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-8 mt-n2 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect v-bind:viewFilter="redditView"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
          <line-chart class="chartBox" v-bind:chartData="redditChartData"></line-chart>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-8 mt-n2 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect v-bind:viewFilter="twitterView"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
          <line-chart class="chartBox" v-bind:chartData="twitterChartData"></line-chart>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-container fluid class="px-8 mt-n2 pb-0">
            <v-row no-gutters align="stretch">
              <v-col class="d-flex">
                <v-card-title class="text-h5">
                  Number of Posts
                </v-card-title>
                <v-spacer></v-spacer>
                <DropDownSelect v-bind:viewFilter="youtubeView"></DropDownSelect>
              </v-col>
            </v-row>
          </v-container>
          <line-chart class="chartBox" v-bind:chartData="youtubeChartData"></line-chart>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>

</template>

<script>
import DropDownSelect from "./DropDownSelect.vue"
import LineChart from '@/components/LineChart'

  export default {
    components: {
        LineChart,
        DropDownSelect
    },
    data () {
      return {
        tabs: null,
        medias: ['facebook','instagram','reddit','twitter','youtube'],
        fbView: [{view: 'Number of Likes'}, {view: 'Number of Comments'}, {view: 'Number of Shares'}],
        redditView: [{view: 'Number of Net Votes'}, {view: 'Number of Comments'}, {view: 'Number of Awards'}],        
        twitterView: [{view: 'Number of Likes'}, {view: 'Number of Retweets'}, {view: 'Number of Replies'}],
        youtubeView: [{view: 'Number of Likes'}, {view: 'Number of Views'}, {view: 'Number of Comments'}],
        fbChartData: {
          labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
          "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
          datasets: [
            {
              label: 'Facebook',
              data: [600,	1150,	342,	6050,	2522,	3241,	1259,	157,	1545, 5000, 8500, 9841],
              fill: false,
              borderColor: '#392A9B',
              backgroundColor: '#392A9B',
              borderWidth: 1,
              // tension: 0.1
            }
          ]
        },
        instaChartData: {
          labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
          "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
          datasets: [
            {
              label: 'Instagram',
              data: [3300,	5450,	9042,	50,	2552,	7241,	4259,	5157,	145, 5800, 6600, 8841],
              fill: false,
              borderColor: '#392A9B',
              backgroundColor: '#392A9B',
              borderWidth: 1
            }
          ]
        },
        redditChartData: {
          labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
          "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
          datasets: [
            {
              label: 'Reddit',
              data: [7700,	1150,	342,	7050,	5522,	341,	259,	1577,	2345, 6000, 8000, 9041],
              fill: false,
              borderColor: '#392A9B',
              backgroundColor: '#392A9B',
              borderWidth: 1
            }
          ]
        },
        twitterChartData: {
          labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
          "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
          datasets: [
            {
              label: 'Twitter',
              data: [600,	1150,	342,	6050,	2522,	3241,	1259,	157,	1445, 3000, 4500, 6641],
              fill: false,
              borderColor: '#392A9B',
              backgroundColor: '#392A9B',
              borderWidth: 1
            }
          ]
        },
        youtubeChartData: {
          labels: ["Feb 2021",	"Mar 2021",	"Apr 2021",	"May 2021",	"Jun 2021",	
          "Jul 2021",	"Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
          datasets: [
            {
              label: 'Youtube',
              data: [6880,	550,	2342,	6070,	522,	2241,	1259,	3157,	1545, 6000, 8500, 9841],
              fill: false,
              borderColor: '#392A9B',
              backgroundColor: '#392A9B',
              borderWidth: 1
            }
          ]
        },
      }
    },
  }
</script>

<style>
  .chartBox {
    width: 800px;
    height: 300px;
  }
</style>