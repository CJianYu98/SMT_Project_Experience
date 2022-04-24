<template>
  <v-card class="pt-2 pb-2">
    <v-tabs
        v-model="tabs"
        centered
    >
        <v-tab
            v-for="media in selectedMedia"
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
          v-for="(platform, index) in selectedMedia" 
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
            <line-chart class="chartBox" 
              
              :data="formattedChartData"></line-chart> 
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
      },
      dateLabels: {
        type: Array,
        required: true
      },
      selectedMedia: {
        type: Array,
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
        // selectedTab: instance.mediaData.medias[0],
        // selectedViewList: instance.mediaData.mediaView.all,
        // selectedViewOption: instance.mediaData.mediaView.all[0],
        formattedChartData: {},
        selectedTab: instance.mediaData.medias[0],
        selectedViewList: instance.mediaData.mediaView.all,
        selectedViewOption: instance.mediaData.mediaView.all[0],
        // formattedChartData: this.defaultChartData(),
        selectedChartData: [],
        selectedTabColor: '',
        selectedDatePeriod: '',
        selectedDateLabels: instance.dateLabels,
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
        sentiment: ['negative', 'neutral', 'positive'],
        emotion: ['anger', 'fear', 'joy', 'neutral', 'sadness']
      }
    },
    computed: {
      defaultChartData()
      {
        console.log("=== START defaultChartData() ===")

        const trendPlotData = this.$props.mediaChartData;
        const data = [];
        let facebook = false;
        let reddit = false;
        let twitter = false;
        let youtube = false;

        // All tab view
        if (this.selectedTab === 'all'){
          if (Object.keys(trendPlotData).includes('facebook')){
            facebook = true;
          }
          if (Object.keys(trendPlotData).includes('reddit')){
            reddit = true;
          }
          if (Object.keys(trendPlotData).includes('twitter')){
            twitter = true;
          }
          if (Object.keys(trendPlotData).includes('youtube')){
            youtube = true;
          }

          if (facebook === true) {
            if (this.selectedViewOption === 'Number of Mentions') {
              data.push({
                label: this.$props.mediaData.medias[1],
                data: this.$props.mediaChartData.facebook.mentions,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              });
            }
            else {
              data.push({
                label: this.$props.mediaData.medias[1],
                data: this.$props.mediaChartData.facebook.likes,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              });
            }
          } // end of facebook for all tab

          if (reddit === true) {
            if (this.selectedViewOption === 'Number of Mentions') {
              data.push({
                label: this.$props.mediaData.medias[2],
                data: this.$props.mediaChartData.reddit.mentions,
                fill: false,
                borderColor: this.colorCode.media.reddit,
                backgroundColor: this.colorCode.media.reddit,
                borderWidth: 1,
              });
            }
            else {
              data.push({
                label: this.$props.mediaData.medias[2],
                data: this.$props.mediaChartData.reddit.likes,
                fill: false,
                borderColor: this.colorCode.media.reddit,
                backgroundColor: this.colorCode.media.reddit,
                borderWidth: 1,
              });
            }
          } // end of reddit for all tab
          
          if (twitter === true) {
            if (this.selectedViewOption === 'Number of Mentions') {
              data.push({
                label: this.$props.mediaData.medias[3],
                data: this.$props.mediaChartData.twitter.mentions,
                fill: false,
                borderColor: this.colorCode.media.twitter,
                backgroundColor: this.colorCode.media.twitter,
                borderWidth: 1,
              });
            }
            else {
              data.push({
                label: this.$props.mediaData.medias[3],
                data: this.$props.mediaChartData.twitter.likes,
                fill: false,
                borderColor: this.colorCode.media.twitter,
                backgroundColor: this.colorCode.media.twitter,
                borderWidth: 1,
              });
            }
          } // end of twitter for all tab
          
          if (youtube === true) {
            if (this.selectedViewOption === 'Number of Mentions') {
              data.push({
                label: this.$props.mediaData.medias[4],
                data: this.$props.mediaChartData.youtube.mentions,
                fill: false,
                borderColor: this.colorCode.media.youtube,
                backgroundColor: this.colorCode.media.youtube,
                borderWidth: 1,
              });
            }
            else {
              data.push({
                label: this.$props.mediaData.medias[4],
                data: this.$props.mediaChartData.youtube.likes,
                fill: false,
                borderColor: this.colorCode.media.youtube,
                backgroundColor: this.colorCode.media.youtube,
                borderWidth: 1,
              });
            }
          } // end of twitter for all tab
        } // end of all tab view

        // Facebook tab view
        else if (this.selectedTab === "facebook"){
          const viewOption = this.selectedViewOption;
          // Facebook sentiments view option
          if (viewOption === 'Sentiments'){ 
            data.push(
              {
                label: this.sentiment[0],
                data: this.$props.mediaChartData.facebook.sentiments.positive,
                fill: false,
                borderColor: this.colorCode.sentiment.negative,
                backgroundColor: this.colorCode.sentiment.negative,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.sentiment[1],
                data: this.$props.mediaChartData.facebook.sentiments.neutral,
                fill: false,
                borderColor: this.colorCode.sentiment.neutral,
                backgroundColor: this.colorCode.sentiment.neutral,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.sentiment[2],
                data: this.$props.mediaChartData.facebook.sentiments.negative,
                fill: false,
                borderColor: this.colorCode.sentiment.positive,
                backgroundColor: this.colorCode.sentiment.positive,
                borderWidth: 1,
              }
            );
          }
          // Facebook emotions view option
          else if (viewOption === 'Emotions'){ 
            data.push(
              {
                label: this.emotion[0],
                data: this.$props.mediaChartData.facebook.emotions.anger,
                fill: false,
                borderColor: this.colorCode.emotion.anger,
                backgroundColor: this.colorCode.emotion.anger,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[1],
                data: this.$props.mediaChartData.facebook.emotions.fear,
                fill: false,
                borderColor: this.colorsCode.emotion.fear,
                backgroundColor: this.colorCode.emotion.fear,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[2],
                data: this.$props.mediaChartData.facebook.emotions.joy,
                fill: false,
                borderColor: this.colorsCode.emotion.joy,
                backgroundColor: this.colorCode.emotion.joy,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[3],
                data: this.$props.mediaChartData.facebook.emotions.neutral,
                fill: false,
                borderColor: this.colorsCode.emotion.neutral,
                backgroundColor: this.colorCode.emotion.neutral,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[4],
                data: this.$props.mediaChartData.facebook.emotions.sadness,
                fill: false,
                borderColor: this.colorsCode.emotion.sadness,
                backgroundColor: this.colorCode.emotion.sadness,
                borderWidth: 1,
              }
            );
          }
          // Facebook other views
          else {
            let viewData;
            if (viewOption === 'Number of Mentions'){
              viewData = this.$props.mediaChartData.facebook.mentions;
            }
            else if (viewOption === 'Number of Likes'){
              viewData = this.$props.mediaChartData.facebook.likes;
            }
            data.push(
              {
                label: this.$props.mediaData.medias[1],
                data: viewData,
                fill: false,
                borderColor: this.colorCode.media.facebook,
                backgroundColor: this.colorCode.media.facebook,
                borderWidth: 1,
              }
            );
          }
        } // end of Facebook tab view

        // Reddit tab view
        else if (this.selectedTab === "reddit"){
          const viewOption = this.selectedViewOption;
          // Reddit sentiments view option
          if (viewOption === 'Sentiments'){ 
            data.push(
              {
                label: this.sentiment[0],
                data: this.$props.mediaChartData.reddit.sentiments.positive,
                fill: false,
                borderColor: this.colorCode.sentiment.negative,
                backgroundColor: this.colorCode.sentiment.negative,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.sentiment[1],
                data: this.$props.mediaChartData.reddit.sentiments.neutral,
                fill: false,
                borderColor: this.colorCode.sentiment.neutral,
                backgroundColor: this.colorCode.sentiment.neutral,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.sentiment[2],
                data: this.$props.mediaChartData.reddit.sentiments.negative,
                fill: false,
                borderColor: this.colorCode.sentiment.positive,
                backgroundColor: this.colorCode.sentiment.positive,
                borderWidth: 1,
              }
            );
          }
          // Reddit emotions view option
          else if (viewOption === 'Emotions'){ 
            data.push(
              {
                label: this.emotion[0],
                data: this.$props.mediaChartData.reddit.emotions.anger,
                fill: false,
                borderColor: this.colorCode.emotion.anger,
                backgroundColor: this.colorCode.emotion.anger,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[1],
                data: this.$props.mediaChartData.reddit.emotions.fear,
                fill: false,
                borderColor: this.colorsCode.emotion.fear,
                backgroundColor: this.colorCode.emotion.fear,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[2],
                data: this.$props.mediaChartData.reddit.emotions.joy,
                fill: false,
                borderColor: this.colorsCode.emotion.joy,
                backgroundColor: this.colorCode.emotion.joy,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[3],
                data: this.$props.mediaChartData.reddit.emotions.neutral,
                fill: false,
                borderColor: this.colorsCode.emotion.neutral,
                backgroundColor: this.colorCode.emotion.neutral,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[4],
                data: this.$props.mediaChartData.reddit.emotions.sadness,
                fill: false,
                borderColor: this.colorsCode.emotion.sadness,
                backgroundColor: this.colorCode.emotion.sadness,
                borderWidth: 1,
              }
            );
          }
          // Reddit other views
          else {
            let viewData;
            if (viewOption === 'Number of Mentions'){
              viewData = this.$props.mediaChartData.reddit.mentions;
            }
            else if (viewOption === 'Number of Net Votes'){
              viewData = this.$props.mediaChartData.reddit.likes;
            }
            else if (viewOption === 'Number of Awards'){
              viewData = this.$props.mediaChartData.reddit.awards;
            }
            data.push(
              {
                label: this.$props.mediaData.medias[2],
                data: viewData,
                fill: false,
                borderColor: this.colorCode.media.reddit,
                backgroundColor: this.colorCode.media.reddit,
                borderWidth: 1,
              }
            );
          }
        } // end of reddit tab view

        // Twitter tab view
        else if (this.selectedTab === "twitter"){
          const viewOption = this.selectedViewOption;
          // Twitter sentiments view option
          if (viewOption === 'Sentiments'){ 
            data.push(
              {
                label: this.sentiment[0],
                data: this.$props.mediaChartData.twitter.sentiments.positive,
                fill: false,
                borderColor: this.colorCode.sentiment.negative,
                backgroundColor: this.colorCode.sentiment.negative,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.sentiment[1],
                data: this.$props.mediaChartData.twitter.sentiments.neutral,
                fill: false,
                borderColor: this.colorCode.sentiment.neutral,
                backgroundColor: this.colorCode.sentiment.neutral,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.sentiment[2],
                data: this.$props.mediaChartData.twitter.sentiments.negative,
                fill: false,
                borderColor: this.colorCode.sentiment.positive,
                backgroundColor: this.colorCode.sentiment.positive,
                borderWidth: 1,
              }
            );
          }
          // Twitter emotions view option
          else if (viewOption === 'Emotions'){ 
            data.push(
              {
                label: this.emotion[0],
                data: this.$props.mediaChartData.twitter.emotions.anger,
                fill: false,
                borderColor: this.colorCode.emotion.anger,
                backgroundColor: this.colorCode.emotion.anger,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[1],
                data: this.$props.mediaChartData.twitter.emotions.fear,
                fill: false,
                borderColor: this.colorsCode.emotion.fear,
                backgroundColor: this.colorCode.emotion.fear,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[2],
                data: this.$props.mediaChartData.twitter.emotions.joy,
                fill: false,
                borderColor: this.colorsCode.emotion.joy,
                backgroundColor: this.colorCode.emotion.joy,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[3],
                data: this.$props.mediaChartData.twitter.emotions.neutral,
                fill: false,
                borderColor: this.colorsCode.emotion.neutral,
                backgroundColor: this.colorCode.emotion.neutral,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[4],
                data: this.$props.mediaChartData.twitter.emotions.sadness,
                fill: false,
                borderColor: this.colorsCode.emotion.sadness,
                backgroundColor: this.colorCode.emotion.sadness,
                borderWidth: 1,
              }
            );
          }
          // Twitter other views
          else {
            let viewData;
            if (viewOption === 'Number of Mentions'){
              viewData = this.$props.mediaChartData.twitter.mentions;
            }
            else if (viewOption === 'Number of Likes'){
              viewData = this.$props.mediaChartData.twitter.likes;
            }
            else if (viewOption === 'Number of Retweets'){
              viewData = this.$props.mediaChartData.twitter.retweets;
            }
            data.push(
              {
                label: this.$props.mediaData.medias[3],
                data: viewData,
                fill: false,
                borderColor: this.colorCode.media.twitter,
                backgroundColor: this.colorCode.media.twitter,
                borderWidth: 1,
              }
            );
          }
        } // end of twitter tab view

        // Youtube tab view
        else if (this.selectedTab === "youtube"){
          const viewOption = this.selectedViewOption;
          // Youtube sentiments view option
          if (viewOption === 'Sentiments'){ 
            data.push(
              {
                label: this.sentiment[0],
                data: this.$props.mediaChartData.youtube.sentiments.positive,
                fill: false,
                borderColor: this.colorCode.sentiment.negative,
                backgroundColor: this.colorCode.sentiment.negative,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.sentiment[1],
                data: this.$props.mediaChartData.youtube.sentiments.neutral,
                fill: false,
                borderColor: this.colorCode.sentiment.neutral,
                backgroundColor: this.colorCode.sentiment.neutral,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.sentiment[2],
                data: this.$props.mediaChartData.youtube.sentiments.negative,
                fill: false,
                borderColor: this.colorCode.sentiment.positive,
                backgroundColor: this.colorCode.sentiment.positive,
                borderWidth: 1,
              }
            );
          }
          // Youtube emotions view option
          else if (viewOption === 'Emotions'){ 
            data.push(
              {
                label: this.emotion[0],
                data: this.$props.mediaChartData.youtube.emotions.anger,
                fill: false,
                borderColor: this.colorCode.emotion.anger,
                backgroundColor: this.colorCode.emotion.anger,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[1],
                data: this.$props.mediaChartData.youtube.emotions.fear,
                fill: false,
                borderColor: this.colorsCode.emotion.fear,
                backgroundColor: this.colorCode.emotion.fear,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[2],
                data: this.$props.mediaChartData.youtube.emotions.joy,
                fill: false,
                borderColor: this.colorsCode.emotion.joy,
                backgroundColor: this.colorCode.emotion.joy,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[3],
                data: this.$props.mediaChartData.youtube.emotions.neutral,
                fill: false,
                borderColor: this.colorsCode.emotion.neutral,
                backgroundColor: this.colorCode.emotion.neutral,
                borderWidth: 1,
              }
            );
            data.push(
              {
                label: this.emotion[4],
                data: this.$props.mediaChartData.youtube.emotions.sadness,
                fill: false,
                borderColor: this.colorsCode.emotion.sadness,
                backgroundColor: this.colorCode.emotion.sadness,
                borderWidth: 1,
              }
            );
          }
          // Youtube other views
          else {
            let viewData;
            if (viewOption === 'Number of Mentions'){
              viewData = this.$props.mediaChartData.youtube.mentions;
            }
            else if (viewOption === 'Number of Likes'){
              viewData = this.$props.mediaChartData.youtube.likes;
            }
            else if (viewOption === 'Number of Views'){
              viewData = this.$props.mediaChartData.youtube.views;
            }
            data.push(
              {
                label: this.$props.mediaData.medias[4],
                data: viewData,
                fill: false,
                borderColor: this.colorCode.media.youtube,
                backgroundColor: this.colorCode.media.youtube,
                borderWidth: 1,
              }
            );
          } // end of youtube tab view
        }

        // // Sentiments View
        // else if (this.selectedViewOption === 'Sentiments'){ 
        //   data.push({
        //       label: 'Negative',
        //       data: this.selectedChartData.positive,
        //       fill: false,
        //       borderColor: this.colorCode.sentiment.negative,
        //       backgroundColor: this.colorCode.sentiment.negative,
        //       borderWidth: 1,
        //     });
        //   data.push({
        //       label: 'Neutral',
        //       data: this.selectedChartData.neutral,
        //       fill: false,
        //       borderColor: this.colorCode.sentiment.neutral,
        //       backgroundColor: this.colorCode.sentiment.neutral,
        //       borderWidth: 1,
        //     });
        //   data.push({
        //       label: 'Positive',
        //       data: this.selectedChartData.negative,
        //       fill: false,
        //       borderColor: this.colorCode.sentiment.positive,
        //       backgroundColor: this.colorCode.sentiment.positive,
        //       borderWidth: 1,
        //     });
        // }
        // // Emotions View
        // else if (this.selectedViewOption === 'Emotions'){ 
        //   data.push({
        //       label: this.selectedTab,
        //       data: this.selectedChartData.anger,
        //       fill: false,
        //       borderColor: this.colorCode.emotion.anger,
        //       backgroundColor: this.colorCode.emotion.anger,
        //       borderWidth: 1,
        //     });
        //   data.push({
        //       label: this.selectedTab,
        //       data: this.selectedChartData.fear,
        //       fill: false,
        //       borderColor: this.colorsCode.emotion.fear,
        //       backgroundColor: this.colorCode.emotion.fear,
        //       borderWidth: 1,
        //     });
        //   data.push({
        //       label: this.selectedTab,
        //       data: this.selectedChartData.joy,
        //       fill: false,
        //       borderColor: this.colorsCode.emotion.joy,
        //       backgroundColor: this.colorCode.emotion.joy,
        //       borderWidth: 1,
        //     });
        //   data.push({
        //       label: this.selectedTab,
        //       data: this.selectedChartData.neutral,
        //       fill: false,
        //       borderColor: this.colorsCode.emotion.neutral,
        //       backgroundColor: this.colorCode.emotion.neutral,
        //       borderWidth: 1,
        //     });
        //   data.push({
        //       label: this.selectedTab,
        //       data: this.selectedChartData.sadness,
        //       fill: false,
        //       borderColor: this.colorsCode.emotion.sadness,
        //       backgroundColor: this.colorCode.emotion.sadness,
        //       borderWidth: 1,
        //     });
        // }
        // // Other Views
        // else {
        //   data.push({
        //       label: this.selectedTab,
        //       data: this.selectedChartData,
        //       fill: false,
        //       borderColor: this.selectedTabColor,
        //       backgroundColor: this.selectedTabColor,
        //       borderWidth: 1,
        //     });
        // }

        console.log("this.selectedDateLabels", this.selectedDateLabels)
        return {
          labels: this.selectedDateLabels,
          datasets: data,
        };

        // return {
        //   labels: this.selectedDateLabels,
        //   datasets: [
        //     {
        //       label: this.$props.mediaData.medias[1],
        //       data: this.$props.mediaChartData.facebook.mentions,
        //       fill: false,
        //       borderColor: this.colorCode.media.facebook,
        //       backgroundColor: this.colorCode.media.facebook,
        //       borderWidth: 1,
        //     },
        //     // {
        //     //   label: this.$props.mediaData.medias[2],
        //     //   data: this.$props.mediasMetrics.reddit.mentions,
        //     //   fill: false,
        //     //   borderColor: this.colorCode.media.reddit,
        //     //   backgroundColor: this.colorCode.media.reddit,
        //     //   borderWidth: 1,
        //     // },
        //     // {
        //     //   label: this.$props.mediaData.medias[3],
        //     //   data: this.$props.mediasMetrics.facebook.mentions,
        //     //   fill: false,
        //     //   borderColor: this.colorCode.media.facebook,
        //     //   backgroundColor: this.colorCode.media.facebook,
        //     //   borderWidth: 1,
        //     // },
        //     // {
        //     //   label: this.$props.mediaData.medias[4],
        //     //   data: this.$props.mediasMetrics.facebook.mentions,
        //     //   fill: false,
        //     //   borderColor: this.colorCode.media.facebook,
        //     //   backgroundColor: this.colorCode.media.facebook,
        //     //   borderWidth: 1,
        //     // },
        //   ]
        // };
      } // end of default chart data

      
    }, // end of computed
    methods:{
      reset(media)
      {
        console.log("=== START reset() ===")
        console.log("media", media)
        this.selectedTab = media;
        
        // 'number of mentions' is the default selection for all tabs 
        // this.selectedViewOption = 'Number of Mentions';

        // change view options and chart data
        // if (this.selectedTab === 'all'){
        //   this.selectedViewList = this.$props.mediaData.mediaView.all;
        //   // this.selectedChartData = this.$props.mediaChartData.all.mentions;
        // }   
        // if (this.selectedTab === 'facebook'){
        //   this.selectedViewList = this.$props.mediaData.mediaView.facebook;
        //   // this.selectedChartData = this.$props.mediaChartData.facebook.mentions;
        // }
        // else if (this.selectedTab === 'reddit'){
        //   this.selectedViewList = this.$props.mediaData.mediaView.reddit;
        //   // this.selectedChartData = this.$props.mediaChartData.reddit.mentions;
        // }
        // else if (this.selectedTab === 'twitter'){
        //   this.selectedViewList = this.$props.mediaData.mediaView.twitter;
        //   // this.selectedChartData = this.$props.mediaChartData.twitter.mentions;
        // }
        // else if (this.selectedTab === 'youtube'){
        //   this.selectedViewList = this.$props.mediaData.mediaView.youtube;
        //   // this.selectedChartData = this.$props.mediaChartData.youtube.mentions;
        // }
        
        this.getChartData();
        console.log("=== END reset() ===")
      },
      changeViewOption(selectedViewOption)
      {
        console.log("=== START changeViewOption() ===")
        console.log(selectedViewOption)
        console.log(this.selectedViewOption);
        this.selectedViewOption = selectedViewOption;
        console.log(this.selectedViewOption);
        this.getChartData();
        // this.changeChart();
        console.log("=== END changeViewOption() ===")
      },
      changeChart()
      {
        console.log("=== START changeChart() ===")
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
        console.log("this.selectedTab", this.selectedTab)
        console.log("this.selectedViewOption", this.selectedViewOption)
        console.log("this.selectedChartData", this.selectedChartData)
        console.log("this.$props.mediaChartData.facebook.mentions", this.$props.mediaChartData.facebook.mentions)
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
          this.selectedTabColor = this.colorCode.media.facebook;
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
          this.selectedTabColor = this.colorCode.media.reddit;
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
          this.selectedTabColor = this.colorCode.media.twitter;
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
          this.selectedTabColor = this.colorCode.media.youtube;
        }
        
        // this.formatChartDataset();
        // this.getChartData();
        console.log("=== END changeChart() ===")
      },

      getChartData() {
        console.log("=== START getChartData() ===")
        console.log("this.formattedChartData 1", this.formattedChartData)
        console.log("this.defaultChartData", this.defaultChartData)
        this.formattedChartData = this.defaultChartData;
        console.log("this.formattedChartData 2", this.formattedChartData);
        // console.log(this.colorCode.medias.facebook);
      }

      // formatChartDataset()
      // {
      //   console.log("=== START formatChartDataset() ===")

      //   if (this.selectedTab === 'all'){
      //     this.allChartData();
      //   }
      //   // Sentiment View
      //   else if (this.selectedViewList === 'Sentiments'){ 
      //     this.formattedChartData = {
      //       labels: this.selectedDateLabels,
      //       datasets: [
      //         {
      //           label: 'Negative',
      //           data: this.selectedChartData.positive,
      //           fill: false,
      //           borderColor: this.colorCode.sentiment.negative,
      //           backgroundColor: this.colorCode.sentiment.negative,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: 'Neutral',
      //           data: this.selectedChartData.neutral,
      //           fill: false,
      //           borderColor: this.colorCode.sentiment.neutral,
      //           backgroundColor: this.colorCode.sentiment.neutral,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: 'Positive',
      //           data: this.selectedChartData.negative,
      //           fill: false,
      //           borderColor: this.colorCode.sentiment.positive,
      //           backgroundColor: this.colorCode.sentiment.positive,
      //           borderWidth: 1,
      //         },
      //       ]
      //     }
      //   }
      //   // Emotions View
      //   else if (this.selectedViewList === 'Emotions'){ 
      //     this.formattedChartData = {
      //       labels: this.selectedDateLabels,
      //       datasets: [
      //         {
      //           label: this.selectedTab,
      //           data: this.selectedChartData.anger,
      //           fill: false,
      //           borderColor: this.colorCode.emotion.anger,
      //           backgroundColor: this.colorCode.emotion.anger,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.selectedTab,
      //           data: this.selectedChartData.fear,
      //           fill: false,
      //           borderColor: this.colorsCode.emotion.fear,
      //           backgroundColor: this.colorCode.emotion.fear,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.selectedTab,
      //           data: this.selectedChartData.joy,
      //           fill: false,
      //           borderColor: this.colorsCode.emotion.joy,
      //           backgroundColor: this.colorCode.emotion.joy,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.selectedTab,
      //           data: this.selectedChartData.neutral,
      //           fill: false,
      //           borderColor: this.colorsCode.emotion.neutral,
      //           backgroundColor: this.colorCode.emotion.neutral,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.selectedTab,
      //           data: this.selectedChartData.sadness,
      //           fill: false,
      //           borderColor: this.colorsCode.emotion.sadness,
      //           backgroundColor: this.colorCode.emotion.sadness,
      //           borderWidth: 1,
      //         }
      //       ]
      //     }
      //   }
      //   // Other Views
      //   else {
      //     this.formattedChartData = {
      //       labels: this.selectedDateLabels,
      //       datasets: [
      //         {
      //           label: this.selectedTab,
      //           data: this.selectedChartData,
      //           fill: false,
      //           borderColor: this.selectedTabColor,
      //           backgroundColor: this.selectedTabColor,
      //           borderWidth: 1,
      //         },
      //       ]
      //     }
      //   }
      //   console.log("=== END formatChartDataset() ===")
      // },
      // allChartData()
      // {
      //   console.log("=== START allChartData() ===")

      //   if (this.selectedViewOption === 'Number of Mentions') {
      //     this.formattedChartData = {
      //       labels: [],
      //       datasets: [
      //         {
      //           label: this.$props.mediaData.medias[1],
      //           data: this.$props.mediaChartData.facebook.mentions,
      //           fill: false,
      //           borderColor: this.colorCode.media.facebook,
      //           backgroundColor: this.colorCode.media.facebook,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.$props.mediaData.medias[2],
      //           data: this.$props.mediaChartData.reddit.mentions,
      //           fill: false,
      //           borderColor: this.colorCode.media.reddit,
      //           backgroundColor: this.colorCode.media.reddit,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.$props.mediaData.medias[3],
      //           data: this.$props.mediaChartData.facebook.mentions,
      //           fill: false,
      //           borderColor: this.colorCode.media.facebook,
      //           backgroundColor: this.colorCode.media.facebook,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.$props.mediaData.medias[4],
      //           data: this.$props.mediaChartData.facebook.mentions,
      //           fill: false,
      //           borderColor: this.colorCode.media.facebook,
      //           backgroundColor: this.colorCode.media.facebook,
      //           borderWidth: 1,
      //         },
      //       ]
      //     };
      //   }
      //   else {
      //     this.formattedChartData = {
      //       labels: [],
      //       datasets: [
      //         {
      //           label: this.$props.mediaData.medias[1],
      //           data: this.$props.mediaChartData.facebook.likes,
      //           fill: false,
      //           borderColor: this.colorCode.media.facebook,
      //           backgroundColor: this.colorCode.media.facebook,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.$props.mediaData.medias[2],
      //           data: this.$props.mediaChartData.reddit.likes,
      //           fill: false,
      //           borderColor: this.colorCode.media.reddit,
      //           backgroundColor: this.colorCode.media.reddit,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.$props.mediaData.medias[3],
      //           data: this.$props.mediaChartData.facebook.likes,
      //           fill: false,
      //           borderColor: this.colorCode.media.facebook,
      //           backgroundColor: this.colorCode.media.facebook,
      //           borderWidth: 1,
      //         },
      //         {
      //           label: this.$props.mediaData.medias[4],
      //           data: this.$props.mediaChartData.facebook.likes,
      //           fill: false,
      //           borderColor: this.colorCode.media.facebook,
      //           backgroundColor: this.colorCode.media.facebook,
      //           borderWidth: 1,
      //         },
      //       ]
      //     };
      //   }
      //   console.log("=== END allChartData() ===")
      // },
    }, // end of methods
    mounted () {
      this.getChartData();
    }
  }
</script>

<style>
  .chartBox {
    width: 800px;
    height: 420px;
  }
</style>