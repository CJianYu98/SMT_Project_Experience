<template>
  <div class="mb-15">
    <SearchFilters @changeFilter="rerenderDashboard" :selected-trending-query="selectedTrendingQuery"/>
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
    const requestOptions = {
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
        }
      )
    };

    const requestOptionsForWordcloud = {
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
          "topN": 30
        }
      )
    };

    const requestOptionsForRawPosts = {
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
          "topN": 5
        }
      )
    };

    const requestOptionsForNoteworthyTopics = {
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
          "topN": 5
        }
      )
    };

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

    await fetch("http://127.0.0.1:8000/topic-analysis/get-top5-topic-analysis", requestOptions)
      .then(response => response.json())
      .then(data => 
        {
          // { "detail": "No data found within date period given" }
          // [ 
              // { 
              //   "name": "others", 
              //   "topThreeMentions": [ "russia", "ukraine", "china" ], 
              //   "mentions": 21231, 
              //   "sentiment": 
              //     [ { "sentiment": "neutral", "count": 9343 }, 
              //     { "sentiment": "negative", "count": 6460 }, 
              //     { "sentiment": "positive", "count": 5428 } ], 
              //   "emotions": 
              //     [ { "emotion": "neutral", "count": 18360 }, 
              //     { "emotion": "joy", "count": 1716 }, 
              //     { "emotion": "sadness", "count": 935 }, 
              //     { "emotion": "fear", "count": 164 }, 
              //     { "emotion": "anger", "count": 56 } ] 
              //   }
              // ]

          // this.testData = data
          console.log("top5-topic data", data)
          console.log(this.fetchEndDate)
          console.log(this.fetchNumDays)
          console.log(this.fetchPlatforms)
          if (data.detail === "No data found within date period given") {
            console.log("inside if loop, No data found within date period given")
            this.topFiveTopicsData = []
          } else {
            this.topFiveTopicsData = data
          }
        }
      )
      // .catch((error) => {
      //   console.error(error)
      // })
    
    await fetch("http://127.0.0.1:8000/trend-analysis/get-all-aggregated-stats", requestOptions)
      .then(response => response.json())
      .then(data => 
        {
          // { "posts": 166, "posts": 5863, "likes": 47456, "platformMetrics": { "facebook": { "mentions": 1, "emotion": "neutral" }, "twitter": { "mentions": 0, "emotion": null } } }

          // when there is no data to show
          // { "posts": 0, "posts": 0, "likes": 0, "platformMetrics": { "facebook": { "mentions": 0, "emotion": null }, "reddit": { "mentions": 0, "emotion": null }, "twitter": { "mentions": 0, "emotion": null }, "youtube": { "mentions": 0, "emotion": null } } }

          // this.testData = data
          console.log("get-all-aggregated-stats data", data)
          
          this.platformMetrics = data.platformMetrics
          delete data.platformMetrics
          this.overallStatsData = data

          console.log("this.platformMetrics", this.platformMetrics)
          console.log("this.overallStatsData", this.overallStatsData)
        }
      )
      // .catch((error) => {
      //   console.error(error);
      // })
    
    await fetch("http://127.0.0.1:8000/trend-analysis/get-all-trend-stats", requestOptions)
      .then(response => response.json())
      .then(data => 
        {
          // { "trend": 0.62 }
          // { "detail": "No data found from previous data range to compare trend" }
          // this.testData = data
          console.log("get-all-trend-stats", data)

          if (data.detail === "No data found from previous data range to compare trend") {
            // console.log("inside if loop, No data found from previous data range to compare trend")
            this.allTrend = { "trend": "-" }
          } else {
            this.allTrend = data
          }
        }
      )
      // .catch((error) => {
      //   console.error(error);
      // })
    
    await fetch("http://127.0.0.1:8000/trend-analysis/get-indiv-trend-stats", requestOptions)
      .then(response => response.json())
      .then(data => 
        { 
          // { "facebook": { "trend": 0.62 }, "reddit": { "trend": 0.62 }, "twitter": { "trend": 0 }, "youtube": { "trend": 0.62 } }

          // when there is no data to show, to confirm again
          // { "facebook": { "trend": 0 }, "reddit": { "trend": 0 }, "twitter": { "trend": 0 }, "youtube": { "trend": 0 } }

          // this.testData = data
          console.log("get-indv-trend-stats", data)

          this.platformTrend = data
        }
      )
      // .catch((error) => {
      //   console.error(error);
      // })
    
    await fetch("http://127.0.0.1:8000/keyword-analysis/get-all-top-keywords", requestOptionsForWordcloud)
    .then(response => response.json())
      .then(data => 
        {
          // [ { "word": "rip", "count": 58, "sentiment": "neutral" }, { "word": "china", "count": 52, "sentiment": "negative" } ]
          // { "detail": "No data found within date period given" }

          // this.testData = data
          console.log("get-all-top-keywords data", data)

          if (data.detail === "No data found within date period given") {
            // console.log("inside if loop, No data found within date period given")
            this.keywords = []
          } else {
            this.keywords = data
          }
        }
      )
    //   .catch((error) => {
    //     console.error(error);
    //   })
    
    await fetch("http://127.0.0.1:8000/complaint-analysis/get-all-top-complaint-keywords", requestOptionsForWordcloud)
    .then(response => response.json())
      .then(data => 
        {
          // [ { "word": "rip", "count": 58, "sentiment": "neutral" }, { "word": "china", "count": 52, "sentiment": "negative" } ]
          // { "detail": "No data found within date period given" }
            // render image saying there is no data

          // this.testData = data
          console.log("get-all-top-complaint-keywords data", data)

          if (data.detail === "No data found within date period given") {
            // console.log("inside if loop, No data found within date period given")
            this.complaintsKeywords = []
          } else {
            this.complaintsKeywords = data
          }
        }
      )
    //   .catch((error) => {
    //     console.error(error);
    //   })
    
    await fetch("http://127.0.0.1:8000/complaint-analysis/get-all-top5-complaint-posts", requestOptionsForRawPosts)
    .then(response => response.json())
      .then(data => 
        {
          // { "facebook": { "likes": [], "date": [] }, "reddit": { "likes": [], "date": [] }, "twitter": { "likes": [], "date": [] }, "youtube": { "likes": [], "date": [] } }

          // this.testData = data
          console.log("get-all-top5-complaint-posts data", data)

          // getting sum of posts in dictionary
          const numComplaintPosts = this.getNumPostsTotal(this.numComplaintPostsTotal, data)
          
          if (numComplaintPosts === 0) {
            this.complaintsRelatedPosts = {"platform": []}
          } else {
            this.complaintsRelatedPosts = data
          }
          
          this.numComplaintPostsTotal = 0

          // console.log("this.numComplaintPostsTotal", this.numComplaintPostsTotal)

        },
      )
    //   .catch((error) => {
    //     console.error(error);
    //   })
    
    // //   await fetch("http://127.0.0.1:8000/complaint-analysis/get-platform-complaint-percentage", requestOptions)
    // //   .then(response => response.json())
    // //     .then(data => 
    // //       {
    // //         // { "facebook": 0.17, "reddit": 0, "twitter": 0, "youtube": 0 }
    // //         // { "facebook": 0, "reddit": 0, "twitter": 0, "youtube": 0 } if no data

    // //         // this.testData = data
  
    // //       }
    // //     )
    // //   .catch((error) => {
    // //     console.error(error);
    // //   })
    
    await fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-posts", requestOptionsForRawPosts)
    .then(response => response.json())
      .then(data => 
        {
          // { "facebook": { "likes": [], "date": [] }, "reddit": { "likes": [], "date": [] }, "twitter": { "likes": [], "date": [] }, "youtube": { "likes": [], "date": [] } }

          // this.testData = data

          console.log("get-all-top5-noteworthy-posts data", data)

          // getting sum of posts in dictionary
          const numNoteworthyPosts = this.getNumPostsTotal(this.numNoteworthyPostsTotal, data)
          
          if (numNoteworthyPosts === 0) {
            this.noteworthyPosts = {"platform": []}
          } else {
            this.noteworthyPosts = data
          }
          
          this.numNoteworthyPostsTotal = 0
        }
      )
    //   .catch((error) => {
    //     console.error(error);
    //   })
    
    await fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-topics", requestOptionsForNoteworthyTopics)
      .then(response => response.json())
        .then(data => 
          {
            // [ "others", "art", "politics", "education", "law and crime" ]
            // [] if no data
  
            // this.testData = data
            console.log("get-all-top5-noteworthy-topics data", data)
            this.noteworthyTopTopics = data
          }
        )
      .catch((error) => {
        console.error(error);
      })

    await fetch("http://127.0.0.1:8000/trend-analysis/get-all-trend-plot-data", requestOptionsForTrendPlots)
      .then(response => response.json())
        .then(data => 
          {
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
    topFiveTopicsData: [],
    overallStatsData: {},
    allTrend: {},
    platformMetrics: {},
    platformTrend: {},
    keywords: [],
    complaintsKeywords: [],
    complaintsRelatedPosts: {},
    noteworthyPosts: {},
    noteworthyTopTopics: [],
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
    mediasMetrics: { 
      all: {
        view: ['Number of Mentions','Number of Likes'],
        data_mentions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Facebook',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#3949AB',
                backgroundColor: '#3949AB',
                borderWidth: 1,
                // tension: 0.1
              },
              {
                label: 'Reddit',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#EF6C00',
                backgroundColor: '#EF6C00',
                borderWidth: 1,
              },
              {
                label: 'Twitter',
                data: [2300,  150,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3000, 4500, 6641],
                fill: false,
                borderColor: '#42A5F5',
                backgroundColor: '#42A5F5',
                borderWidth: 1
              },
              {
                label: 'Youtube',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#C62828',
                backgroundColor: '#C62828',
                borderWidth: 1
              },
            ]
          },
        },
        data_likes: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Facebook',
                data: [4440,  7850,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#3949AB',
                backgroundColor: '#3949AB',
                borderWidth: 1,
                // tension: 0.1
              },
              {
                label: 'Reddit',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#EF6C00',
                backgroundColor: '#EF6C00',
                borderWidth: 1,
              },
              {
                label: 'Twitter',
                data: [2300,  150,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3000, 4500, 6641],
                fill: false,
                borderColor: '#42A5F5',
                backgroundColor: '#42A5F5',
                borderWidth: 1
              },
              {
                label: 'Youtube',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#C62828',
                backgroundColor: '#C62828',
                borderWidth: 1
              },
            ]
          },
        },
      }, 
      facebook: {
        view: ['Number of Mentions', 'Number of Likes', 'Number of Shares', 'Sentiments', 'Emotions'],
        data_mentions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Facebook',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#3949AB',
                backgroundColor: '#3949AB',
                borderWidth: 1,
              }
            ]
          }
        },
        data_likes: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Facebook',
                data: [4440,  7850,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#3949AB',
                backgroundColor: '#3949AB',
                borderWidth: 1,
              }
            ]
          }
        },
        data_shares: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Facebook',
                data: [4440,  7850,  3342,  500,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#3949AB',
                backgroundColor: '#3949AB',
                borderWidth: 1,
              }
            ]
          }
        },
        data_sentiments: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Negative',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#EB8159',
                backgroundColor: '#EB8159',
                borderWidth: 1
              },
              {
                label: 'Neutral',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#A0D6E8',
                backgroundColor: '#A0D6E8',
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#EFB727',
                backgroundColor: '#EFB727',
                borderWidth: 1,
              },
            ]
          },
        },
        data_emotions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Anger',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#FB3412',
                backgroundColor: '#FB3412',
                borderWidth: 1
              },
              {
                label: 'Fear',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#8C56AF',
                backgroundColor: '#8C56AF',
                borderWidth: 1,
              },
              {
                label: 'Joy',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#F7CF15',
                backgroundColor: '#F7CF15',
                borderWidth: 1,
              },
              {
                label: 'Neutral',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#A1A08D',
                backgroundColor: '#A1A08D',
                borderWidth: 1
              },
              {
                label: 'Sadness',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#477BD1',
                backgroundColor: '#477BD1',
                borderWidth: 1,
              },
            ]
          },
        },
      }, 
      reddit: {
        view: ['Number of Mentions', 'Number of Net Votes', 'Number of Awards', 'Sentiments', 'Emotions'],
        data_mentions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Reddit',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#EF6C00',
                backgroundColor: '#EF6C00',
                borderWidth: 1
              }
            ]
          }
        },
        data_net_votes: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Reddit',
                data: [77,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#EF6C00',
                backgroundColor: '#EF6C00',
                borderWidth: 1
              }
            ]
          }
        },
        data_awards: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Reddit',
                data: [77,  6550,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#EF6C00',
                backgroundColor: '#EF6C00',
                borderWidth: 1
              }
            ]
          }
        },
        data_sentiments: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Negative',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#EB8159',
                backgroundColor: '#EB8159',
                borderWidth: 1
              },
              {
                label: 'Neutral',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#A0D6E8',
                backgroundColor: '#A0D6E8',
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#EFB727',
                backgroundColor: '#EFB727',
                borderWidth: 1,
              },
            ]
          },
        },
        data_emotions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Anger',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#FB3412',
                backgroundColor: '#FB3412',
                borderWidth: 1
              },
              {
                label: 'Fear',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#8C56AF',
                backgroundColor: '#8C56AF',
                borderWidth: 1,
              },
              {
                label: 'Joy',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#F7CF15',
                backgroundColor: '#F7CF15',
                borderWidth: 1,
              },
              {
                label: 'Neutral',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#A1A08D',
                backgroundColor: '#A1A08D',
                borderWidth: 1
              },
              {
                label: 'Sadness',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#477BD1',
                backgroundColor: '#477BD1',
                borderWidth: 1,
              },
            ]
          },
        },
      },         
      twitter: {
        view: ['Number of Mentions', 'Number of Likes', 'Number of Retweets', 'Sentiments', 'Emotions'],
        data_mentions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Twitter',
                data: [2300,  150,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3000, 4500, 6641],
                fill: false,
                borderColor: '#42A5F5',
                backgroundColor: '#42A5F5',
                borderWidth: 1
              }
            ]
          }
        },
        data_likes: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Twitter',
                data: [23,  150,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3000, 4500, 6641],
                fill: false,
                borderColor: '#42A5F5',
                backgroundColor: '#42A5F5',
                borderWidth: 1
              }
            ]
          }
        },
        data_retweets: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Twitter',
                data: [23,  8500,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3000, 4500, 6641],
                fill: false,
                borderColor: '#42A5F5',
                backgroundColor: '#42A5F5',
                borderWidth: 1
              }
            ]
          }
        },
        data_sentiments: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Negative',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#EB8159',
                backgroundColor: '#EB8159',
                borderWidth: 1
              },
              {
                label: 'Neutral',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#A0D6E8',
                backgroundColor: '#A0D6E8',
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#EFB727',
                backgroundColor: '#EFB727',
                borderWidth: 1,
              },
            ]
          },
        },
        data_emotions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Anger',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#FB3412',
                backgroundColor: '#FB3412',
                borderWidth: 1
              },
              {
                label: 'Fear',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#8C56AF',
                backgroundColor: '#8C56AF',
                borderWidth: 1,
              },
              {
                label: 'Joy',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#F7CF15',
                backgroundColor: '#F7CF15',
                borderWidth: 1,
              },
              {
                label: 'Neutral',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#A1A08D',
                backgroundColor: '#A1A08D',
                borderWidth: 1
              },
              {
                label: 'Sadness',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#477BD1',
                backgroundColor: '#477BD1',
                borderWidth: 1,
              },
            ]
          },
        },
      }, 
      youtube: {
        view: ['Number of Mentions', 'Number of Likes', 'Number of Views', 'Sentiments', 'Emotions'],
        data_mentions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Youtube',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#C62828',
                backgroundColor: '#C62828',
                borderWidth: 1
              }
            ]
          }
        },
        data_likes: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Youtube',
                data: [688,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#C62828',
                backgroundColor: '#C62828',
                borderWidth: 1
              }
            ]
          }
        },
        data_views: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Youtube',
                data: [688,  5500,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#C62828',
                backgroundColor: '#C62828',
                borderWidth: 1
              }
            ]
          }
        },
        data_sentiments: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Negative',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#EB8159',
                backgroundColor: '#EB8159',
                borderWidth: 1
              },
              {
                label: 'Neutral',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#A0D6E8',
                backgroundColor: '#A0D6E8',
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#EFB727',
                backgroundColor: '#EFB727',
                borderWidth: 1,
              },
            ]
          },
        },
        data_emotions: {
          chartData: {
            labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
            "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
            datasets: [
              {
                label: 'Anger',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#FB3412',
                backgroundColor: '#FB3412',
                borderWidth: 1
              },
              {
                label: 'Fear',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#8C56AF',
                backgroundColor: '#8C56AF',
                borderWidth: 1,
              },
              {
                label: 'Joy',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#F7CF15',
                backgroundColor: '#F7CF15',
                borderWidth: 1,
              },
              {
                label: 'Neutral',
                data: [6880,  550,  2342,  6070,  522,  2241,  1259,  3157,  1545, 6000, 8500, 9841],
                fill: false,
                borderColor: '#A1A08D',
                backgroundColor: '#A1A08D',
                borderWidth: 1
              },
              {
                label: 'Sadness',
                data: [7700,  1150,  342,  7050,  5522,  341,  259,  1577,  2345, 6000, 8000, 9041],
                fill: false,
                borderColor: '#477BD1',
                backgroundColor: '#477BD1',
                borderWidth: 1,
              },
            ]
          },
        },
      }
    },
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
