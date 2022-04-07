<template>
  <v-card
    elevation="3"
    class="mr-8 mt-8 rounded-lg"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6">
      Trending Analysis
      <HelpTextTooltip :help-text="trendingTopicsHelpText"/>
    </v-card-title>

    <v-row>
      <v-col cols="4" >
        <TrendAnalysisMetricsCard
          :selected-date-filter="selectedDateFilter" 
          :overall-stats="overallStats" 
          :platform-data="platformData"/>
      </v-col>
      <v-col cols="" class="py-0">
        <TrendAnalysisTabs
          :medias="medias"
          :mediasMetrics="mediasMetrics"
        />
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import HelpTextTooltip from './HelpTextTooltip.vue'
import TrendAnalysisMetricsCard from './TrendAnalysisMetricsCard.vue'
import TrendAnalysisTabs from './TrendAnalysisTabs.vue'

export default {
  components: { 
    HelpTextTooltip,
    TrendAnalysisMetricsCard,
    TrendAnalysisTabs,
  },
  props: {
    selectedDateFilter: {
      type: String,
      required: true
    },
    overallStats: {
      type: Object,
      required: true
    },
    platformData: {
      type: Object,
      required: true
    },
    medias: {
      type: Array,
      required: true
    },
    mediasMetrics: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    trendingTopicsHelpText: "Study aggregated statistics across platforms, including each platform's change in activity and dominant emotion. Mentions refer to both posts and comments. The trend is calculated by comparing the selected time interval against the previous.",
  }),
}
</script>

<style>

</style>
