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
      <v-col cols="4">
        <KeywordCard
          :keywords-word-cloud="keywords" 
          :keywords-word-cloud-legend="keywordsWordCloudLegend"
        />
      </v-col>
      <v-col cols="8">
        <ComplaintsCard 
          :complaints-word-cloud="complaintsKeywords"
          :complaints-related-comments="complaintsRelatedComments"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <!-- <NoteworthyComments /> -->
      </v-col>
      <v-col cols="7">
        <!-- <KeywordAnalysis /> -->
      </v-col>      
    </v-row>
  </div>
</template>

<script>
import TrendAnalysis from '../components/TrendAnalysis.vue'
import KeywordCard from '../components/KeywordWordCloudCard.vue'
// import KeywordAnalysis from '../components/KeywordAnalysisCard.vue'
// import NoteworthyComments from '../components/NoteworthyComments.vue'
import ComplaintsCard from '../components/ComplaintsCard.vue'
import TrendingTopics from '@/components/TrendingTopics.vue'
import SearchFilters from '@/components/SearchFilters'
export default {
  name: 'DashBoard',
  components: { 
    TrendingTopics,            
    SearchFilters,
    TrendAnalysis,
    KeywordCard,
    // KeywordAnalysis,,
    ComplaintsCard
    // NoteworthyComments,
  },
  data: () => ({
    fakeData: {
        defaultFilters: {
          topFiveTopicsData: [
            {
              name: "test1",
              topThreeMentions: ["test1", "test2", "test3"],
              mentions: 294940, 
              sentiment: [
                  {
                    sentiment: "negative",
                    percentage: 0.2,
                    count: 58988
                  },
                  {
                    sentiment: "neutral",
                    percentage: 0.6,
                    count: 176946
                  },
                  {
                    sentiment: "positive",
                    percentage: 0.2,
                    count: 58988
                  },
                ],
            }
          ]
        },
    },
    topFiveTopicsData: [
      {
        name: 'Bitcoin',
        topThreeMentions: ['0.5X Long Algorand Token', '0cash', 'RealT Token - 11078 Longview St, Detroit, MI 48213'],
        mentions: 294940, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.2,
              count: 58988
            },
            {
              sentiment: "neutral",
              percentage: 0.6,
              count: 176946
            },
            {
              sentiment: "positive",
              percentage: 0.2,
              count: 58988
            },
          ],
      },
      {
        name: 'Economics',
        topThreeMentions: ['GST Increase', 'STI', 'Taxes'], 
        mentions: 29494, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.2,
              count: 58988
            },
            {
              sentiment: "neutral",
              percentage: 0.6,
              count: 176946
            },
            {
              sentiment: "positive",
              percentage: 0.2,
              count: 58988
            },
          ],
      },
      {
        name: 'Environment',
        topThreeMentions: ['Tengah Forest', 'Plastic Bags', 'Carbon Tax'], 
        mentions: 29494, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.2,
              count: 58988
            },
            {
              sentiment: "neutral",
              percentage: 0.6,
              count: 176946
            },
            {
              sentiment: "positive",
              percentage: 0.2,
              count: 58988
            },
          ],
      },
      {
        name: 'Travel',
        topThreeMentions: ['SG Rediscover Vouchers', 'ART test', 'VTL'], 
        mentions: 29494, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.2,
              count: 58988
            },
            {
              sentiment: "neutral",
              percentage: 0.6,
              count: 176946
            },
            {
              sentiment: "positive",
              percentage: 0.2,
              count: 58988
            },
          ],
      },
      {
        name: 'Education',
        topThreeMentions: ['PSLE results', 'O Level results', 'June holidays'], 
        mentions: 29494, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.2,
              count: 58988
            },
            {
              sentiment: "neutral",
              percentage: 0.6,
              count: 176946
            },
            {
              sentiment: "positive",
              percentage: 0.2,
              count: 58988
            },
          ],
      }
    ],
    overallStatsData: {
      posts: 2940490,
      trend: 0,
      comments: 93893,
      likes: 93398,
      shares: 2732,
      filters: {
        date: ["All"],
      }
    },
    platformMetricsData: {
      Facebook: {
        mentions: 0.24,
        trend: -0.2
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
        mentions: 0.54,
        trend: -0.2
      }
    },
    keywords: [
      {word: "Running", size: "10", sentiment: "positive", hover: "10"}, 
      {word: "Surfing", size: "20", sentiment: "neutral", hover: "20"}, 
      {word: "Climbing", size: "50", sentiment: "negative", hover: "50"}, 
      {word: "Kiting", size: "30", sentiment: "positive", hover: "30"}, 
      {word: "Sailing", size: "20", sentiment: "negative", hover: "20"}, 
      {word: "Snowboarding", size: "60", sentiment: "neutral", hover: "60"} 
    ],
    complaintsKeywords: [
      {word: "Running", size: "10", hover: "10"}, 
      {word: "Surfing", size: "20", hover: "20"}, 
      {word: "Hot", size: "50", hover: "50"}, 
      {word: "Kiting", size: "30", hover: "30"}, 
      {word: "Sailing", size: "20", hover: "20"}, 
      {word: "Snowboarding", size: "60", hover: "60"} 
    ],
    complaintsRelatedComments: [
      {
        media: 'facebook',
        likes: '65,000',
        date: '21 December 2021',
        comment: 'The dreadful breakthrough infection can effectively be prevented with VCO/Lauric Acid, and total community viral load can be lowered, do not play dice with Covid, try to protect the community and your loved ones at the same time.',
        topic: 'Healthcare'
      },
      {
        media: 'facebook',
        likes: '23,000',
        date: '22 December 2021',
        comment: 'The dreadful breakthrough infection can effectively be prevented with VCO/Lauric Acid, and total community viral load can be lowered, do not play dice with Covid, try to protect the community and your loved ones at the same time.',
        topic: 'Healthcare'
      },
    ],
    keywordsWordCloudLegend: {
      positive: "#78D549",
      neutral: "#EFB727",
      negative: "#EB8159"
    },
    selectedTrendingQuery: "", 
    // dateSelected: 
  }),

  computed: {
    // get top 5 topics
    // getTopGiveTopics(){
    //     return 
    // }
  },

  // mounted(): {
  //   this.checkFilterSelectionToReturnFakeData(updatedSentiments)
  // },

  methods: {
    rerenderDashboard(updatedSentiments) {
      // code to rerender dashboard when the filters are selected, by passing them to the api
      console.log("=== START rerenderDashboard ===")
      console.log("rerenderDashboard updatedSentiments", updatedSentiments)

      let filterCheck = this.checkFilterSelectionToReturnFakeData(updatedSentiments)

      if (filterCheck == null) {
        filterCheck = "defaultFilters"
      }

      console.log("filterCheck", filterCheck)
      // console.log("query", query)
      // console.log("filterSelection", filterSelection)
      console.log("this.fakeData", this.fakeData)

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
          sentiment: [
            {
              sentiment: "negative",
              percentage: 0,
              count: 0
            },
            {
              sentiment: "neutral",
              percentage: 0,
              count: 0
            },
            {
              sentiment: "positive",
              percentage: 1,
              count: 294940
            },
          ],
        },
        {
          name: 'DiffName',
          topThreeMentions: ['GST Increase', 'STI', 'Taxes'], 
          mentions: 29494, 
          sentiment: [
            {
              sentiment: "negative",
              percentage: 0,
              count: 0
            },
            {
              sentiment: "neutral",
              percentage: 1,
              count: 294940
            },
            {
              sentiment: "positive",
              percentage: 0,
              count: 0
            },
          ],
        },
        {
          name: 'Environment',
          topThreeMentions: ['Tengah Forest', 'Plastic Bags', 'Carbon Tax'], 
          mentions: 29494, 
          sentiment: [
            {
              sentiment: "negative",
              percentage: 1,
              count: 294940
            },
            {
              sentiment: "neutral",
              percentage: 0,
              count: 0
            },
            {
              sentiment: "positive",
              percentage: 0,
              count: 0
            },
          ],
        },
        {
          name: 'Travel',
          topThreeMentions: ['SG Rediscover Vouchers', 'ART test', 'VTL'], 
          mentions: 29494, 
          sentiment: [
            {
              sentiment: "negative",
              percentage: 0.2,
              count: 58988
            },
            {
              sentiment: "neutral",
              percentage: 0.6,
              count: 176946
            },
            {
              sentiment: "positive",
              percentage: 0.2,
              count: 58988
            },
          ],
        },
        {
          name: 'Education',
          topThreeMentions: ['PSLE results', 'O Level results', 'June holidays'], 
          mentions: 29494, 
          sentiment: [
            {
              sentiment: "negative",
              percentage: 0.2,
              count: 58988
            },
            {
              sentiment: "neutral",
              percentage: 0.6,
              count: 176946
            },
            {
              sentiment: "positive",
              percentage: 0.2,
              count: 58988
            },
          ],
        }
      ]

      this.overallStatsData = {
        posts: 12,
        trend: 0.4,
        comments: 93893,
        likes: 93398,
        shares: 2732,
        filters: {
          date: ["All"],
        }
      }

      this.platformMetricsData = {
        facebook: {
          mentions: 0.54,
          trend: 0.98
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
        {word: "Chocolate", size: "10", sentiment: "positive", hover: "9210"}, 
        {word: "Chicken Rice", size: "20", sentiment: "neutral", hover: "9210"}, 
        {word: "Bingsoo", size: "50", sentiment: "negative", hover: "9210"}, 
        {word: "Kiting", size: "30", sentiment: "positive", hover: "9210"}, 
        {word: "Sailing", size: "20", sentiment: "negative", hover: "9210"}, 
        {word: "Snowboarding", size: "60", sentiment: "neutral", hover: "9210"} 
      ]

      this.complaintsKeywords = [
      {word: "Running", size: "10", hover: "9210"}, 
      {word: "Surfing", size: "20", hover: "9210"}, 
      {word: "Rain", size: "50", hover: "9210"}, 
      {word: "Kiting", size: "30", hover: "9210"}, 
      {word: "Sailing", size: "20", hover: "9210"}, 
      {word: "Queue", size: "60", hover: "9210"} 
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
    },

    checkFilterSelectionToReturnFakeData(filters) {
      console.log("=== START checkFilterSelectionToReturnFakeData ====")
      console.log("filters", filters)

      const dateSelection = filters[0]
      const platformSelection = filters[1]
      const sentSelection =  filters[2]
      const emotionSelection = filters[3]

      // console.log("query", query)
      // console.log("dateSelection", dateSelection)
      // console.log("platformSelection", platformSelection)
      // console.log("sentSelection", sentSelection)
      // console.log("emotionSelection", emotionSelection)

      if (dateSelection==="Past 7 Days" && platformSelection.length===4 && sentSelection.length===3 && emotionSelection.length===5) {
        console.log("inside if loop")
        console.log("default filters")
        return ["covid","defaultFilters"]
      } else {
        console.log("inside else loop")
      }

    }
  }
  
}
</script>


<style>

</style>
