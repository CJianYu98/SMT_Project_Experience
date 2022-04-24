<template>
  <div class="mb-15">
    <SearchFilters @changeFilter="rerenderDashboard" :selected-trending-query="selectedTrendingQuery"/>
    <p>{{testData}}</p>
    <v-row>
      <v-col cols="4">
        <TrendingTopics
          :pending-state="$fetchState.pending"
          :top-five-topics="topFiveTopicsData" 
          :keywords-word-cloud-legend="keywordsWordCloudLegend"
          :trending-topics-emotions-legend="trendingTopicsEmotionsLegend"
          @clickQuery="updateDashboardWithQuery"
        />
      </v-col>
      <v-col cols="8">
        <TrendAnalysis
          :pending-state="$fetchState.pending"
          :overall-stats="overallStatsData"
          :platform-metrics="platformMetrics"
          :all-trend="allTrend"
          :platform-trend="platformTrend"
          :media-data="mediaData"
          :media-chart-data="mediaChartData"
          :selected-date-filter="dateFilter"
          :sentiment-colors="keywordsWordCloudLegend"
          :emotion-colors="trendingTopicsEmotionsLegend"
          :date-labels="dateLabels"
          :selected-media="selectedMedia"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4">
        <KeywordCard
          :pending-state="$fetchState.pending"
          :keywords-word-cloud="keywords" 
          :keywords-word-cloud-legend="keywordsWordCloudLegend"
        />
      </v-col>
      <v-col cols="8">
        <NoteworthyPosts
          :pending-state="$fetchState.pending"
          :related-posts="noteworthyPosts"
          :noteworthy-top-topics="noteworthyTopTopics"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4">
        <PlaceholderCard/>
      </v-col>
      <v-col cols="8">
        <ComplaintsCard
          :pending-state="$fetchState.pending"
          :complaints-word-cloud="complaintsKeywords"
          :related-posts="complaintsRelatedPosts"
        />
      </v-col>      
    </v-row>
  </div>
</template>

