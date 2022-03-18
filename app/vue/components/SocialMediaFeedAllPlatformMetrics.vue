<template>
  <v-card
    elevation="3"
    class="ml-8 mr-2 mt-8 rounded-lg"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6">
      Aggregated Statistics
      <HelpTextTooltip :help-text="aggregatedStatsHelpText"/>
    </v-card-title>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="5">
        <SocialMediaFeedIndvPlatformMetrics :platform="facebook"/>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="5">
        <SocialMediaFeedIndvPlatformMetrics :platform="reddit"/>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="5">
        <SocialMediaFeedIndvPlatformMetrics :platform="twitter"/>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="5">
        <SocialMediaFeedIndvPlatformMetrics :platform="youtube"/>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </v-card>
</template>


<script>
import SocialMediaFeedIndvPlatformMetrics from './SocialMediaFeedIndvPlatformMetrics.vue'
export default {
  components: { SocialMediaFeedIndvPlatformMetrics },
  data: () => ({
    aggregatedStatsHelpText: "These aggregated statistics are based on the filters that are selected.",
    facebook: {
      name: 'facebook',
      statistics: 2393832,
      description: 'posts posted',
    },
    reddit: {
      name: 'reddit',
      statistics: 2393832,
      description: 'posts posted',
    },
    twitter: {
      name: 'twitter',
      statistics: 2393832,
      description: 'tweets posted',
    },
    youtube: {
      name: 'youtube',
      statistics: 2393832,
      description: 'videos posted',
    },
  })
}
</script>


<style scoped>

</style>




