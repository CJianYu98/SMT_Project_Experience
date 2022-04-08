<template>
  <div class="mb-15">
    <SearchFilters @changeFilter="rerenderDashboard" :selected-trending-query="selectedTrendingQuery"/>
    <!--  align="stretch" in v-row works with d-flex in v-col -->
    <!-- <p>{{testData}}</p> -->
    <v-row>
      <v-col cols="4">
        <TrendingTopics 
          :top-five-topics="topFiveTopicsData" 
          :keywords-word-cloud-legend="keywordsWordCloudLegend"
          :trending-topics-emotions-legend="trendingTopicsEmotionsLegend"
          @clickQuery="updateDashboardWithQuery" @selectedTrendingTopicInDashboard="passTrendingTopicsToDashboard" 
        />
      </v-col>
      <v-col cols="8">
        <TrendAnalysis 
          :overall-stats="overallStatsData"
          :platform-metrics="platformMetrics"
          :all-trend="allTrend"
          :platform-trend="platformTrend"
          :medias="medias"
          :mediasMetrics="mediasMetrics"
          :selected-date-filter="dateFilter"
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
        <NoteworthyComments 
          :related-comments="noteworthyComments"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="4">
        <PlaceholderCard/>
      </v-col>
      <v-col cols="8">
        <ComplaintsCard 
          :complaints-word-cloud="complaintsKeywords"
          :related-comments="complaintsRelatedComments"
        />
      </v-col>      
    </v-row>
  </div>
</template>

