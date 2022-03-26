<template>
  <div class="mb-10">
    <SearchFilters/>
    <SocialMediaFeedAllPlatformMetrics/>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard :related-comments="complaintsRelatedComments"/>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard :related-comments="complaintsRelatedComments"/>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard :related-comments="complaintsRelatedComments"/>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard :related-comments="complaintsRelatedComments"/>
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
  data: () => ({
    complaintsRelatedComments: [
      {
        media: 'facebook',
        likes: '22',
        date: '17 October 2021',
        comment: 'Does anyone has bad experience in this dental clinic? These 3 clinics changed its name to Bliss Dental. I have a bad experience at its Hougang outlet...',
        topic: ['Healthcare'],
        sentiment: 'negative',
        emotion: 'sadness',
        link: "https://www.facebook.com/groups/348293689060800/permalink/978840129339483/",
      },
      {
        media: 'Reddit',
        likes: '7',
        date: '25 December 2021',
        comment: 'My personal opinion: Covid has won, the pandemic scare is over, and Im ready to live my life again.',
        topic: ['Healthcare'],
        sentiment: 'neutral',
        emotion: 'neutral',
        link: "https://www.facebook.com/groups/complaintsingapore/posts/1372131596567064/",
      },
    ],
  })
}
</script>


<style>

</style>
