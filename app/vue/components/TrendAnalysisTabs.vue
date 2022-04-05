<template>
  <v-card>
    <v-tabs
        v-model="tabs"
        centered
    >
        <v-tab
            v-for="media in medias"
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
          v-for="platform in mediasMetrics" 
          :key="platform.view"
        >
          <v-card flat>
            <v-container fluid class="px-4 mt-n4 pb-0">
              <v-row no-gutters align="stretch">
                <v-col class="d-flex">
                  <v-card-title class="text-h5">
                    {{ selectedViewOption }}
                  </v-card-title>
                  <v-spacer></v-spacer>
                  <DropDownSelect 
                  :viewFilter="selectedViewList" 
                  :viewSelected="selectedViewOption"
                  @changeView="changeViewOption($event)"
                  :label="label">
                  </DropDownSelect>
                </v-col>
              </v-row>
            </v-container>
          </v-card>
          <v-card>
            <line-chart class="chartBox" :data="selectedChartData"></line-chart>  
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
      medias: {
        type: Array,
        required: true
      },
      mediasMetrics: {
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
        selectedTab: instance.medias[0],
        selectedViewList: instance.mediasMetrics.all.view,
        selectedViewOption: instance.mediasMetrics.all.view[0],
        selectedChartData: instance.mediasMetrics.all.data_mentions,
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
          this.selectedViewList = this.$props.mediasMetrics.all.view;
          this.selectedChartData = this.$props.mediasMetrics.all.data_mentions;
        }   
        else if (this.selectedTab === 'facebook'){
          this.selectedViewList = this.$props.mediasMetrics.facebook.view;
          this.selectedChartData = this.$props.mediasMetrics.facebook.data_mentions;
        }
        else if (this.selectedTab === 'reddit'){
          this.selectedViewList = this.$props.mediasMetrics.reddit.view;
          this.selectedChartData = this.$props.mediasMetrics.reddit.data_mentions;
        }
        else if (this.selectedTab === 'twitter'){
          this.selectedViewList = this.$props.mediasMetrics.twitter.view;
          this.selectedChartData = this.$props.mediasMetrics.twitter.data_mentions;
        }
        else if (this.selectedTab === 'youtube'){
          this.selectedViewList = this.$props.mediasMetrics.youtube.view;
          this.selectedChartData = this.$props.mediasMetrics.youtube.data_mentions;
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
        if (this.selectedTab === 'all'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediasMetrics.all.data_mentions;
          } 
          else if (this.selectedViewOption === 'Number of Likes'){            
            this.selectedChartData = this.$props.mediasMetrics.all.data_likes;
          }
        }
        // Facebook tab
        else if (this.selectedTab === 'facebook'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediasMetrics.facebook.data_mentions;
          } 
          else if (this.selectedViewOption === 'Number of Likes'){            
            this.selectedChartData = this.$props.mediasMetrics.facebook.data_likes;
          }
          else if (this.selectedViewOption === 'Number of Shares'){            
            this.selectedChartData = this.$props.mediasMetrics.facebook.data_shares;
          }
          else if (this.selectedViewOption === 'Sentiments'){            
            this.selectedChartData = this.$props.mediasMetrics.facebook.data_sentiments;
          }
        }
        // Reddit tab
        else if (this.selectedTab === 'reddit'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediasMetrics.reddit.data_mentions;
          } 
          else if (this.selectedViewOption === 'Number of Net Votes'){            
            this.selectedChartData = this.$props.mediasMetrics.reddit.data_net_votes;
          }
          else if (this.selectedViewOption === 'Number of Awards'){            
            this.selectedChartData = this.$props.mediasMetrics.reddit.data_awards;
          }
          else if (this.selectedViewOption === 'Sentiments'){            
            this.selectedChartData = this.$props.mediasMetrics.reddit.data_sentiments;
          }
        }
        // Twitter tab
        else if (this.selectedTab === 'twitter'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediasMetrics.twitter.data_mentions;
          } 
          else if (this.selectedViewOption === 'Number of Likes'){            
            this.selectedChartData = this.$props.mediasMetrics.twitter.data_likes;
          }
          else if (this.selectedViewOption === 'Number of Replies'){            
            this.selectedChartData = this.$props.mediasMetrics.twitter.data_replies;
          }
          else if (this.selectedViewOption === 'Sentiments'){            
            this.selectedChartData = this.$props.mediasMetrics.twitter.data_sentiments;
          }
        }
        // Youtube tab
        else if (this.selectedTab === 'youtube'){
          if (this.selectedViewOption === 'Number of Mentions'){
            this.selectedChartData = this.$props.mediasMetrics.youtube.data_mentions;
          } 
          else if (this.selectedViewOption === 'Number of Likes'){            
            this.selectedChartData = this.$props.mediasMetrics.youtube.data_likes;
          }
          else if (this.selectedViewOption === 'Number of Views'){            
            this.selectedChartData = this.$props.mediasMetrics.youtube.data_views;
          }
          else if (this.selectedViewOption === 'Sentiments'){            
            this.selectedChartData = this.$props.mediasMetrics.youtube.data_sentiments;
          }
        }
      }
    },
  }
</script>

<style>
  .chartBox {
    width: 800px;
    height: 360px;
  }
</style>