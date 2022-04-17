<template>
  <v-card class="pt-2 pb-2">
    <v-tabs
        v-model="tabs"
        centered
    >
        <v-tab
            v-for="media in mediaData.medias"
            :key="media"
            @change="reset(media)"
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
          v-for="(platform, index) in mediaData.mediaView" 
          :key="index"
        >
          <!-- <v-card flat> -->
            <!-- <v-container fluid class="px-4 mt-n2 mb-1 pb-0"> -->
              <v-row no-gutters align="stretch" >
                <v-col class="d-flex">
                  <v-card-title class="text-h5">
                    {{ selectedViewOption }}
                  </v-card-title>
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="4">
                  <DropDownSelect 
                  :viewFilter="selectedViewList" 
                  :viewSelected="selectedViewOption"
                  @changeView="changeViewOption($event)"
                  :label="label">
                  </DropDownSelect>
                </v-col>
              </v-row>
            <!-- </v-container> -->
          <!-- </v-card> -->
          <v-card class="">
            <line-chart class="chartBox" :data="formattedChartData"></line-chart>  
          </v-card>   
        </v-tab-item>
    </v-tabs>
  </v-card>
</template>

<script>
import DropDownSelect from "./DropDownSelect.vue"
import LineChart from '@/components/TrendAnalysisLineChart'

  export default {
    props: {
      mediaData: {
        type: Object,
        required: true
      },
      mediaChartData: {
        type: Object,
        required: true
      },
      sentimentColors: {
        type: Object,
        required: true
      },
      emotionColors: {
        type: Object,
        required: true
      }
    },
    components: {
        LineChart,
        DropDownSelect,
    },
    data: (instance) => {
      return {
        tabs: null,
        label: 'View',
        selectedTab: instance.mediaData.medias[0],
        selectedViewList: instance.mediaData.mediaView.all,
        selectedViewOption: instance.mediaData.mediaView.all[0],
        formattedChartData: {},
        // selectedTab: instance.mediaData.medias[0],
        // selectedViewList: instance.mediaData.mediaView.all,
        // selectedViewOption: instance.mediaData.mediaView.all[0],
        // formattedChartData: this.defaultChartData(),
        selectedChartData: [],
        selectedTabColor: '',
        selectedDatePeriod: '',
        selectedDateLabels: ["Jan 2021", "Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
        colorCode: {
          media: {
            facebook: '#3949AB',
            reddit: '#EF6C00',
            twitter: '#42A5F5',
            youtube: '#C62828'
          },
          sentiment: {
            negative: instance.sentimentColors.negative,
            neutral: instance.sentimentColors.neutral,
            positive: instance.sentimentColors.positive,
          },
          emotion: {
            anger: instance.emotionColors.anger,
            fear: instance.emotionColors.fear,
            joy: instance.emotionColors.joy,
            neutral: instance.emotionColors.neutral,
            sadness: instance.emotionColors.sadness
          }
        },
      }
    },
    methods:{
      reset(media)
      {
        this.selectedTab = media;
        
        // 'number of mentions' is the default selection for all tabs 
        this.selectedViewOption= 'Number of Mentions';

        // change view options and chart data
        if (this.selectedTab === 'all'){
          this.selectedViewList = this.$props.mediaData.mediaView.all;
          this.selectedChartData = this.$props.mediaChartData.all.mentions;
        }   
        else if (this.selectedTab === 'facebook'){
          this.selectedViewList = this.$props.mediaData.mediaView.facebook;
          this.selectedChartData = this.$props.mediaChartData.facebook.mentions;
        }
        else if (this.selectedTab === 'reddit'){
          this.selectedViewList = this.$props.mediaData.mediaView.reddit;
          this.selectedChartData = this.$props.mediaChartData.reddit.mentions;
        }
        else if (this.selectedTab === 'twitter'){
          this.selectedViewList = this.$props.mediaData.mediaView.twitter;
          this.selectedChartData = this.$props.mediaChartData.twitter.mentions;
        }
        else if (this.selectedTab === 'youtube'){
          this.selectedViewList = this.$props.mediaData.mediaView.youtube;
          this.selectedChartData = this.$props.mediaChartData.youtube.mentions;
        }            
      },
      changeViewOption(selectedViewOption)
      {
        this.selectedViewOption = selectedViewOption;
        this.changeChart();
      },
      changeChart()
      {
        // All tab
        // if (this.selectedTab === 'all'){
        //   if (this.selectedViewOption === 'Number of Mentions'){
        //     this.selectedChartData = this.$props.mediasMetrics.all.data_mentions;
        //   } 
        //   else if (this.selectedViewOption === 'Number of Likes'){            
        //     this.selectedChartData = this.$props.mediasMetrics.all.data_likes;
        //   }
        // }
        
        // Facebook tab
        if (this.selectedTab === 'facebook'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediaChartData.facebook.mentions;
          } 
          else if (this.selectedViewOption === 'Number of Likes'){            
            this.selectedChartData = this.$props.mediaChartData.facebook.likes;
          }
          // else if (this.selectedViewOption === 'Number of Shares'){            
          //   this.selectedChartData = this.$props.mediasMetrics.facebook.data_shares;
          // }
          else if (this.selectedViewOption === 'Sentiments'){            
            this.selectedChartData = this.$props.mediaChartData.facebook.sentiments;
          }
          else if (this.selectedViewOption === 'Emotions'){            
            this.selectedChartData = this.$props.mediaChartData.facebook.emotions;
          }
          this.selectedTabColor = this.colorCode.medias.facebook;
        }
        // Reddit tab
        else if (this.selectedTab === 'reddit'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediaChartData.reddit.mentions;
          } 
          else if (this.selectedViewOption === 'Number of Net Votes'){            
            this.selectedChartData = this.$props.mediaChartData.reddit.likes;
          }
          else if (this.selectedViewOption === 'Number of Awards'){            
            this.selectedChartData = this.$props.mediaChartData.reddit.awards;
          }
          else if (this.selectedViewOption === 'Sentiments'){            
            this.selectedChartData = this.$props.mediaChartData.reddit.sentiments;
          }
          else if (this.selectedViewOption === 'Emotions'){            
            this.selectedChartData = this.$props.mediaChartData.reddit.emotions;
          }
          this.selectedTabColor = this.colorCode.medias.reddit;
        }
        // Twitter tab
        else if (this.selectedTab === 'twitter'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediaChartData.twitter.mentions;
          } 
          else if (this.selectedViewOption === 'Number of Likes'){            
            this.selectedChartData = this.$props.mediaChartData.twitter.likes;
          }
          else if (this.selectedViewOption === 'Number of Retweets'){            
            this.selectedChartData = this.$props.mediaChartData.twitter.retweets;
          }
          else if (this.selectedViewOption === 'Sentiments'){            
            this.selectedChartData = this.$props.mediaChartData.twitter.sentiments;
          }
          else if (this.selectedViewOption === 'Emotions'){            
            this.selectedChartData = this.$props.mediaChartData.twitter.emotions;
          }
          this.selectedTabColor = this.colorCode.medias.twitter;
        }
        // Youtube tab
        else if (this.selectedTab === 'youtube'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediaChartData.youtube.mentions;
          } 
          else if (this.selectedViewOption === 'Number of Likes'){            
            this.selectedChartData = this.$props.mediaChartData.youtube.likes;
          }
          else if (this.selectedViewOption === 'Number of Views'){            
            this.selectedChartData = this.$props.mediaChartData.youtube.views;
          }
          else if (this.selectedViewOption === 'Sentiments'){            
            this.selectedChartData = this.$props.mediaChartData.youtube.sentiments;
          }
          else if (this.selectedViewOption === 'Emotions'){            
            this.selectedChartData = this.$props.mediaChartData.youtube.emotions;
          }
          this.selectedTabColor = this.colorCode.medias.youtube;
        }
        
        this.formatChartDataset();
      },
      formatChartDataset()
      {
        if (this.selectedTab === 'all'){
          this.allChartData();
        }
        // Sentiment View
        else if (this.selectedViewList === 'Sentiments'){ 
          this.formattedChartData = {
            labels: this.selectedDateLabels,
            datasets: [
              {
                label: 'Negative',
                data: this.selectedChartData.positive,
                fill: false,
                borderColor: this.colorCode.sentiment.negative,
                backgroundColor: this.colorCode.sentiment.negative,
                borderWidth: 1,
              },
              {
                label: 'Neutral',
                data: this.selectedChartData.neutral,
                fill: false,
                borderColor: this.colorCode.sentiment.neutral,
                backgroundColor: this.colorCode.sentiment.neutral,
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: this.selectedChartData.negative,
                fill: false,
                borderColor: this.colorCode.sentiment.positive,
                backgroundColor: this.colorCode.sentiment.positive,
                borderWidth: 1,
              },
            ]
          }
        }
        // Emotions View
        else if (this.selectedViewList === 'Emotions'){ 
          this.formattedChartData = {
            labels: this.selectedDateLabels,
            datasets: [
              {
                label: this.selectedTab,
                data: this.selectedChartData.anger,
                fill: false,
                borderColor: this.colorCode.emotion.anger,
                backgroundColor: this.colorCode.emotion.anger,
                borderWidth: 1,
              },
              {
                label: this.selectedTab,
                data: this.selectedChartData.fear,
                fill: false,
                borderColor: this.colorsCode.emotion.fear,
                backgroundColor: this.colorCode.emotion.fear,
                borderWidth: 1,
              },
              {
                label: this.selectedTab,
                data: this.selectedChartData.joy,
                fill: false,
                borderColor: this.colorsCode.emotion.joy,
                backgroundColor: this.colorCode.emotion.joy,
                borderWidth: 1,
              },
              {
                label: this.selectedTab,
                data: this.selectedChartData.neutral,
                fill: false,
                borderColor: this.colorsCode.emotion.neutral,
                backgroundColor: this.colorCode.emotion.neutral,
                borderWidth: 1,
              },
              {
                label: this.selectedTab,
                data: this.selectedChartData.sadness,
                fill: false,
                borderColor: this.colorsCode.emotion.sadness,
                backgroundColor: this.colorCode.emotion.sadness,
                borderWidth: 1,
              }
            ]
          }
        }
        // Other Views
        else {
          this.formattedChartData = {
            labels: this.selectedDateLabels,
            datasets: [
              {
                label: this.selectedTab,
                data: this.selectedChartData,
                fill: false,
                borderColor: this.selectedTabColor,
                backgroundColor: this.selectedTabColor,
                borderWidth: 1,
              },
            ]
          }
        }
      },
      allChartData()
      {
        if (this.selectedViewOption === 'Number of Mentions') {
          this.formattedChartData = {
            labels: [],
            datasets: [
              {
                label: this.$props.mediaData.medias[1],
                data: this.$props.mediaChartData.facebook.mentions,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              },
              {
                label: this.$props.mediaData.medias[2],
                data: this.$props.mediaChartData.reddit.mentions,
                fill: false,
                borderColor: this.colorCode.media.reddit,
                backgroundColor: this.colorCode.media.reddit,
                borderWidth: 1,
              },
              {
                label: this.$props.mediaData.medias[3],
                data: this.$props.mediaChartData.facebook.mentions,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              },
              {
                label: this.$props.mediaData.medias[4],
                data: this.$props.mediaChartData.facebook.mentions,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              },
            ]
          };
        }
        else {
          this.formattedChartData = {
            labels: [],
            datasets: [
              {
                label: this.$props.mediaData.medias[1],
                data: this.$props.mediaChartData.facebook.likes,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              },
              {
                label: this.$props.mediaData.medias[2],
                data: this.$props.mediaChartData.reddit.likes,
                fill: false,
                borderColor: this.colorCode.media.reddit,
                backgroundColor: this.colorCode.media.reddit,
                borderWidth: 1,
              },
              {
                label: this.$props.mediaData.medias[3],
                data: this.$props.mediaChartData.facebook.likes,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              },
              {
                label: this.$props.mediaData.medias[4],
                data: this.$props.mediaChartData.facebook.likes,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              },
            ]
          };
        }
      },
      defaultChartData()
      {
        return {
          labels: [],
          datasets: [
            {
              label: this.$props.mediaData.medias[1],
              data: this.$props.mediaChartData.facebook.mentions,
              fill: false,
              borderColor: this.colorCode.media.facebook,
              backgroundColor: this.colorCode.media.facebook,
              borderWidth: 1,
            },
            {
              label: this.$props.mediaData.medias[2],
              data: this.$props.mediasMetrics.reddit.mentions,
              fill: false,
              borderColor: this.colorCode.media.reddit,
              backgroundColor: this.colorCode.media.reddit,
              borderWidth: 1,
            },
            {
              label: this.$props.mediaData.medias[3],
              data: this.$props.mediasMetrics.facebook.mentions,
              fill: false,
              borderColor: this.colorCode.media.facebook,
              backgroundColor: this.colorCode.media.facebook,
              borderWidth: 1,
            },
            {
              label: this.$props.mediaData.medias[4],
              data: this.$props.mediasMetrics.facebook.mentions,
              fill: false,
              borderColor: this.colorCode.media.facebook,
              backgroundColor: this.colorCode.media.facebook,
              borderWidth: 1,
            },
          ]
        };
      }
    }, // end of methods
  }
</script>

<style>
  .chartBox {
    width: 800px;
    height: 420px;
  }
</style>