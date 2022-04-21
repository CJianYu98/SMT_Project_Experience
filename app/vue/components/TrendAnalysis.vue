<template>
  <v-card
    elevation="3"
    class="mr-8 mt-8 rounded-lg"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6">
      Trend Analysis
      <HelpTextTooltip :help-text="trendingTopicsHelpText"/>
    </v-card-title>

    <template v-if="pendingState">
      <LoadingPlaceholder />
    </template>
    <template v-else>
      <v-row>
        <v-col cols="3.5" >
          <TrendAnalysisMetricsCard
            :selected-date-filter="selectedDateFilter" 
            :overall-stats="overallStats"
            :all-trend="allTrend"
            :platform-metrics="platformMetrics"
            :platform-trend="platformTrend"/>
        </v-col>
        <v-col cols="" class="mr-7">
          <TrendAnalysisTabs
            :media-data="mediaData"
            :media-chart-data="mediaChartData"
            :sentiment-colors="sentimentColors"
            :emotion-colors="emotionColors"
            :date-labels="dateLabels"
          />
        </v-col>
      </v-row>
    </template>
  </v-card>
</template>

<script>
import HelpTextTooltip from './HelpTextTooltip.vue'
import LoadingPlaceholder from './LoadingPlaceholder.vue'
import TrendAnalysisMetricsCard from './TrendAnalysisMetricsCard.vue'
import TrendAnalysisTabs from './TrendAnalysisTabs.vue'

export default {
  components: { 
    HelpTextTooltip,
    TrendAnalysisMetricsCard,
    TrendAnalysisTabs,
    LoadingPlaceholder,
  },
  props: {
    pendingState: {
      type: Boolean,
      required: true
    },
    selectedDateFilter: {
      type: String,
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
    mediaData: {
      type: Object,
      required: true
    },
    mediaChartData: {
      type: Object,
      required: true
    },
    sentimentColors: {
      type: Object,
      required: true
    },
    emotionColors: {
      type: Object,
      required: true
    },
    dateLabels: {
      type: Array,
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