<script>
import TrendAnalysis from '../components/TrendAnalysis.vue'
import KeywordCard from '../components/KeywordWordCloudCard.vue'
// import KeywordAnalysis from '../components/KeywordAnalysisCard.vue'
import NoteworthyPosts from '../components/NoteworthyPosts.vue'
import ComplaintsCard from '../components/ComplaintsCard.vue'
import TrendingTopics from '@/components/TrendingTopicsCard.vue'
import SearchFilters from '@/components/SearchFilters'
import PlaceholderCard from '@/components/PlaceholderCard'
export default {
  name: 'DashBoard',
  components: { 
    TrendingTopics,            
    SearchFilters,
    TrendAnalysis,
    KeywordCard,
    // KeywordAnalysis,,
    ComplaintsCard,
    NoteworthyPosts,
    PlaceholderCard,
  },
  async fetch() {
    // const requestOptions = {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(
    //     { 
    //       "endDate": this.fetchEndDate,
    //       "numDays": this.fetchNumDays,
    //       "platforms": this.fetchPlatforms,
    //       "sentiments": this.fetchSentiments,
    //       "emotions": this.fetchEmotions,
    //       "query": this.fetchQuery,
    //     }
    //   )
    // };

    // const requestOptionsForWordcloud = {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(
    //     { 
    //       "endDate": this.fetchEndDate,
    //       "numDays": this.fetchNumDays,
    //       "platforms": this.fetchPlatforms,
    //       "sentiments": this.fetchSentiments,
    //       "emotions": this.fetchEmotions,
    //       "query": this.fetchQuery,
    //       "topN": 30
    //     }
    //   )
    // };

    // const requestOptionsForRawPosts = {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(
    //     { 
    //       "endDate": this.fetchEndDate,
    //       "numDays": this.fetchNumDays,
    //       "platforms": this.fetchPlatforms,
    //       "sentiments": this.fetchSentiments,
    //       "emotions": this.fetchEmotions,
    //       "query": this.fetchQuery,
    //       "topN": 5
    //     }
    //   )
    // };

    // const requestOptionsForNoteworthyTopics = {
    //   method: "POST",
    //   headers: { "Content-Type": "application/json" },
    //   body: JSON.stringify(
    //     { 
    //       "endDate": this.fetchEndDate,
    //       "numDays": this.fetchNumDays,
    //       "platforms": this.fetchPlatforms,
    //       "sentiments": this.fetchSentiments,
    //       "emotions": this.fetchEmotions,
    //       "query": this.fetchQuery,
    //       "topN": 5
    //     }
    //   )
    // };

    const requestOptionsForTrendPlots = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        { 
          "endDate": this.fetchEndDate,
          "numDays": this.fetchNumDays,
          "platforms": this.fetchPlatforms,
          "sentiments": this.fetchSentiments,
          "emotions": this.fetchEmotions,
          "query": this.fetchQuery,
          "interval": this.determineChartInterval(this.fetchNumDays)
        }
      )
    };

    // await fetch("http://127.0.0.1:8000/topic-analysis/get-top5-topic-analysis", requestOptions)
    //   .then(response => response.json())
    //   .then(data => 
    //     {
    //       // { "detail": "No data found within date period given" }
    //       // [ 
    //           // { 
    //           //   "name": "others", 
    //           //   "topThreeMentions": [ "russia", "ukraine", "china" ], 
    //           //   "mentions": 21231, 
    //           //   "sentiment": 
    //           //     [ { "sentiment": "neutral", "count": 9343 }, 
    //           //     { "sentiment": "negative", "count": 6460 }, 
    //           //     { "sentiment": "positive", "count": 5428 } ], 
    //           //   "emotions": 
    //           //     [ { "emotion": "neutral", "count": 18360 }, 
    //           //     { "emotion": "joy", "count": 1716 }, 
    //           //     { "emotion": "sadness", "count": 935 }, 
    //           //     { "emotion": "fear", "count": 164 }, 
    //           //     { "emotion": "anger", "count": 56 } ] 
    //           //   }
    //           // ]

    //       // this.testData = data
    //       console.log("top5-topic data", data)
    //       console.log(this.fetchEndDate)
    //       console.log(this.fetchNumDays)
    //       console.log(this.fetchPlatforms)
    //       if (data.detail === "No data found within date period given") {
    //         console.log("inside if loop, No data found within date period given")
    //         this.topFiveTopicsData = []
    //       } else {
    //         this.topFiveTopicsData = data
    //       }
    //     }
    //   )
    //   // .catch((error) => {
    //   //   console.error(error)
    //   // })
    
    // await fetch("http://127.0.0.1:8000/trend-analysis/get-all-aggregated-stats", requestOptions)
    //   .then(response => response.json())
    //   .then(data => 
    //     {
    //       // { "posts": 166, "posts": 5863, "likes": 47456, "platformMetrics": { "facebook": { "mentions": 1, "emotion": "neutral" }, "twitter": { "mentions": 0, "emotion": null } } }

    //       // when there is no data to show
    //       // { "posts": 0, "posts": 0, "likes": 0, "platformMetrics": { "facebook": { "mentions": 0, "emotion": null }, "reddit": { "mentions": 0, "emotion": null }, "twitter": { "mentions": 0, "emotion": null }, "youtube": { "mentions": 0, "emotion": null } } }

    //       // this.testData = data
    //       console.log("get-all-aggregated-stats data", data)
          
    //       this.platformMetrics = data.platformMetrics
    //       delete data.platformMetrics
    //       this.overallStatsData = data

    //       console.log("this.platformMetrics", this.platformMetrics)
    //       console.log("this.overallStatsData", this.overallStatsData)
    //     }
    //   )
    //   // .catch((error) => {
    //   //   console.error(error);
    //   // })
    
    // await fetch("http://127.0.0.1:8000/trend-analysis/get-all-trend-stats", requestOptions)
    //   .then(response => response.json())
    //   .then(data => 
    //     {
    //       // { "trend": 0.62 }
    //       // { "detail": "No data found from previous data range to compare trend" }
    //       // this.testData = data
    //       console.log("get-all-trend-stats", data)

    //       if (data.detail === "No data found from previous data range to compare trend") {
    //         // console.log("inside if loop, No data found from previous data range to compare trend")
    //         this.allTrend = { "trend": "-" }
    //       } else {
    //         this.allTrend = data
    //       }
    //     }
    //   )
    //   // .catch((error) => {
    //   //   console.error(error);
    //   // })
    
    // await fetch("http://127.0.0.1:8000/trend-analysis/get-indiv-trend-stats", requestOptions)
    //   .then(response => response.json())
    //   .then(data => 
    //     { 
    //       // { "facebook": { "trend": 0.62 }, "reddit": { "trend": 0.62 }, "twitter": { "trend": 0 }, "youtube": { "trend": 0.62 } }

    //       // when there is no data to show, to confirm again
    //       // { "facebook": { "trend": 0 }, "reddit": { "trend": 0 }, "twitter": { "trend": 0 }, "youtube": { "trend": 0 } }

    //       // this.testData = data
    //       console.log("get-indv-trend-stats", data)

    //       this.platformTrend = data
    //     }
    //   )
    //   // .catch((error) => {
    //   //   console.error(error);
    //   // })
    
    // await fetch("http://127.0.0.1:8000/keyword-analysis/get-all-top-keywords", requestOptionsForWordcloud)
    // .then(response => response.json())
    //   .then(data => 
    //     {
    //       // [ { "word": "rip", "count": 58, "sentiment": "neutral" }, { "word": "china", "count": 52, "sentiment": "negative" } ]
    //       // { "detail": "No data found within date period given" }

    //       // this.testData = data
    //       console.log("get-all-top-keywords data", data)

    //       if (data.detail === "No data found within date period given") {
    //         // console.log("inside if loop, No data found within date period given")
    //         this.keywords = []
    //       } else {
    //         this.keywords = data
    //       }
    //     }
    //   )
    // //   .catch((error) => {
    // //     console.error(error);
    // //   })
    
    // await fetch("http://127.0.0.1:8000/complaint-analysis/get-all-top-complaint-keywords", requestOptionsForWordcloud)
    // .then(response => response.json())
    //   .then(data => 
    //     {
    //       // [ { "word": "rip", "count": 58, "sentiment": "neutral" }, { "word": "china", "count": 52, "sentiment": "negative" } ]
    //       // { "detail": "No data found within date period given" }
    //         // render image saying there is no data

    //       // this.testData = data
    //       console.log("get-all-top-complaint-keywords data", data)

    //       if (data.detail === "No data found within date period given") {
    //         // console.log("inside if loop, No data found within date period given")
    //         this.complaintsKeywords = []
    //       } else {
    //         this.complaintsKeywords = data
    //       }
    //     }
    //   )
    // //   .catch((error) => {
    // //     console.error(error);
    // //   })
    
    // await fetch("http://127.0.0.1:8000/complaint-analysis/get-all-top5-complaint-posts", requestOptionsForRawPosts)
    // .then(response => response.json())
    //   .then(data => 
    //     {
    //       // { "facebook": { "likes": [], "date": [] }, "reddit": { "likes": [], "date": [] }, "twitter": { "likes": [], "date": [] }, "youtube": { "likes": [], "date": [] } }

    //       // this.testData = data
    //       console.log("get-all-top5-complaint-posts data", data)

    //       // getting sum of posts in dictionary
    //       const numComplaintPosts = this.getNumPostsTotal(this.numComplaintPostsTotal, data)
          
    //       if (numComplaintPosts === 0) {
    //         this.complaintsRelatedPosts = {"platform": []}
    //       } else {
    //         this.complaintsRelatedPosts = data
    //       }
          
    //       this.numComplaintPostsTotal = 0

    //       // console.log("this.numComplaintPostsTotal", this.numComplaintPostsTotal)

    //     },
    //   )
    // //   .catch((error) => {
    // //     console.error(error);
    // //   })
    
    // // //   await fetch("http://127.0.0.1:8000/complaint-analysis/get-platform-complaint-percentage", requestOptions)
    // // //   .then(response => response.json())
    // // //     .then(data => 
    // // //       {
    // // //         // { "facebook": 0.17, "reddit": 0, "twitter": 0, "youtube": 0 }
    // // //         // { "facebook": 0, "reddit": 0, "twitter": 0, "youtube": 0 } if no data

    // // //         // this.testData = data
  
    // // //       }
    // // //     )
    // // //   .catch((error) => {
    // // //     console.error(error);
    // // //   })
    
    // await fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-posts", requestOptionsForRawPosts)
    // .then(response => response.json())
    //   .then(data => 
    //     {
    //       // { "facebook": { "likes": [], "date": [] }, "reddit": { "likes": [], "date": [] }, "twitter": { "likes": [], "date": [] }, "youtube": { "likes": [], "date": [] } }

    //       // this.testData = data

    //       console.log("get-all-top5-noteworthy-posts data", data)

    //       // getting sum of posts in dictionary
    //       const numNoteworthyPosts = this.getNumPostsTotal(this.numNoteworthyPostsTotal, data)
          
    //       if (numNoteworthyPosts === 0) {
    //         this.noteworthyPosts = {"platform": []}
    //       } else {
    //         this.noteworthyPosts = data
    //       }
          
    //       this.numNoteworthyPostsTotal = 0
    //     }
    //   )
    // //   .catch((error) => {
    // //     console.error(error);
    // //   })
    
    // await fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-topics", requestOptionsForNoteworthyTopics)
    //   .then(response => response.json())
    //     .then(data => 
    //       {
    //         // [ "others", "art", "politics", "education", "law and crime" ]
    //         // [] if no data
  
    //         // this.testData = data
    //         console.log("get-all-top5-noteworthy-topics data", data)
    //         this.noteworthyTopTopics = data
    //       }
    //     )
    //   .catch((error) => {
    //     console.error(error);
    //   })

    await fetch("http://127.0.0.1:8000/trend-analysis/get-all-trend-plot-data", requestOptionsForTrendPlots)
      .then(response => response.json())
        .then(data => 
          {
            this.testData = data
            console.log("get-all-trend-plot data", data)
            this.mediaChartData = data
          }
        )
      .catch((error) => {
        console.error(error);
      })
  },
  // mounted() {
  // },
  data: () => ({
    // topFiveTopicsData: [],
    // overallStatsData: {},
    // allTrend: {},
    // platformMetrics: {},
    // platformTrend: {},
    // keywords: [],
    // complaintsKeywords: [],
    // complaintsRelatedPosts: {},
    // noteworthyPosts: {},
    // noteworthyTopTopics: [],
    noteworthyTopTopics: ["others", "tech", "food"],
    keywordsWordCloudLegend: {
      negative: "#EB8159",
      neutral: "#A0D6E8",
      positive: "#EFB727",
    },
    trendingTopicsEmotionsLegend: {
      anger: "#FB3412",
      fear: "#8C56AF",
      joy: "#F7CF15",
      neutral: "#a1a08d",
      sadness: "#477BD1",
    },
    selectedTrendingQuery: "",
    dateLabels: [],
    selectedMedia: [],
    mediaData: {
      medias: ['all','facebook','reddit','twitter','youtube'],
      mediaView: {
        all: ['Number of Mentions','Number of Likes'],
        facebook: ['Number of Mentions', 'Number of Likes', 'Sentiments', 'Emotions'],
        reddit: ['Number of Mentions', 'Number of Net Votes', 'Sentiments', 'Emotions', 'Number of Awards'],
        twitter: ['Number of Mentions', 'Number of Likes', 'Sentiments', 'Emotions', 'Number of Retweets'],
        youtube: ['Number of Mentions', 'Number of Likes', 'Sentiments', 'Emotions', 'Number of Views']
      },
    },
    mediaChartData: {},
    dateFilter: 'Past 7 Days',
    testData: {},
    numComplaintPostsTotal: 0,
    numNoteworthyPostsTotal: 0,
    fetchQuery: null,
    fetchEndDate: "2021-04-06",
    fetchNumDays: 8, // api will return less 1 data point, so need to + 1 to num days
    fetchPlatforms: ["facebook", "reddit", "twitter", "youtube"],
    fetchSentiments: ["neutral", "negative", "positive"],
    fetchEmotions: ["neutral", "anger", "fear", "sadness", "joy"],
    // backup data
    noteworthyPosts: {
      reddit: {
        likes: [
          {
            likes: '300',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: '290',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: '280',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: '270',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: '260',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
        ],
        date: [
          {
            likes: '20',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: '290',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: '80',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: '20',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: '26',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
        ]
      }
    },
    topFiveTopicsData: [
      // arts and entertainment, business and economy, covid19, crime, culture, education, environment, fashion, food, healthcare, law, lifestyle, others, politics, science and medicine, society, sports, technology, transportation, travel
      {
        name: "Business and Economy",
        topThreeMentions: ["01coin", "Budget 2022", "Higher Costs"],
        mentions: 19872, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.4,
              count: 7949
            },
            {
              sentiment: "neutral",
              percentage: 0.2,
              count: 3974
            },
            {
              sentiment: "positive",
              percentage: 0.4,
              count: 7949
            },
          ],
          emotions: [
            {
              emotion: "anger",
              percentage: 0.3,
              count: 5961
            },
            {
              emotion: "fear",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "joy",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "neutral",
              percentage: 0.1,
              count: 1987
            },
            {
              emotion: "sadness",
              percentage: 0.2,
              count: 3974
            },
          ],
      },
      {
        name: "covid19",
        topThreeMentions: ["Endemic", "Throat Spray", "Singapore VTL"],
        mentions: 18790, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.3,
              count: 5673
            },
            {
              sentiment: "neutral",
              percentage: 0.2,
              count: 3758
            },
            {
              sentiment: "positive",
              percentage: 0.5,
              count: 9395
            },
          ],
          emotions: [
            {
              emotion: "anger",
              percentage: 0.3,
              count: 5961
            },
            {
              emotion: "fear",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "joy",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "neutral",
              percentage: 0.1,
              count: 1987
            },
            {
              emotion: "sadness",
              percentage: 0.2,
              count: 3974
            },
          ],
      },
      {
        name: "Politics",
        topThreeMentions: ["Singapore Parliament", "Generation Covid", "Jobs Growth Incentive"],
        mentions: 17393, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.6,
              count: 10436
            },
            {
              sentiment: "neutral",
              percentage: 0.2,
              count: 3479
            },
            {
              sentiment: "positive",
              percentage: 0.2,
              count: 3479
            },
          ],
          emotions: [
            {
              emotion: "anger",
              percentage: 0.3,
              count: 5961
            },
            {
              emotion: "fear",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "joy",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "neutral",
              percentage: 0.1,
              count: 1987
            },
            {
              emotion: "sadness",
              percentage: 0.2,
              count: 3974
            },
          ],
      },
      {
        name: "Sports",
        topThreeMentions: ["Para Sport Academy", "Singapore Football", "Soh Rui Yong"],
        mentions: 16985, 
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
          emotions: [
            {
              emotion: "anger",
              percentage: 0.3,
              count: 5961
            },
            {
              emotion: "fear",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "joy",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "neutral",
              percentage: 0.1,
              count: 1987
            },
            {
              emotion: "sadness",
              percentage: 0.2,
              count: 3974
            },
          ],
      },
      {
        name: "Law",
        topThreeMentions: ["Section 377A", "Drug Trafficker", "Sex Crime"],
        mentions: 16493, 
        sentiment: [
            {
              sentiment: "negative",
              percentage: 0.4,
              count: 6597
            },
            {
              sentiment: "neutral",
              percentage: 0.3,
              count: 4948
            },
            {
              sentiment: "positive",
              percentage: 0.3,
              count: 4948
            },
          ],
          emotions: [
            {
              emotion: "anger",
              percentage: 0.3,
              count: 5961
            },
            {
              emotion: "fear",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "joy",
              percentage: 0.2,
              count: 3974
            },
            {
              emotion: "neutral",
              percentage: 0.1,
              count: 1987
            },
            {
              emotion: "sadness",
              percentage: 0.2,
              count: 3974
            },
          ],
      },
    ],
    overallStatsData: {
      posts: 1000,
      // trend: 0.6,
      comments: 100,
      likes: 10,
      // shares: 3097,
      // filters: {
      //   date: ["", "All"],
      // }
    },
    allTrend: {trend: 0},
    platformMetrics: {
      facebook: { mentions: 0.2, emotion: "anger" }, 
      twitter: { mentions: 0.2, emotion: "sadness" },
    },
    platformTrend: { 
      facebook: { trend: 0.62 }, 
      reddit: { trend: 0.62 }, 
      twitter: { trend: 0 }, 
      youtube: { trend: 0.62 } 
    },
    keywords: [
      {word: "GST Hike", count: "3000", sentiment: "neutral", hover: "60"}, 
      {word: "Dormitory Workers", count: "2000", sentiment: "neutral", hover: "20"}, 
      {word: "Russian Embassy", count: "500", sentiment: "negative"}, 
      {word: "2022 Budget", count: "300", sentiment: "positive"}, 
      {word: "Valentine's Day", count: "200", sentiment: "positive"}, 
      {word: "Progressive Wages", count: "200", sentiment: "positive"}, 
      {word: "Sylvia Lim", count: "180", sentiment: "neutral"}, 
      {word: "Plastic Bag", count: "150", sentiment: "negative"}, 
      {word: "Rental Fees", count: "550", sentiment: "neutral"}, 
      {word: "Phising Scam", count: "600", sentiment: "negative"}, 
      {word: "BTO Prices", count: "600", sentiment: "negative"}, 
      {word: "Inflation", count: "600", sentiment: "negative"}, 
      {word: "Booster Shot", count: "600", sentiment: "positive"}, 
      {word: "SEA Games", count: "200", sentiment: "neutral"}, 
      {word: "Iris Koh", count: "330", sentiment: "negative"}, 
    ],
    complaintsKeywords: [
      {word: "Hot Weather", count: "20"}, 
      {word: "Long Queue", count: "30"}, 
      {word: "Russian Embassy", count: "50"}, 
      {word: "Plastic Bag", count: "18"}, 
      {word: "Rental Fees", count: "23"}, 
      {word: "Phising Scam", count: "60"}, 
      {word: "BTO Prices", count: "60"}, 
      {word: "GrabFood Delivery", count: "60"},  
      {word: "COE Prices", count: "30"}, 
      {word: "Tuition", count: "20"}, 
      {word: "Fuel Price", count: "60"}, 
      {word: "Rental Discrimination", count: "60"}, 
      {word: "Trace Together", count: "60"}, 
      {word: "Scam Call", count: "60", hover: "60"}, 
      {word: "Chicken Hotpot", count: "60"}, 
    ],
    complaintsRelatedPosts: {
      reddit: {
        likes: [
          {
            likes: '300',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '290',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '280',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '270',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '260',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
        ],
        date: [
          {
            likes: '20',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '290',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '80',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '20',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '26',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
        ]
      },
      facebook: {
        likes: [
          {
            likes: '300',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '290',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '280',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '270',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '260',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
        ],
        date: [
          {
            likes: '20',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '290',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '80',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '20',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '26',
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
        ]
      }
    },

  }), // end of data

  computed: {

  },

  methods: {
    getNumPostsTotal(baseCount, data) {
      // console.log("baseCount", baseCount)
      // console.log("data", data)
      for (const platform in data) {
        // console.log("platform", platform)
        for (const metric in data[platform]) {
          // console.log("metric", metric)
          baseCount += data[platform][metric].length
          // console.log("this.numComplaintPostsTotal", baseCount)
        }
      }
      return baseCount
    },
    rerenderDashboard(updatedSentiments) {
      // console.log("=== START rerenderDashboard ===")
      // console.log("rerenderDashboard updatedSentiments", updatedSentiments)

      this.fetchQuery = updatedSentiments[0]
      this.fetchEndDate = updatedSentiments[1]
      this.fetchNumDays = updatedSentiments[2]
      this.fetchPlatforms = updatedSentiments[3]
      this.fetchSentiments = updatedSentiments[4]
      this.fetchEmotions = updatedSentiments[5]
      this.dateFilter = updatedSentiments[6]

      // console.log("this.fetchQuery", this.fetchQuery)
      // console.log("this.fetchEndDate", this.fetchEndDate)
      // console.log("this.fetchNumDays", this.fetchNumDays)
      // console.log("this.fetchPlatforms", this.fetchPlatforms)
      // console.log("this.fetchSentiments", this.fetchSentiments)
      // console.log("this.fetchEmotions", this.fetchEmotions)

      this.getPlatforms();
      this.getDateLabels();

      this.$fetch()

      // console.log("=== END rerenderDashboard ===")
    },

    updateDashboardWithQuery(query) {
      console.log("=== START updateDashboardWithQuery() ===")
      console.log(query)

      this.fetchQuery = query
      this.selectedTrendingQuery = query
      console.log("this.fetchQuery", this.fetchQuery)

      this.$fetch()

      console.log("=== END updateDashboardWithQuery() ===")
    },

    determineChartInterval(numDays) {
      if (numDays <= 4) {
        return "3hours";
      }
      else if (numDays <= 21) {
        return "daily";
      }
      else if (numDays <= 169) {
        return "weekly";
      }
      else if (numDays <= 673) {
        return "monthly";
      }
      else {
        return "yearly";
      }
    },

    getCurrentDate() {
      const current = new Date();
      // const date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
      const date = `${current.getFullYear()}-${current.getMonth()+1}-${current.getDate()}`;
      console.log(date);
      this.fetchEndDate = date;
      console.log(this.fetchEndDate);
    },

    getDaysArray(start, end) {
      const arr = [];
      for(const dt=new Date(start); dt<=new Date(end); dt.setDate(dt.getDate()+1)){
          const date = `${dt.getFullYear()}-${dt.getMonth()+1}-${dt.getDate()}`;
          arr.push(date);
      }
      return arr;
    },

    getDateLabels() {
      const startDate = new Date(this.fetchEndDate);
      startDate.setDate(startDate.getDate() - this.fetchNumDays + 1);
      const formattedStartDate = `${startDate.getFullYear()}-${startDate.getMonth()+1}-${startDate.getDate()}`;

      const endDate = new Date(this.fetchEndDate);
      endDate.setDate(endDate.getDate() - 1);
      const formattedEndDate = `${endDate.getFullYear()}-${endDate.getMonth()+1}-${endDate.getDate()}`;

      const dateList = this.getDaysArray(formattedStartDate, formattedEndDate);
      this.dateLabels = dateList;
      // console.log(startDate);
      // console.log(formattedStartDate);
      // console.log(endDate);
      // console.log(formattedEndDate);
      // console.log(dateList);
      // console.log(this.dateLabels);
    },

    getPlatforms() {
      const numPlatforms = (this.fetchPlatforms).length;
      if (numPlatforms > 1) {
        const platformArr = ["all"];
        for (let platform = 0; platform < numPlatforms; platform++) {
          platformArr.push(this.fetchPlatforms[platform]);
        }
        this.selectedMedia = platformArr;
      }
      else {
        this.selectedMedia = this.fetchPlatforms;
      }
    }

  }, // end of methods
  mounted () {
    this.getCurrentDate();
    this.getPlatforms();
    this.getDateLabels();
  }
}
</script>


<style>

</style>
