<template>
  <div class="mb-10">
    <SearchFilters @changeFilter="rerenderDashboard" :selected-trending-query="selectedTrendingQuery"/>
    <!--  align="stretch" in v-row works with d-flex in v-col -->
    <v-row>
      <v-col cols="4">
        <TrendingTopics 
          :top-five-topics="topFiveTopicsData" 
          @clickQuery="updateDashboardWithQuery" @selectedTrendingTopicInDashboard="passTrendingTopicsToDashboard" 
        />
      </v-col>
      <v-col cols="8">
        <TrendAnalysis 
          :overall-stats="overallStatsData" 
          :platform-data="platformMetricsData"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <KeywordCard
          :keywords-word-cloud="keywords" 
          :keywords-word-cloud-legend="keywordsWordCloudLegend"
        />
      </v-col>
      <v-col cols="7">
        <!-- <KeywordAnalysis /> -->
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <!-- <NoteworthyComments /> -->
      </v-col>
      <v-col cols="7">

      </v-col>      
    </v-row>
  </div>
</template>

<script>
import TrendAnalysis from '../components/TrendAnalysis.vue'
import KeywordCard from '../components/KeywordCard.vue'
// import KeywordAnalysis from '../components/KeywordAnalysis.vue'
// import NoteworthyComments from '../components/NoteworthyComments.vue'
import TrendingTopics from '@/components/TrendingTopics.vue'
import SearchFilters from '@/components/SearchFilters'
export default {
  name: 'DashBoard',
  components: { 
    TrendingTopics,            
    SearchFilters,
    TrendAnalysis,
    KeywordCard,
    // KeywordAnalysis,
    // NoteworthyComments,
  },
  data: () => ({
    allData: [
      {
        name: 'GE2020', 
        mentions: 294940, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        },
        post: 'GE2020 could have gone better',
        comment: `Couldn't have agreed more`,
        likeCount: 200,
        commentCount: 198,
        shareCount: 56,
        categories: ['Politics'],
      },
      {
        name: 'GE2024', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        },
        post: 'Looking forward to 2024',
        comment: `Couldn't have agreed more`,
        likeCount: 200,
        commentCount: 198,
        shareCount: 56,
        categories: ['Politics'],
      },
    ],
    topFiveTopicsData: [
      {
        name: 'Politics',
        topThreeMentions: ['0.5X Long Algorand Token', '0cash', 'RealT Token - 11078 Longview St, Detroit, MI 48213'],
        mentions: 294940, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'Economics',
        topThreeMentions: ['GST Increase', 'STI', 'Taxes'], 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'Environment',
        topThreeMentions: ['Tengah Forest', 'Plastic Bags', 'Carbon Tax'], 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'Travel',
        topThreeMentions: ['SG Rediscover Vouchers', 'ART test', 'VTL'], 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'Education',
        topThreeMentions: ['PSLE results', 'O Level results', 'June holidays'], 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      }
    ],
    overallStatsData: {
      posts: 2940490,
      trend: 0.4,
      comments: 93893,
      likes: 93398,
      shares: 2732
    },
    platformMetricsData: {
      Facebook: {
        mentions: 0.24,
        trend: -0.2
      },
      Instagram: {
        mentions: 0.34,
        trend: -0.4
      },
      Reddit: {
        mentions: 0.14,
        trend: 0.2
      },
      Twitter: {
        mentions: 0.08,
        trend: 0.2
      },
      Youtube: {
        mentions: 0.20,
        trend: -0.2
      }
    },
    keywords: [
      {word: "Running", size: "10", sentiment: "positive"}, 
      {word: "Surfing", size: "20", sentiment: "neutral"}, 
      {word: "Climbing", size: "50", sentiment: "negative"}, 
      {word: "Kiting", size: "30", sentiment: "positive"}, 
      {word: "Sailing", size: "20", sentiment: "negative"}, 
      {word: "Snowboarding", size: "60", sentiment: "neutral"} 
    ],
    keywordsWordCloudLegend: {
      positive: "#78D549",
      neutral: "#EFB727",
      negative: "#EB8159"
    },
    selectedTrendingQuery: "", 
  }),

  computed: {
    // get top 5 topics
    // getTopGiveTopics(){
    //     return 
    // }
  },

  methods: {
    rerenderDashboard(updatedSentiments) {
      // code to rerender dashboard when the filters are selected, by passing them to the api
      console.log("=== START rerenderDashboard ===")
      console.log(updatedSentiments)
      // axios.get('/login', {
      //   firstName: 'Finn',
      //   lastName: 'Williams'
      // })
      // .then((response) => {
      //   console.log(response);
      // }, (error) => {
      //   console.log(error);
      // })

      this.topFiveTopicsData = [
        {
          name: 'Healthcare',
          topThreeMentions: ['GE2020', 'GE2024', 'Reesah Khan'],
          mentions: 294940, 
          sentiment: {
            negative: 0.2, neutral: 0.6, positive: 0.2
          }
        },
        {
          name: 'Economics',
          topThreeMentions: ['GST Increase', 'STI', 'Taxes'], 
          mentions: 29494, 
          sentiment: {
            negative: 0.2, neutral: 0.6, positive: 0.2
          }
        },
        {
          name: 'Environment',
          topThreeMentions: ['Tengah Forest', 'Plastic Bags', 'Carbon Tax'], 
          mentions: 29494, 
          sentiment: {
            negative: 0.2, neutral: 0.6, positive: 0.2
          }
        },
        {
          name: 'Travel',
          topThreeMentions: ['SG Rediscover Vouchers', 'ART test', 'VTL'], 
          mentions: 29494, 
          sentiment: {
            negative: 0.2, neutral: 0.6, positive: 0.2
          }
        },
        {
          name: 'Education',
          topThreeMentions: ['PSLE results', 'O Level results', 'June holidays'], 
          mentions: 29494, 
          sentiment: {
            negative: 0.2, neutral: 0.6, positive: 0.2
          }
        }
      ]

      this.overallStatsData = {
        posts: 12,
        trend: 0.4,
        comments: 93893,
        likes: 93398,
        shares: 2732
      }

      this.platformMetricsData = {
        facebook: {
          mentions: 0.54,
          trend: 0.98
        },
        instagram: {
          mentions: 0.34,
          trend: -0.4
        },
        reddit: {
          mentions: 0.14,
          trend: 0.2
        },
        twitter: {
          mentions: 0.08,
          trend: 0.2
        },
        youtube: {
          mentions: 0.20,
          trend: -0.2
        }
      }

      this.keywords = [
        {word: "Chocolate", size: "10", sentiment: "positive"}, 
        {word: "Chicken Rice", size: "20", sentiment: "neutral"}, 
        {word: "Bingsoo", size: "50", sentiment: "negative"}, 
        {word: "Kiting", size: "30", sentiment: "positive"}, 
        {word: "Sailing", size: "20", sentiment: "negative"}, 
        {word: "Snowboarding", size: "60", sentiment: "neutral"} 
      ]


      console.log("=== END rerenderDashboard ===")
    },

    updateDashboardWithQuery(query) {
      console.log("=== START updateDashboardWithQuery() ===")
      console.log(query)
      // need to call multiple apis to call with query
      // should be done from the main dashboard page
      console.log("=== END updateDashboardWithQuery() ===")
    },

    passTrendingTopicsToDashboard(topic) {
      console.log("=== START passTrendingTopicsToDashboard() ===")
      console.log(topic)
      this.selectedTrendingQuery = topic
      console.log("this.selectedTrendingQuery", this.selectedTrendingQuery)
      console.log("=== END passTrendingTopicsToDashboard() ===")
    }
  }
  
}
</script>


<style>

</style>
