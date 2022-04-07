<template>
  <v-container class="px-4 ml-2 pt-0">
    <TrendAnalysisMetricsCardOverallTrend
      :selected-date-filter="selectedDateFilter"
      :overall-stats="overallStats"
      :get-combined-string-from-indv-platform="combinedString"
      />
      <!-- :selected-date-filter="selectedDateFilter" -->
    <TrendAnalysisMetricsCardIndvPlatform 
      @passCombinedStringToOverallTrend="getCombinedStringFromIndvPlatform"
      :overall-stats="overallStats" 
      :platform-data="platformData"
      :selected-date-filter="selectedDateFilter"/>
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
  },
  methods: {
    getCombinedStringFromIndvPlatform(combinedString) {
      console.log("=== start getCombinedStringFromIndvPlatform() ===")
      console.log("combinedString", combinedString)
      this.combinedString = combinedString
    }
  },
  data: () => ({
    combinedString: '',
  }),
}
</script>

<style>

</style>

