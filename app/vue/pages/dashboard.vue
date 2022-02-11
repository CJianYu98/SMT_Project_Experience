<template>
  <div>
    <SearchFilters @changeFilter="rerenderDashboard"/>
    <v-row>
      <v-col cols="4">
        <TrendingTopics :top-five-topics="topFiveTopicsData" @clickQuery="updateDashboardWithQuery"/>
      </v-col>
      <v-col cols="8">
        <TrendAnalysis/>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import TrendingTopics from '@/components/TrendingTopics.vue'
import SearchFilters from '@/components/SearchFilters'
import TrendAnalysis from '../components/TrendAnalysis.vue'
export default {
  components: { 
    TrendingTopics,            
    SearchFilters,
    TrendAnalysis,
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
        name: 'GE2020', 
        mentions: 294940, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'GE2024', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'GST Increase', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'SG Rediscover Vouchers', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'Reesah Khan', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      }
    ],
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
        name: 'ABC NEW TOPIC 1', 
        mentions: 294940, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'ABC NEW TOPIC 2', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'GST Increase', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'SG Rediscover Vouchers', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      },
      {
        name: 'Reesah Khan', 
        mentions: 29494, 
        sentiment: {
          negative: 0.2, neutral: 0.6, positive: 0.2
        }
      }
      ]


      console.log("=== END rerenderDashboard ===")
    },

    updateDashboardWithQuery(query) {
      console.log("=== START updateDashboardWithQuery() ===")
      console.log(query)
      // need to call multiple apis to call with query
      // should be done from the main dashboard page
      console.log("=== END updateDashboardWithQuery() ===")
    }
  }
  
}
</script>


<style>

</style>
