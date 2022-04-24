<template>
  <v-container class="px-4 ml-2 pt-0">
      <!-- :pending-state="pendingState" -->
    <TrendAnalysisMetricsCardOverallTrend
      :selected-date-filter="selectedDateFilter"
      :overall-stats="overallStats"
      :all-trend="allTrend"
      :get-combined-string-from-indv-platform="combinedString"
      />
      <!-- :pending-state="pendingState" -->
    <TrendAnalysisMetricsCardIndvPlatform
      @passCombinedStringToOverallTrend="getCombinedStringFromIndvPlatform"
      :platform-metrics="platformMetrics"
      :platform-trend="platformTrend"
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
    // pendingState: {
    //   type: Boolean,
    //   required: true
    // },
    selectedDateFilter: {
      // type: String,
      required: true
    },
    overallStats: {
      type: Object,
      required: true
    },
    platformMetrics: {
      type: Object,
      required: true
    },
    allTrend: {
      type: Object,
      required: true
    },
    platformTrend: {
      type: Object,
      required: true
    },
  },
  methods: {
    getCombinedStringFromIndvPlatform(combinedString) {
      // console.log("=== start getCombinedStringFromIndvPlatform() ===")
      // console.log("combinedString", combinedString)
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