<script>
import TrendAnalysis from '../components/TrendAnalysis.vue'
import KeywordCard from '../components/KeywordWordCloudCard.vue'
// import KeywordAnalysis from '../components/KeywordAnalysisCard.vue'
import NoteworthyComments from '../components/NoteworthyPosts.vue'
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
    NoteworthyComments,
    PlaceholderCard,
  },
  created() {
    // Simple POST request with a JSON body using fetch
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        { 
          "endDate": "2021-04-08",
          "numDays": 7,
          "platforms": [
            "facebook", "youtube", "reddit", "twitter"
          ],
          "sentiments": [
            "neutral", "negative", "positive"
          ],
          "emotions": [
            "neutral", "anger", "fear", "sadness", "joy"
          ],
          "query": null
        }
      )
    };
    // fetch("http://127.0.0.1:8000/topic-analysis/get-top5-topic-analysis", requestOptions)
    // .then(response => response.json())
    //   .then(data => 
    //     {
    //       this.testData = data
    //     }
    //   )
    //   .catch((error) => {
    //     console.error(error);
    //   })
    fetch("http://127.0.0.1:8000/trend-analysis/get-all-aggregated-stats", requestOptions)
      .then(response => response.json())
      .then(data => 
        {
          // { "posts": 166, "comments": 5863, "likes": 47456, "platformMetrics": { "facebook": { "mentions": 1, "emotion": "neutral" }, "twitter": { "mentions": 0, "emotion": null } } }
          this.platformMetrics = data.platformMetrics
          delete data.platformMetrics
          this.overallStatsData = data
          console.log("this.platformMetrics", this.platformMetrics)
        }
      )
      .catch((error) => {
        console.error(error);
      })
    fetch("http://127.0.0.1:8000/trend-analysis/get-all-trend-stats", requestOptions)
      .then(response => response.json())
      .then(data => 
        {
          // { "trend": 0.62 }
          // this.testData = data
          this.allTrend = data
          console.log("this.allTrend", this.allTrend)
        }
      )
      .catch((error) => {
        console.error(error);
      })
    fetch("http://127.0.0.1:8000/trend-analysis/get-indiv-trend-stats", requestOptions)
      .then(response => response.json())
      .then(data => 
        { 
          // { "facebook": { "trend": 0.62 }, "reddit": { "trend": 0.62 }, "twitter": { "trend": 0 }, "youtube": { "trend": 0.62 } }
          this.platformTrend = data
        }
      )
      .catch((error) => {
        console.error(error);
      })
    fetch("http://127.0.0.1:8000/keyword-analysis/get-all-top-keywords", requestOptions)
    // [ { "word": "rip", "count": 58, "sentiment": "neutral" }, { "word": "china", "count": 52, "sentiment": "negative" } ]
    .then(response => response.json())
      .then(data => 
        {
          this.keywords = data
        }
      )
      .catch((error) => {
        console.error(error);
      })
    fetch("http://127.0.0.1:8000/complaint-analysis/get-all-top-complaint-keywords", requestOptions)
    // [ { "word": "rip", "count": 58, "sentiment": "neutral" }, { "word": "china", "count": 52, "sentiment": "negative" } ]
    .then(response => response.json())
      .then(data => 
        {
          this.complaintsKeywords = data
        }
      )
      .catch((error) => {
        console.error(error);
      })
    fetch("http://127.0.0.1:8000/complaint-analysis/get-all-top5-complaint-comments", requestOptions)
    .then(response => response.json())
      .then(data => 
        {
          // this.testData = data
          this.complaintsRelatedComments = data
        }
      )
      .catch((error) => {
        console.error(error);
      })
    fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-comments", requestOptions)
    .then(response => response.json())
      .then(data => 
        {
          // this.testData = data
          this.noteworthyComments = data
        }
      )
      .catch((error) => {
        console.error(error);
      })
  },
  data: () => ({
    fakeData: {
        defaultFilters: {
          topFiveTopicsData: [
            // arts and entertainment, business and economy, covid19, crime, culture, education, environment, fashion, food, healthcare, law, lifestyle, others, politics, science and medicine, society, sports, technology, transportation, travel
            {
              name: "Business and Economy",
              topThreeMentions: ["01coin", "Budget 2022", "Higher Costs"],
              mentions: 19872, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 7949
                  },
                  {
                    sentiment: "neutral",
                    count: 3974
                  },
                  {
                    sentiment: "positive",
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
              name: "Covid19",
              topThreeMentions: ["Endemic", "Throat Spray", "Singapore VTL"],
              mentions: 18790, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 5673
                  },
                  {
                    sentiment: "neutral",
                    count: 3758
                  },
                  {
                    sentiment: "positive",
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
              name: "Healthcare",
              topThreeMentions: ["Singapore Parliament", "Generation Covid", "Jobs Growth Incentive"],
              mentions: 17393, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 10436
                  },
                  {
                    sentiment: "neutral",
                    count: 3479
                  },
                  {
                    sentiment: "positive",
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
              name: "Technology",
              topThreeMentions: ["Tesla", "", ""],
              mentions: 14940, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 4482
                  },
                  {
                    sentiment: "neutral",
                    count: 2988
                  },
                  {
                    sentiment: "positive",
                    count: 7470
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
              mentions: 13495, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 5398
                  },
                  {
                    sentiment: "neutral",
                    count: 5398
                  },
                  {
                    sentiment: "positive",
                    count: 2699
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
            posts: 90857,
            trend: 0.6,
            comments: 7894,
            likes: 100394,
            shares: 3097,
            filters: {
              date: ["", "All"],
            }
          },
          platformMetricsData: {
            Facebook: {
              mentions: 0.24,
              trend: -0.2,
              emotion: 'anger',
            },
            Reddit: {
              mentions: 0.14,
              trend: 0.2,
              emotion: 'fear',
            },
            Twitter: {
              mentions: 0.08,
              trend: 0.2,
              emotion: 'joy',
            },
            Youtube: {
              mentions: 0.54,
              trend: -0.2,
              emotion: 'neutral',
            }
          },
          keywords: [
            {word: "GST Hike", size: "60", sentiment: "neutral", hover: "60"}, 
            {word: "Dormitory Workers", size: "20", sentiment: "neutral", hover: "20"}, 
            {word: "Russian Embassy", size: "50", sentiment: "negative", hover: "50"}, 
            {word: "2022 Budget", size: "30", sentiment: "positive", hover: "30"}, 
            {word: "Valentine's Day", size: "20", sentiment: "positive", hover: "20"}, 
            {word: "Progressive Wages", size: "20", sentiment: "positive", hover: "60"}, 
            {word: "Sylvia Lim", size: "18", sentiment: "neutral", hover: "60"}, 
            {word: "Plastic Bag", size: "15", sentiment: "negative", hover: "60"}, 
            {word: "Rental Fees", size: "55", sentiment: "neutral", hover: "60"}, 
            {word: "Phising Scam", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "BTO Prices", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Inflation", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Booster Shot", size: "60", sentiment: "positive", hover: "60"}, 
            {word: "SEA Games", size: "20", sentiment: "neutral", hover: "60"}, 
            {word: "Iris Koh", size: "33", sentiment: "negative", hover: "60"}, 
          ],
          complaintsKeywords: [
            {word: "Hot Weather", size: "20", hover: "60"}, 
            {word: "Long Queue", size: "30", hover: "20"}, 
            {word: "Russian Embassy", size: "50", hover: "50"}, 
            {word: "Plastic Bag", size: "18", hover: "60"}, 
            {word: "Rental Fees", size: "23", hover: "60"}, 
            {word: "Phising Scam", size: "60", hover: "60"}, 
            {word: "BTO Prices", size: "60", hover: "60"}, 
            {word: "GrabFood Delivery", size: "60", hover: "60"},  
            {word: "COE Prices", size: "30", hover: "30"}, 
            {word: "Tuition", size: "20", hover: "20"}, 
            {word: "Fuel Price", size: "60", hover: "60"}, 
            {word: "Rental Discrimination", size: "60", hover: "60"}, 
            {word: "Trace Together", size: "60", hover: "60"}, 
            {word: "Scam Call", size: "60", hover: "60"}, 
            {word: "Chicken Hotpot", size: "60", hover: "60"}, 
          ],
          complaintsRelatedComments: [
            {
              media: 'facebook',
              likes: '24',
              date: '28 February 2022',
              comment: 'Here to share awareness. I was shocked to see I’ve so many foodpanda transaction which were not done by me. Please do check your bank transaction regularly to monitor for any potential fraud transaction. I don’t even maintain my debit card in my foodpan...',
              topic: ['Food', 'Lifestyle'],
              sentiment: 'positive',
              emotion: 'neutral',
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1373797533067137/",
            },
            {
              media: 'facebook',
              likes: '51',
              date: '28 February 2022',
              comment: 'Was tested positive and a doctor called me today about 5 minutes ago. He was wearing glasses and we did a tele call. He was so impatient and when I asked more details on the symptoms he started shouting and when I asked for his name again, he hanged up ...',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'fear',
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            },
            {
              media: 'reddit',
              likes: '0',
              date: '1 March 2022',
              comment: 'Possibly unpopular opinion: Stop letting people test themselves for Covid: The only reason clinics and hospitals are overwhelmed is because kiasu people who are only mildly sick go to see doctor, when it"s not necessary at all. The Covid scare is more of...',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'anger',
              link: "https://www.reddit.com/r/singapore/comments/t1vsu5/possibly_unpopular_opinion_stop_letting_people/",
            },
            {
              media: 'reddit',
              likes: '410',
              date: '24 February 2022',
              comment: 'Inflation: I have began to notice that food prices in Singapore have been going up since the start of the year. At the hawker centre I frequent, several stalls have adjusted their prices by at least $0.20 and reduced their portions. Prices in super marke...',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'anger',
              link: "https://www.reddit.com/r/singapore/comments/sxl2k7/inflation/",
            },
          ],
          keywordsWordCloudLegend: {
            positive: "#78D549",
            neutral: "#EFB727",
            negative: "#EB8159"
          },
          selectedTrendingQuery: "", 
          medias: ['all','facebook','reddit','twitter','youtube'],
          mediasMetrics: { 
            all: {
              view: ['Number of Likes'],
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
            facebook: {
              view: ['Number of Likes', 'Number of Comments', 'Number of Shares'],
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
            reddit: {
              view: ['Number of Net Votes', 'Number of Comments', 'Number of Awards'],
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
            twitter: {
              view: ['Number of Likes','Number of Retweets','Number of Replies'],
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
            youtube: {
              view: ['Number of Likes', 'Number of Views', 'Number of Comments'],
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
            }
          },
          
        },

        customDate: {
          topFiveTopicsData: [
            // arts and entertainment, business and economy, covid19, crime, culture, education, environment, fashion, food, healthcare, law, lifestyle, others, politics, science and medicine, society, sports, technology, transportation, travel
            {
              name: "Travel",
              topThreeMentions: ["Travel Ban", "VTL", "Korea"],
              mentions: 22678, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 9071
                  },
                  {
                    sentiment: "neutral",
                    count: 4536
                  },
                  {
                    sentiment: "positive",
                    count: 9071
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
              name: "Covid19",
              topThreeMentions: ["Omnicron", "Delta Variant", "Vaccine"],
              mentions: 18790, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 9395
                  },
                  {
                    sentiment: "neutral",
                    count: 3758
                  },
                  {
                    sentiment: "positive",
                    count: 5673
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
              name: "Healthcare",
              topThreeMentions: ["Resignation Rates", "Migrant Workers", "MOH"],
              mentions: 17393, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 10436
                  },
                  {
                    sentiment: "neutral",
                    count: 3479
                  },
                  {
                    sentiment: "positive",
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
              topThreeMentions: ["Loh Kean Yew", "Badminton", "Soh Rui Yong"],
              mentions: 17140, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 3428
                  },
                  {
                    sentiment: "neutral",
                    count: 10284
                  },
                  {
                    sentiment: "positive",
                    count: 3428
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
              name: "Crime",
              topThreeMentions: ["OnlyFans", "Titus Low", "Maid"],
              mentions: 16495, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 13196
                  },
                  {
                    sentiment: "neutral",
                    count: 1649
                  },
                  {
                    sentiment: "positive",
                    count: 1650
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
            posts: 92496,
            trend: 0.7,
            comments: 9674,
            likes: 237864,
            shares: 3537,
            filters: {
              date: ["", "All"],
            }
          },
          platformMetricsData: {
            Facebook: {
              mentions: 0.27,
              trend: 0.2,
              emotion: 'anger',
            },
            Reddit: {
              mentions: 0.06,
              trend: -0.05,
              emotion: 'neutral',
            },
            Twitter: {
              mentions: 0.07,
              trend: 0.1,
              emotion: 'joy',
            },
            Youtube: {
              mentions: 0.60,
              trend: 0.5,
              emotion: 'fear',
            }
          },
          keywords: [
            {word: "Travel Restrictions", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Biden", size: "20", sentiment: "neutral", hover: "20"}, 
            {word: "Delta Variant", size: "50", sentiment: "negative", hover: "50"}, 
            {word: "Omnicron", size: "30", sentiment: "positive", hover: "30"}, 
            {word: "Loh Kean Yew", size: "20", sentiment: "neutral", hover: "20"}, 
            {word: "Congratulations", size: "20", sentiment: "positive", hover: "60"}, 
            {word: "Titus Low", size: "18", sentiment: "neutral", hover: "60"}, 
            {word: "OnlyFans", size: "15", sentiment: "negative", hover: "60"}, 
            {word: "Korea", size: "55", sentiment: "neutral", hover: "60"}, 
            {word: "Domestic Abuse", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Resignation", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Jailed", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Soh Rui Yong", size: "60", sentiment: "positive", hover: "60"}, 
            {word: "Olympics", size: "20", sentiment: "neutral", hover: "60"}, 
            {word: "Murder", size: "33", sentiment: "negative", hover: "60"}, 
          ],
          complaintsKeywords: [
            {word: "Travel Restrictions", size: "20", hover: "60"}, 
            {word: "Delta Variant", size: "30", hover: "20"}, 
            {word: "OnlyFans", size: "50", hover: "50"}, 
            {word: "Domestic Abuse", size: "18", hover: "60"}, 
            {word: "Resignation", size: "23", hover: "60"}, 
            {word: "Jailed", size: "60", hover: "60"}, 
            {word: "Murder", size: "60", hover: "60"}, 
            {word: "Sexism", size: "60", hover: "60"},  
            {word: "Long wait", size: "30", hover: "30"}, 
            {word: "Hong Kong", size: "20", hover: "20"}, 
            {word: "Covid Variant", size: "60", hover: "60"}, 
            {word: "Abuse", size: "60", hover: "60"}, 
            {word: "Trace Together", size: "60", hover: "60"}, 
            {word: "Racism", size: "60", hover: "60"}, 
            {word: "Ban", size: "60", hover: "60"}, 
          ],
          complaintsRelatedComments: [
            {
              media: 'facebook',
              likes: '22',
              date: '17 October 2021',
              comment: 'Does anyone has bad experience in this dental clinic? These 3 clinics changed its name to Bliss Dental. I have a bad experience at its Hougang outlet...',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'fear',
              link: "https://www.facebook.com/groups/348293689060800/permalink/978840129339483/",
            },
            {
              media: 'Reddit',
              likes: '7',
              date: '25 December 2021',
              comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'fear',
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            },
          ],
          keywordsWordCloudLegend: {
            positive: "#78D549",
            neutral: "#EFB727",
            negative: "#EB8159"
          },
          selectedTrendingQuery: "", 
          medias: ['all','facebook','reddit','twitter','youtube'],
          mediasMetrics: { 
            all: {
              view: ['Number of Likes'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Facebook',
                    data: [4600,  1150,  772,  6050,  2522,  3241,  1259,  157,  1545, 5000, 6700, 7665],
                    fill: false,
                    borderColor: '#3949AB',
                    backgroundColor: '#3949AB',
                    borderWidth: 1,
                    // tension: 0.1
                  },
                  {
                    label: 'Reddit',
                    data: [2300,  150,  452,  3050,  5522,  341,  259,  1577,  2345, 3000, 4000, 4241],
                    fill: false,
                    borderColor: '#EF6C00',
                    backgroundColor: '#EF6C00',
                    borderWidth: 1,
                  },
                  {
                    label: 'Twitter',
                    data: [2700,  750,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3500, 4500, 4641],
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
            facebook: {
              view: ['Number of Likes', 'Number of Comments', 'Number of Shares'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Facebook',
                    data: [4600,  1150,  772,  6050,  2522,  3241,  1259,  157,  1545, 5000, 6700, 7665],
                    fill: false,
                    borderColor: '#3949AB',
                    backgroundColor: '#3949AB',
                    borderWidth: 1,
                  }
                ]
              }
            }, 
            reddit: {
              view: ['Number of Net Votes', 'Number of Comments', 'Number of Awards'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Reddit',
                    data: [2300,  150,  452,  3050,  5522,  341,  259,  1577,  2345, 3000, 4000, 4241],
                    fill: false,
                    borderColor: '#EF6C00',
                    backgroundColor: '#EF6C00',
                    borderWidth: 1
                  }
                ]
              }
            },         
            twitter: {
              view: ['Number of Likes','Number of Retweets','Number of Replies'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Twitter',
                    data: [2700,  750,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3500, 4500, 4641],
                    fill: false,
                    borderColor: '#42A5F5',
                    backgroundColor: '#42A5F5',
                    borderWidth: 1
                  }
                ]
              }
            }, 
            youtube: {
              view: ['Number of Likes', 'Number of Views', 'Number of Comments'],
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
            }
          },
        },

        customDateNegativeNeutral: {
          topFiveTopicsData: [
            {
              name: "Travel",
              topThreeMentions: ["Travel Ban", "VTL", "Korea"],
              mentions: 13606,  
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 9071
                  },
                  {
                    sentiment: "neutral",
                    count: 4536
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
              name: "Covid19",
              topThreeMentions: ["Omnicron", "Delta Variant", "Vaccine"],
              mentions: 13153, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 9395
                  },
                  {
                    sentiment: "neutral",
                    count: 3758
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
              name: "Healthcare",
              topThreeMentions: ["Resignation Rates", "Migrant Workers", "MOH"],
              mentions: 13915, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 10436
                  },
                  {
                    sentiment: "neutral",
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
              topThreeMentions: ["Loh Kean Yew", "Badminton", "Soh Rui Yong"],
              mentions: 13712, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 3428
                  },
                  {
                    sentiment: "neutral",
                    count: 10284
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
              name: "Crime",
              topThreeMentions: ["OnlyFans", "Titus Low", "Maid"],
              mentions: 14845, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 13196
                  },
                  {
                    sentiment: "neutral",
                    count: 1649
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
            posts: 69231,
            trend: 0,
            comments: 7240,
            likes: 178035,
            shares: 2647,
            filters: {
              date: ["All"],
            }
          },
          platformMetricsData: {
            Facebook: {
              mentions: 0.24,
              trend: -0.2,
              emotion: 'anger',
            },
            Reddit: {
              mentions: 0.14,
              trend: 0.2,
              emotion: 'anger',
            },
            Twitter: {
              mentions: 0.08,
              trend: 0.2,
              emotion: 'anger',
            },
            Youtube: {
              mentions: 0.54,
              trend: -0.2,
              emotion: 'anger',
            },
          },
          keywords: [
            {word: "Travel Restrictions", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Biden", size: "20", sentiment: "neutral", hover: "20"}, 
            {word: "Delta Variant", size: "50", sentiment: "negative", hover: "50"}, 
            {word: "Loh Kean Yew", size: "20", sentiment: "neutral", hover: "20"},  
            {word: "Titus Low", size: "18", sentiment: "neutral", hover: "60"}, 
            {word: "OnlyFans", size: "15", sentiment: "negative", hover: "60"}, 
            {word: "Korea", size: "55", sentiment: "neutral", hover: "60"}, 
            {word: "Domestic Abuse", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Resignation", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Jailed", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Olympics", size: "20", sentiment: "neutral", hover: "60"}, 
            {word: "Murder", size: "33", sentiment: "negative", hover: "60"}, 
          ],
          complaintsKeywords: [
            {word: "Travel Restrictions", size: "20", hover: "60"}, 
            {word: "Delta Variant", size: "30", hover: "20"}, 
            {word: "OnlyFans", size: "50", hover: "50"}, 
            {word: "Domestic Abuse", size: "18", hover: "60"}, 
            {word: "Resignation", size: "23", hover: "60"}, 
            {word: "Jailed", size: "60", hover: "60"}, 
            {word: "Murder", size: "60", hover: "60"}, 
            {word: "Sexism", size: "60", hover: "60"},  
            {word: "Long wait", size: "30", hover: "30"}, 
            {word: "Hong Kong", size: "20", hover: "20"}, 
            {word: "Covid Variant", size: "60", hover: "60"}, 
            {word: "Abuse", size: "60", hover: "60"}, 
            {word: "Trace Together", size: "60", hover: "60"}, 
            {word: "Racism", size: "60", hover: "60"}, 
            {word: "Ban", size: "60", hover: "60"}, 
          ],
          complaintsRelatedComments: [
            {
              media: 'facebook',
              likes: '22',
              date: '17 October 2021',
              comment: 'Does anyone has bad experience in this dental clinic? These 3 clinics changed its name to Bliss Dental. I have a bad experience at its Hougang outlet...',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'fear',
              link: "https://www.facebook.com/groups/348293689060800/permalink/978840129339483/",
            },
            {
              media: 'Reddit',
              likes: '7',
              date: '25 December 2021',
              comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'sadness',
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            },
          ],
          keywordsWordCloudLegend: {
            positive: "#78D549",
            neutral: "#EFB727",
            negative: "#EB8159"
          },
          selectedTrendingQuery: "",
          medias: ['all','facebook','reddit','twitter','youtube'],
          mediasMetrics: { 
            all: {
              view: ['Number of Likes'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Facebook',
                    data: [4600,  1150,  772,  6050,  2522,  3241,  1259,  157,  1545, 5000, 6700, 7665],
                    fill: false,
                    borderColor: '#3949AB',
                    backgroundColor: '#3949AB',
                    borderWidth: 1,
                    // tension: 0.1
                  },
                  {
                    label: 'Reddit',
                    data: [2300,  150,  452,  3050,  5522,  341,  259,  1577,  2345, 3000, 4000, 4241],
                    fill: false,
                    borderColor: '#EF6C00',
                    backgroundColor: '#EF6C00',
                    borderWidth: 1,
                  },
                  {
                    label: 'Twitter',
                    data: [2700,  750,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3500, 4500, 4641],
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
            facebook: {
              view: ['Number of Likes', 'Number of Comments', 'Number of Shares'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Facebook',
                    data: [4600,  1150,  772,  6050,  2522,  3241,  1259,  157,  1545, 5000, 6700, 7665],
                    fill: false,
                    borderColor: '#3949AB',
                    backgroundColor: '#3949AB',
                    borderWidth: 1,
                  }
                ]
              }
            }, 
            reddit: {
              view: ['Number of Net Votes', 'Number of Comments', 'Number of Awards'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Reddit',
                    data: [2300,  150,  452,  3050,  5522,  341,  259,  1577,  2345, 3000, 4000, 4241],
                    fill: false,
                    borderColor: '#EF6C00',
                    backgroundColor: '#EF6C00',
                    borderWidth: 1
                  }
                ]
              }
            },         
            twitter: {
              view: ['Number of Likes','Number of Retweets','Number of Replies'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Twitter',
                    data: [2700,  750,  4342,  7050,  1522,  3841,  1559,  657,  1445, 3500, 4500, 4641],
                    fill: false,
                    borderColor: '#42A5F5',
                    backgroundColor: '#42A5F5',
                    borderWidth: 1
                  }
                ]
              }
            }, 
            youtube: {
              view: ['Number of Likes', 'Number of Views', 'Number of Comments'],
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
            }
          },
        },

        customDateNegativeNeutralFbReddit: {
          topFiveTopicsData: [
            {
              name: "Travel",
              topThreeMentions: ["Travel Ban", "VTL", "Korea"],
              mentions: 13606,  
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 9071
                  },
                  {
                    sentiment: "neutral",
                    count: 4536
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
              name: "Covid19",
              topThreeMentions: ["Omnicron", "Delta Variant", "Vaccine"],
              mentions: 13153, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 9395
                  },
                  {
                    sentiment: "neutral",
                    count: 3758
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
              name: "Healthcare",
              topThreeMentions: ["Resignation Rates", "Migrant Workers", "MOH"],
              mentions: 13915, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 10436
                  },
                  {
                    sentiment: "neutral",
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
              topThreeMentions: ["Loh Kean Yew", "Badminton", "Soh Rui Yong"],
              mentions: 13712, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 3428
                  },
                  {
                    sentiment: "neutral",
                    count: 10284
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
              name: "Crime",
              topThreeMentions: ["OnlyFans", "Titus Low", "Maid"],
              mentions: 14845, 
              sentiment: [
                  {
                    sentiment: "negative",
                    count: 13196
                  },
                  {
                    sentiment: "neutral",
                    count: 1649
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
            posts: 69231,
            trend: 0,
            comments: 7240,
            likes: 178035,
            shares: 2647,
            filters: {
              date: ["All"],
            }
          },
          platformMetricsData: {
            Facebook: {
              mentions: 0.24,
              trend: -0.2,
              emotion: 'anger',
            },
            Reddit: {
              mentions: 0.14,
              trend: 0.2,
              emotion: 'anger',
            },
          },
          keywords: [
            {word: "Travel Restrictions", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Biden", size: "20", sentiment: "neutral", hover: "20"}, 
            {word: "Delta Variant", size: "50", sentiment: "negative", hover: "50"}, 
            {word: "Loh Kean Yew", size: "20", sentiment: "neutral", hover: "20"},  
            {word: "Titus Low", size: "18", sentiment: "neutral", hover: "60"}, 
            {word: "OnlyFans", size: "15", sentiment: "negative", hover: "60"}, 
            {word: "Korea", size: "55", sentiment: "neutral", hover: "60"}, 
            {word: "Domestic Abuse", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Resignation", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Jailed", size: "60", sentiment: "negative", hover: "60"}, 
            {word: "Olympics", size: "20", sentiment: "neutral", hover: "60"}, 
            {word: "Murder", size: "33", sentiment: "negative", hover: "60"}, 
          ],
          complaintsKeywords: [
            {word: "Travel Restrictions", size: "20", hover: "60"}, 
            {word: "Delta Variant", size: "30", hover: "20"}, 
            {word: "OnlyFans", size: "50", hover: "50"}, 
            {word: "Domestic Abuse", size: "18", hover: "60"}, 
            {word: "Resignation", size: "23", hover: "60"}, 
            {word: "Jailed", size: "60", hover: "60"}, 
            {word: "Murder", size: "60", hover: "60"}, 
            {word: "Sexism", size: "60", hover: "60"},  
            {word: "Long wait", size: "30", hover: "30"}, 
            {word: "Hong Kong", size: "20", hover: "20"}, 
            {word: "Covid Variant", size: "60", hover: "60"}, 
            {word: "Abuse", size: "60", hover: "60"}, 
            {word: "Trace Together", size: "60", hover: "60"}, 
            {word: "Racism", size: "60", hover: "60"}, 
            {word: "Ban", size: "60", hover: "60"}, 
          ],
          complaintsRelatedComments: [
            {
              media: 'facebook',
              likes: '22',
              date: '17 October 2021',
              comment: 'Does anyone has bad experience in this dental clinic? These 3 clinics changed its name to Bliss Dental. I have a bad experience at its Hougang outlet...',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'fear',
              link: "https://www.facebook.com/groups/348293689060800/permalink/978840129339483/",
            },
            {
              media: 'Reddit',
              likes: '7',
              date: '25 December 2021',
              comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
              topic: ['Healthcare'],
              sentiment: 'negative',
              emotion: 'fear',
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            },
          ],
          keywordsWordCloudLegend: {
            positive: "#78D549",
            neutral: "#EFB727",
            negative: "#EB8159"
          },
          selectedTrendingQuery: "",
          medias: ['all','facebook','reddit'],
          mediasMetrics: { 
            all: {
              view: ['Number of Likes'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Facebook',
                    data: [4600,  1150,  772,  6050,  2522,  3241,  1259,  157,  1545, 5000, 6700, 7665],
                    fill: false,
                    borderColor: '#3949AB',
                    backgroundColor: '#3949AB',
                    borderWidth: 1,
                    // tension: 0.1
                  },
                  {
                    label: 'Reddit',
                    data: [2300,  150,  452,  3050,  5522,  341,  259,  1577,  2345, 3000, 4000, 4241],
                    fill: false,
                    borderColor: '#EF6C00',
                    backgroundColor: '#EF6C00',
                    borderWidth: 1,
                  },
                ]
              },
            }, 
            facebook: {
              view: ['Number of Likes', 'Number of Comments', 'Number of Shares'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Facebook',
                    data: [4600,  1150,  772,  6050,  2522,  3241,  1259,  157,  1545, 5000, 6700, 7665],
                    fill: false,
                    borderColor: '#3949AB',
                    backgroundColor: '#3949AB',
                    borderWidth: 1,
                  }
                ]
              }
            }, 
            reddit: {
              view: ['Number of Net Votes', 'Number of Comments', 'Number of Awards'],
              chartData: {
                labels: ["Feb 2021",  "Mar 2021",  "Apr 2021",  "May 2021",  "Jun 2021",  
                "Jul 2021",  "Aug 2021", "Sep 2021", "Oct 2021", "Nov 2021", "Dec 2021", "Jan 2022"],
                datasets: [
                  {
                    label: 'Reddit',
                    data: [2300,  150,  452,  3050,  5522,  341,  259,  1577,  2345, 3000, 4000, 4241],
                    fill: false,
                    borderColor: '#EF6C00',
                    backgroundColor: '#EF6C00',
                    borderWidth: 1
                  }
                ]
              }
            },          
          },
        },

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
    // platformMetricsData: {
    //   Facebook: {
    //     mentions: 0.24,
    //     trend: -0.18,
    //     emotion: 'anger',
    //   },
    //   Reddit: {
    //     mentions: 0.14,
    //     trend: 0.39,
    //     emotion: 'joy',
    //   },
    //   Twitter: {
    //     mentions: 0.08,
    //     trend: 0.05,
    //     emotion: 'fear',
    //   },
    //   Youtube: {
    //     mentions: 0.54,
    //     trend: -0.32,
    //     emotion: 'neutral',
    //   }
    // },
    keywords: [
      {word: "GST Hike", size: "60", sentiment: "neutral", hover: "60"}, 
      {word: "Dormitory Workers", size: "20", sentiment: "neutral", hover: "20"}, 
      {word: "Russian Embassy", size: "50", sentiment: "negative", hover: "50"}, 
      {word: "2022 Budget", size: "30", sentiment: "positive", hover: "30"}, 
      {word: "Valentine's Day", size: "20", sentiment: "positive", hover: "20"}, 
      {word: "Progressive Wages", size: "20", sentiment: "positive", hover: "60"}, 
      {word: "Sylvia Lim", size: "18", sentiment: "neutral", hover: "60"}, 
      {word: "Plastic Bag", size: "15", sentiment: "negative", hover: "60"}, 
      {word: "Rental Fees", size: "55", sentiment: "neutral", hover: "60"}, 
      {word: "Phising Scam", size: "60", sentiment: "negative", hover: "60"}, 
      {word: "BTO Prices", size: "60", sentiment: "negative", hover: "60"}, 
      {word: "Inflation", size: "60", sentiment: "negative", hover: "60"}, 
      {word: "Booster Shot", size: "60", sentiment: "positive", hover: "60"}, 
      {word: "SEA Games", size: "20", sentiment: "neutral", hover: "60"}, 
      {word: "Iris Koh", size: "33", sentiment: "negative", hover: "60"}, 
    ],
    complaintsKeywords: [
      {word: "Hot Weather", size: "20", hover: "60"}, 
      {word: "Long Queue", size: "30", hover: "20"}, 
      {word: "Russian Embassy", size: "50", hover: "50"}, 
      {word: "Plastic Bag", size: "18", hover: "60"}, 
      {word: "Rental Fees", size: "23", hover: "60"}, 
      {word: "Phising Scam", size: "60", hover: "60"}, 
      {word: "BTO Prices", size: "60", hover: "60"}, 
      {word: "GrabFood Delivery", size: "60", hover: "60"},  
      {word: "COE Prices", size: "30", hover: "30"}, 
      {word: "Tuition", size: "20", hover: "20"}, 
      {word: "Fuel Price", size: "60", hover: "60"}, 
      {word: "Rental Discrimination", size: "60", hover: "60"}, 
      {word: "Trace Together", size: "60", hover: "60"}, 
      {word: "Scam Call", size: "60", hover: "60"}, 
      {word: "Chicken Hotpot", size: "60", hover: "60"}, 
    ],
    complaintsRelatedComments: {
      reddit: {
        likes: [
          {
            likes: '300',
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '290',
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '280',
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '270',
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '260',
            date: '25 December 2021',
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
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '290',
            date: '24 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '80',
            date: '23 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '20',
            date: '22 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '26',
            date: '21 December 2021',
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
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '290',
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '280',
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '270',
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '260',
            date: '25 December 2021',
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
            date: '25 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '290',
            date: '24 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '80',
            date: '23 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '20',
            date: '22 December 2021',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: ['Healthcare'],
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
          },
          {
            likes: '26',
            date: '21 December 2021',
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
    keywordsWordCloudLegend: {
      negative: "#EB8159",
      neutral: "#EFB727",
      positive: "#78D549",
    },
    trendingTopicsEmotionsLegend: {
      anger: "#FB3412",
      fear: "#8C56AF",
      joy: "#F7CF15",
      neutral: "#a1a08d",
      sadness: "#477BD1",
    },
    selectedTrendingQuery: "",

    medias: ['all','facebook','reddit','twitter','youtube'],
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
        view: ['Number of Mentions', 'Number of Likes', 'Number of Shares', 'Sentiments'],
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
                borderColor: '#EFB727',
                backgroundColor: '#EFB727',
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#78D549',
                backgroundColor: '#78D549',
                borderWidth: 1,
              },
            ]
          },
        },
      }, 
      reddit: {
        view: ['Number of Mentions', 'Number of Net Votes', 'Number of Awards', 'Sentiments'],
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
                borderColor: '#EFB727',
                backgroundColor: '#EFB727',
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#78D549',
                backgroundColor: '#78D549',
                borderWidth: 1,
              },
            ]
          },
        },
      },         
      twitter: {
        view: ['Number of Mentions', 'Number of Likes', 'Number of Retweets', 'Sentiments'],
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
                borderColor: '#EFB727',
                backgroundColor: '#EFB727',
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#78D549',
                backgroundColor: '#78D549',
                borderWidth: 1,
              },
            ]
          },
        },
      }, 
      youtube: {
        view: ['Number of Mentions', 'Number of Likes', 'Number of Views', 'Sentiments'],
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
                borderColor: '#EFB727',
                backgroundColor: '#EFB727',
                borderWidth: 1,
              },
              {
                label: 'Positive',
                data: [600,  1150,  342,  6050,  2522,  3241,  1259,  157,  1545, 5000, 8500, 9841],
                fill: false,
                borderColor: '#78D549',
                backgroundColor: '#78D549',
                borderWidth: 1,
              },
            ]
          },
        },
      }
    },
    dateFilter: 'Past 7 Days',
    testData: {},
    noteworthyComments: {
      reddit: {
        likes: [
          {
            likes: '300',
            date: '25 December 2021',
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
            date: '25 December 2021',
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
            date: '25 December 2021',
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
            date: '25 December 2021',
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
            date: '25 December 2021',
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
            date: '25 December 2021',
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
            date: '24 December 2021',
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
            date: '23 December 2021',
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
            date: '22 December 2021',
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
            date: '21 December 2021',
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

  
  }),

  computed: {

  },

  methods: {
    rerenderDashboard(updatedSentiments) {
      // code to rerender dashboard when the filters are selected, by passing them to the api
      console.log("=== START rerenderDashboard ===")
      console.log("rerenderDashboard updatedSentiments", updatedSentiments)

      this.dateFilter = updatedSentiments[1]
      console.log("dateFilter", this.dateFilter)

      let filterCheck = this.checkFilterSelectionToReturnFakeData(updatedSentiments)

      if (filterCheck == null) {
        filterCheck = "defaultFilters"
      }

      console.log("filterCheck", filterCheck)
      // console.log("query", query)
      // console.log("filterSelection", filterSelection)
      // console.log("this.fakeData", this.fakeData)
      // console.log("this.fakeData.filterCheck", this.fakeData[filterCheck])
      console.log("this.fakeData[filterCheck].topFiveTopicsData", this.fakeData[filterCheck].topFiveTopicsData)

      this.topFiveTopicsData = this.fakeData[filterCheck].topFiveTopicsData
      this.overallStatsData = this.fakeData[filterCheck].overallStatsData
      this.platformMetricsData = this.fakeData[filterCheck].platformMetricsData
      this.keywordsWordCloudLegend = this.fakeData[filterCheck].keywordsWordCloudLegend
      this.keywords = this.fakeData[filterCheck].keywords
      this.complaintsKeywords = this.fakeData[filterCheck].complaintsKeywords
      this.complaintsRelatedComments = this.fakeData[filterCheck].complaintsRelatedComments
      this.medias = this.fakeData[filterCheck].medias
      this.mediasMetrics = this.fakeData[filterCheck].mediasMetrics

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

      const dateSelection = filters[1]
      const platformSelection = filters[2]
      const sentSelection =  filters[3]
      const emotionSelection = filters[4]

      // console.log("query", query)
      // console.log("dateSelection", dateSelection)
      // console.log("platformSelection", platformSelection)
      // console.log("sentSelection", sentSelection)
      // console.log("emotionSelection", emotionSelection)

      if (
        dateSelection==="Past 7 Days" && 
        platformSelection.length===4 && 
        sentSelection.length===3 && 
        emotionSelection.length===5
      ) {
        // console.log("inside if loop")
        // console.log("default filters")
        return "defaultFilters"
      } else if (
        dateSelection==="Custom" && 
        platformSelection.length===4 && 
        sentSelection.length===3 && 
        emotionSelection.length===5
      ) {
        // console.log("inside else if loop")
        return "customDate"
      } else if (
        dateSelection==="Custom" && 
        platformSelection.length===4 && 
        sentSelection.length===2 && 
        sentSelection.includes("Negative") && 
        sentSelection.includes("Neutral") && 
        emotionSelection.length===5
      ) {
        // console.log("inside else if loop")
        return "customDateNegativeNeutral"
      } else if (
        dateSelection==="Custom" && 
        platformSelection.length===2 &&
        platformSelection.includes("Reddit") && 
        platformSelection.includes("Facebook") && 
        sentSelection.length===2 && 
        sentSelection.includes("Negative") && 
        sentSelection.includes("Neutral") && 
        emotionSelection.length===5
      ) {
        return "customDateNegativeNeutralFbReddit"
      }

    },
  }
  
}
</script>


<style>

</style>
