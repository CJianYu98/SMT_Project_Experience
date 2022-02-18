<template>
  <v-card
    elevation="3"
    class="mr-8 mt-8"
  >
    <v-card-title class="pb-4 accent--text">
      Trending Analysis
      <HelpTextTooltip :help-text="trendingTopicsHelpText"/>
    </v-card-title>

    <v-row>
      <v-col cols="4" >
        <TrendAnalysisMetricsCard :overall-stats="overallStats" :platform-data="platformData"/>
      </v-col>
      <v-col cols="" class="py-0">
        <TrendAnalysisTabs/>
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
    TrendAnalysisTabs
  },
  props: {
    overallStats: {
      type: Object,
      required: true
    },
    platformData: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    trendingTopicsHelpText: "Study the breakdown of aggregated statistics across platforms. Posts refer to videos (YouTube), posts (Facebook, Reddit and Instagram), and tweets (Twitter).",
  }),
}
</script>

<style>

</style>
