<template>
  <div class="mb-10">
    <SearchFilters @changeFilter="rerenderSocialMeduaFeed"/>
    <!-- <p> {{ testData }} </p> -->
    <SocialMediaFeedAllPlatformMetrics
      :aggregated-stats-all-platforms="aggregatedStatsAllPlatforms"
    />
    <v-row class="my-2">
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard
          :platform-all-data="reddit"
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard
          :platform-all-data="reddit"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row class="mb-2">
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard
          :platform-all-data="reddit"
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard
          :platform-all-data="reddit"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
import SocialMediaFeedCard from '../components/SocialMediaFeedCard.vue'
import SocialMediaFeedAllPlatformMetrics from '../components/SocialMediaFeedAllPlatformMetrics.vue'
import SearchFilters from '@/components/SearchFilters'
export default {
  components: { 
    SearchFilters,
    SocialMediaFeedAllPlatformMetrics,
    SocialMediaFeedCard,
  },
  computed: {
  },
  data: () => ({
    aggregatedStatsAllPlatforms: {
      facebook: {
        mentions: 2393832,
        sentiment: [
          {
            sentiment: "positive",
            count: 4535       
          },      
          {
            sentiment: "neutral",
            count: 4535       
          },      
          {
            sentiment: "negative",
            count: 4536       
          }
        ],
        emotions: [
          {
            emotion: "anger",
            count: 5961
          },
          {
            emotion: "fear",
            count: 3974
          },
          {
            emotion: "joy",
            count: 3974
          },
          {
            emotion: "neutral",
            count: 1987
          },
          {
            emotion: "sadness",
            count: 3974
          },
        ],
      },
      reddit: {
        mentions: 2393832,
        sentiment: [
          {
            sentiment: "positive",
            count: 4535       
          },      
          {
            sentiment: "neutral",
            count: 4535       
          },      
          {
            sentiment: "negative",
            count: 4536       
          }
        ],
        emotions: [
          {
            emotion: "anger",
            count: 5961
          },
          {
            emotion: "fear",
            count: 3974
          },
          {
            emotion: "joy",
            count: 3974
          },
          {
            emotion: "neutral",
            count: 1987
          },
          {
            emotion: "sadness",
            count: 3974
          },
        ],
      },
      twitter: {
        mentions: 2393832,
        sentiment: [
          {
            sentiment: "positive",
            count: 4535       
          },      
          {
            sentiment: "neutral",
            count: 4535       
          },      
          {
            sentiment: "negative",
            count: 4536       
          }
        ],
        emotions: [
          {
            emotion: "anger",
            count: 5961
          },
          {
            emotion: "fear",
            count: 3974
          },
          {
            emotion: "joy",
            count: 3974
          },
          {
            emotion: "neutral",
            count: 1987
          },
          {
            emotion: "sadness",
            count: 3974
          },
        ],
      },
      youtube: {
        mentions: 2393832,
        sentiment: [
          {
            sentiment: "positive",
            count: 4535       
          },      
          {
            sentiment: "neutral",
            count: 4535       
          },      
          {
            sentiment: "negative",
            count: 4536       
          }
        ],
        emotions: [
          {
            emotion: "anger",
            count: 5961
          },
          {
            emotion: "fear",
            count: 3974
          },
          {
            emotion: "joy",
            count: 3974
          },
          {
            emotion: "neutral",
            count: 1987
          },
          {
            emotion: "sadness",
            count: 3974
          },
        ],
      },
    },
    reddit: { 
      reddit: {
        likes: [
          {
            likes: 300,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 290,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 280,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 270,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 260,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 300,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 290,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 280,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 270,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 260,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 300,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 290,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 280,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 270,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 260,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 300,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 290,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 280,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 270,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 260,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
        ],
        date: [
          {
            likes: 20,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 290,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 80,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 20,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 26,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 20,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 290,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 80,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 20,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 26,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 20,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 290,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 80,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 20,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 26,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 20,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 290,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 80,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 20,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
          {
            likes: 26,
            datetime: '2021-04-03T14:24:24',
            comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
            topic: 'Healthcare',
            sentiment: 'negative',
            emotion: 'fear',
            link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
            img: "(if there is one)",
            intent: "seeking/giving advice"
          },
        ]
      }
    },
    testData: "",
    fetchQuery: null,
    fetchEndDate: "2021-04-06",
    fetchNumDays: 14,
    fetchSentiments: ["neutral", "negative", "positive"],
    fetchEmotions: ["neutral", "anger", "fear", "sadness", "joy"],
  }),
  methods: {
    rerenderSocialMeduaFeed(updatedSentiments) {
      console.log("=== START rerenderSocialMeduaFeed ===")
      console.log("rerenderSocialMeduaFeed updatedSentiments", updatedSentiments)

      this.fetchQuery = updatedSentiments[0]
      this.fetchEndDate = updatedSentiments[1]
      this.fetchNumDays = updatedSentiments[2]
      this.fetchSentiments = updatedSentiments[3]
      this.fetchEmotions = updatedSentiments[4]
      this.dateFilter = updatedSentiments[5]

      // console.log("this.fetchQuery", this.fetchQuery)
      // console.log("this.fetchEndDate", this.fetchEndDate)
      // console.log("this.fetchNumDays", this.fetchNumDays)
      // console.log("this.fetchSentiments", this.fetchSentiments)
      // console.log("this.fetchEmotions", this.fetchEmotions)

      // this.$fetch()

      console.log("=== END rerenderSocialMeduaFeed ===")
    },
  },
  // async fetch() {
  //   const requestOptions = {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify(
  //       { 
  //         "endDate": this.fetchEndDate,
  //         "numDays": this.fetchNumDays,
  //         "sentiments": this.fetchSentiments,
  //         "emotions": this.fetchEmotions,
  //         "query": this.fetchQuery,
  //       }
  //     )
  //   };

  //   await fetch("http://127.0.0.1:8000/topic-analysis/get-top5-topic-analysis", requestOptions)
  //     .then(response => response.json())
  //     .then(data => 
  //       {
  //         // this.testData = data
  //         console.log("top5-topic data", data)

  //         if (data.detail === "No data found within date period given") {
  //           console.log("inside if loop, No data found within date period given")
  //           this.topFiveTopicsData = []
  //         } else {
  //           this.topFiveTopicsData = data
  //         }
  //       }
  //     )
  //     // .catch((error) => {
  //     //   console.error(error)
  //     // })
  //  },
}
</script>


<style>

</style>
