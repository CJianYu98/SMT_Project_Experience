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
          :medias="medias"
          :mediasMetrics="mediasMetrics"
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
            // arts and entertainment, business and economy, covid19, crime, culture, education, environment, fashion, food, healthcare, law, lifestyle, others, politics, science and medicine, society, sports, technology, transportation, travel
            {
              name: "Business and Economy",
              topThreeMentions: ["GST Hike", "Budget 2022", "Higher Costs"],
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
            },
            {
              name: "topFiveTopicsData test1",
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
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1373797533067137/",
            },
            {
              media: 'facebook',
              likes: '51',
              date: '28 February 2022',
              comment: 'Was tested positive and a doctor called me today about 5 minutes ago. He was wearing glasses and we did a tele call. He was so impatient and when I asked more details on the symptoms he started shouting and when I asked for his name again, he hanged up ...',
              topic: ['Healthcare'],
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            },
            {
              media: 'reddit',
              likes: '0',
              date: '1 March 2022',
              comment: 'Possibly unpopular opinion: Stop letting people test themselves for Covid: The only reason clinics and hospitals are overwhelmed is because kiasu people who are only mildly sick go to see doctor, when it"s not necessary at all. The Covid scare is more of...',
              topic: ['Healthcare'],
              link: "https://www.reddit.com/r/singapore/comments/t1vsu5/possibly_unpopular_opinion_stop_letting_people/",
            },
            {
              media: 'reddit',
              likes: '410',
              date: '24 February 2022',
              comment: 'Inflation: I have began to notice that food prices in Singapore have been going up since the start of the year. At the hawker centre I frequent, several stalls have adjusted their prices by at least $0.20 and reduced their portions. Prices in super marke...',
              topic: ['Healthcare'],
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
              name: "Business and Economy",
              topThreeMentions: ["GST Hike", "Budget 2022", "Higher Costs"],
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
            },
            {
              name: "topFiveTopicsData test1",
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
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1373797533067137/",
            },
            {
              media: 'facebook',
              likes: '51',
              date: '28 February 2022',
              comment: 'Was tested positive and a doctor called me today about 5 minutes ago. He was wearing glasses and we did a tele call. He was so impatient and when I asked more details on the symptoms he started shouting and when I asked for his name again, he hanged up ...',
              topic: ['Healthcare'],
              link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            },
            {
              media: 'reddit',
              likes: '0',
              date: '1 March 2022',
              comment: 'Possibly unpopular opinion: Stop letting people test themselves for Covid: The only reason clinics and hospitals are overwhelmed is because kiasu people who are only mildly sick go to see doctor, when it"s not necessary at all. The Covid scare is more of...',
              topic: ['Healthcare'],
              link: "https://www.reddit.com/r/singapore/comments/t1vsu5/possibly_unpopular_opinion_stop_letting_people/",
            },
            {
              media: 'reddit',
              likes: '410',
              date: '24 February 2022',
              comment: 'Inflation: I have began to notice that food prices in Singapore have been going up since the start of the year. At the hawker centre I frequent, several stalls have adjusted their prices by at least $0.20 and reduced their portions. Prices in super marke...',
              topic: ['Healthcare'],
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

        customDateNegativeNeutral: {
          topFiveTopicsData: [
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
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
            },
          },
          keywords: [
            {word: "Surfing", size: "20", sentiment: "neutral", hover: "20"}, 
            {word: "Climbing", size: "50", sentiment: "negative", hover: "50"}, 
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
              topic: ['Healthcare']
            },
            {
              media: 'facebook',
              likes: '23,000',
              date: '22 December 2021',
              comment: 'The dreadful breakthrough infection can effectively be prevented with VCO/Lauric Acid, and total community viral load can be lowered, do not play dice with Covid, try to protect the community and your loved ones at the same time.',
              topic: ['Healthcare']
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

        customDateNegativeNeutralFbReddit: {
          topFiveTopicsData: [
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
            {
              name: "topFiveTopicsData test1",
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
                ],
            },
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
          },
          keywords: [
            {word: "Surfing", size: "20", sentiment: "neutral", hover: "20"}, 
            {word: "Climbing", size: "50", sentiment: "negative", hover: "50"}, 
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
              topic: ['Healthcare']
            },
            {
              media: 'facebook',
              likes: '23,000',
              date: '22 December 2021',
              comment: 'The dreadful breakthrough infection can effectively be prevented with VCO/Lauric Acid, and total community viral load can be lowered, do not play dice with Covid, try to protect the community and your loved ones at the same time.',
              topic: ['Healthcare']
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

    },
    
    topFiveTopicsData: [
      // arts and entertainment, business and economy, covid19, crime, culture, education, environment, fashion, food, healthcare, law, lifestyle, others, politics, science and medicine, society, sports, technology, transportation, travel
      {
        name: "Business and Economy",
        topThreeMentions: ["GST Hike", "Budget 2022", "Higher Costs"],
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
      },
      {
        name: "topFiveTopicsData test1",
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
        link: "https://www.facebook.com/groups/complaintsingapore/posts/1373797533067137/",
      },
      {
        media: 'facebook',
        likes: '51',
        date: '28 February 2022',
        comment: 'Was tested positive and a doctor called me today about 5 minutes ago. He was wearing glasses and we did a tele call. He was so impatient and when I asked more details on the symptoms he started shouting and when I asked for his name again, he hanged up ...',
        topic: ['Healthcare'],
        link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
      },
      {
        media: 'reddit',
        likes: '0',
        date: '1 March 2022',
        comment: 'Possibly unpopular opinion: Stop letting people test themselves for Covid: The only reason clinics and hospitals are overwhelmed is because kiasu people who are only mildly sick go to see doctor, when it"s not necessary at all. The Covid scare is more of...',
        topic: ['Healthcare'],
        link: "https://www.reddit.com/r/singapore/comments/t1vsu5/possibly_unpopular_opinion_stop_letting_people/",
      },
      {
        media: 'reddit',
        likes: '410',
        date: '24 February 2022',
        comment: 'Inflation: I have began to notice that food prices in Singapore have been going up since the start of the year. At the hawker centre I frequent, several stalls have adjusted their prices by at least $0.20 and reduced their portions. Prices in super marke...',
        topic: ['Healthcare'],
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
    }
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

    }
  }
  
}
</script>


<style>

</style>
