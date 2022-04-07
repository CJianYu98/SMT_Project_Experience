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
              v-if="selectedDateFilter === 'All'">-</div>
            <TrendAnalysisUpwardTrend v-else-if="overallStats.trend > 0" :percentage-increase="overallStats.trend"/>
            <TrendAnalysisDownwardTrend v-else-if="overallStats.trend < 0" :percentage-decrease="overallStats.trend"/>
            <TrendAnalysisNoTrend v-else/>
          </td>
          <td>{{ overallStats.likes.toLocaleString() }}</td>              
        </tr> 
      </tbody>
    </template>
  </v-simple-table>
</template>


<script>
import TrendAnalysisDownwardTrend from './TrendAnalysisDownwardTrend.vue'
import TrendAnalysisNoTrend from './TrendAnalysisNoTrend.vue'
import TrendAnalysisUpwardTrend from './TrendAnalysisUpwardTrend.vue'
export default {
  components: { 
    TrendAnalysisDownwardTrend, 
    TrendAnalysisUpwardTrend,
    TrendAnalysisNoTrend 
  },
  props: {
    getCombinedStringFromIndvPlatform: {
      type: String,
      required: true
    },
    selectedDateFilter: {
      type: String,
      required: true
    },
    overallStats: {
      type: Object,
      required: true,
    },
  },
}
</script>

<style scoped>

</style>


