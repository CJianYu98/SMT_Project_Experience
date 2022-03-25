<template>
  <v-container class="px-4 ml-2 pt-0">
    <TrendAnalysisMetricsCardOverallTrend 
      :overall-stats="overallStats"/>
    <TrendAnalysisMetricsCardIndvPlatform 
      :overall-stats="overallStats" 
      :platform-data="platformData"/>
  </v-container>
</template>

<script>
import TrendAnalysisMetricsCardIndvPlatform from './TrendAnalysisMetricsCardIndvPlatform.vue'
import TrendAnalysisMetricsCardOverallTrend from './TrendAnalysisMetricsCardOverallTrend.vue'
export default {
  components: { 
    TrendAnalysisMetricsCardOverallTrend,
    TrendAnalysisMetricsCardIndvPlatform 
  },
  props: {
    overallStats: {
      type: Object,
      required: true
    },
    platformData: {
      type: Object,
      required: true
    },
  },
  data: () => ({

  }),
}
</script>

<style>

</style>

