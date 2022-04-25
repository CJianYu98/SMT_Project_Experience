<template>
  <v-card
    elevation="3"
    class="mx-8 mt-8 rounded-lg pb-6"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6">
      Aggregated Statistics
      <HelpTextTooltip :help-text="aggregatedStatsHelpText"/>
    </v-card-title>
    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="2">
        <GraphLegend 
            :graph-legend="keywordsWordCloudLegend"
            type="sentiment"
            class="mb-5"
          />
        <GraphLegend
          :graph-legend="trendingTopicsEmotionsLegend"
          type="emotion"
        />
      </v-col>
      <v-spacer></v-spacer>
      <template v-if="pendingState">
        <v-col cols="8">
          <LoadingPlaceholder/>
        </v-col>
      </template>
      <template v-else>
        <v-col cols="2" class="px-1">
          <SocialMediaFeedIndvPlatformMetrics
            :platform-all-data="aggregatedStatsAllPlatforms.facebook"
            platform-string="facebook"
          />
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="2" class="px-1">
          <SocialMediaFeedIndvPlatformMetrics
            :platform-all-data="aggregatedStatsAllPlatforms.reddit"
            platform-string="reddit"
          />
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="2" class="px-1">
          <SocialMediaFeedIndvPlatformMetrics
            :platform-all-data="aggregatedStatsAllPlatforms.twitter"
            platform-string="twitter"
          />
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="2" class="px-1">
          <SocialMediaFeedIndvPlatformMetrics
            :platform-all-data="aggregatedStatsAllPlatforms.youtube"
            platform-string="youtube"
          />
        </v-col>
      </template>
      <v-spacer></v-spacer>
    </v-row>
  </v-card>
</template>


<script>
import LoadingPlaceholder from './LoadingPlaceholder.vue'
import SocialMediaFeedIndvPlatformMetrics from './SocialMediaFeedIndvPlatformMetrics.vue'
export default {
  components: { 
    SocialMediaFeedIndvPlatformMetrics,
    LoadingPlaceholder,
  },
  props: {
    aggregatedStatsAllPlatforms: {
      type: Object,
      required: true
    },
    pendingState: {
      type: Boolean,
      required: true
    },
  },
  data: () => ({
    aggregatedStatsHelpText: "These aggregated statistics are based on the filters that are selected.",
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
  }),
}
</script>


<style scoped>

</style>




