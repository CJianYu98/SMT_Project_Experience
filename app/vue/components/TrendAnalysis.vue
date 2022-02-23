<template>
  <v-card
    elevation="3"
    class="mr-8 mt-8"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6">
      Trending Analysis
      <HelpTextTooltip :help-text="trendingTopicsHelpText"/>
    </v-card-title>

    <TrendAnalysisMetricsCard :overall-stats="overallStats" :platform-data="platformData"/>

  </v-card>
</template>

<script>
import HelpTextTooltip from './HelpTextTooltip.vue'
import TrendAnalysisMetricsCard from './TrendAnalysisMetricsCard.vue'
export default {
  components: { 
    HelpTextTooltip,
    TrendAnalysisMetricsCard,
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
