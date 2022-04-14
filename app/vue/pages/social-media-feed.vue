<template>
  <div class="mb-10">
    <SearchFilters/>
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
        statistics: 2393832,
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
        statistics: 2393832,
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
        statistics: 2393832,
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
        statistics: 2393832,
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
  }),
}
</script>


<style>

</style>
