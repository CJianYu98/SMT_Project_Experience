<template>
  <v-simple-table class="mb-2 text-center">
    <template v-slot:default>
      <thead class="deep-purple">
        <tr>
          <th class="white--text text-center">Posts</th>
          <th class="white--text text-center">Comments</th>
        </tr>
      </thead>
      <tbody>
        <tr class="primary--text">
          <td>{{ overallStats.posts.toLocaleString() }}</td>
          <td>{{ overallStats.comments.toLocaleString() }}</td>
        </tr> 
      </tbody>

      <thead class="deep-purple">
        <tr>
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <th class="white--text text-center"
                v-bind="attrs"
                v-on="on"
              >
                <span>Trend</span>
              </th>
            </template>
            <span>{{ getCombinedStringFromIndvPlatform }}</span>
          </v-tooltip>
          <th class="white--text text-center">Likes</th>
        </tr>
      </thead>
      <tbody>
        <tr class="primary--text">
          <td>
            <div class="font-weight-medium"
              v-if="selectedDateFilter === 'All'">
                <v-img
                  max-height="20"
                  max-width="20"
                  :src="`/dash.png`"
                  class="mx-auto"
                  v-bind="attrs"
                  v-on="on"
                ></v-img>
              </div>
            <TrendAnalysisUpwardTrend v-else-if="allTrend.trend > 0" :percentage-increase="allTrend.trend"/>
            <TrendAnalysisDownwardTrend v-else-if="allTrend.trend < 0" :percentage-decrease="allTrend.trend"/>
            <TrendAnalysisNoTrend v-else-if="allTrend.trend === 0"/>
            <TrendAnalysisNoComparableTrend v-else :tooltipMsg="`no data found from previous data range to compare trend`"/>
          </td>
          <td>{{ overallStats.likes.toLocaleString() }}</td>              
        </tr> 
      </tbody>
    </template>
  </v-simple-table>
</template>


<script>
import TrendAnalysisDownwardTrend from './TrendAnalysisDownwardTrend.vue'
import TrendAnalysisNoComparableTrend from './TrendAnalysisNoComparableTrend.vue'
import TrendAnalysisNoTrend from './TrendAnalysisNoTrend.vue'
import TrendAnalysisUpwardTrend from './TrendAnalysisUpwardTrend.vue'
export default {
  components: { 
    TrendAnalysisDownwardTrend, 
    TrendAnalysisUpwardTrend,
    TrendAnalysisNoTrend,
    TrendAnalysisNoComparableTrend
  },
  props: {
    // pendingState: {
    //   type: Boolean,
    //   required: true
    // },
    getCombinedStringFromIndvPlatform: {
      type: String,
      required: true
    },
    selectedDateFilter: {
      required: true
    },
    overallStats: {
      type: Object,
      required: true,
    },
    allTrend: {
      type: Object,
      required: true
    },
  },
}
</script>

<style scoped>

</style>


