<template>
  <v-container class="px-4 ml-2 pt-0">
      <v-simple-table class="mb-2 text-center">
        <template v-slot:default>
          <thead class="deep-purple">
            <tr>
              <th class="white--text text-center">
                Posts
              </th>
              <th class="white--text text-center">
                Trend
              </th>
              <!-- text-center, width 100% -->
            </tr>
          </thead>
          <tbody>
            <tr class="primary--text">
              <td>
                {{ overallStats.posts.toLocaleString() }}
              </td>
              <td>
                <div
                  class="font-weight-medium"
                  v-if="overallStats.filters.date[0] === 'All'"
                >
                  -
                </div>
                <TrendAnalysisUpwardTrend v-else-if="overallStats.trend > 0" :percentage-increase="overallStats.trend"/>
                <TrendAnalysisDownwardTrend v-else-if="overallStats.trend < 0" :percentage-decrease="overallStats.trend"/>
                <TrendAnalysisNoTrend v-else/>
              </td>
            </tr> 
          </tbody>

          <thead class="deep-purple">
            <tr>
              <th class="white--text text-center">
                Comments
              </th>
              <th class="white--text text-center">
                Likes
              </th>
            </tr>
          </thead>
          <tbody>
            <tr class="primary--text">
              <td>
                {{ overallStats.comments.toLocaleString() }}
              </td>
              <td>
                {{ overallStats.likes.toLocaleString() }}
              </td>              
            </tr> 
          </tbody>
        </template>
      </v-simple-table>

      <v-simple-table class="mb-3 text-center">
        <template v-slot:default>
          <thead class="deep-purple">
            <tr>
              <th class="white--text text-center">
                Platform
              </th>
              <th class="white--text text-center">
                Mentions
              </th>
              <th class="white--text text-center">
                Trend
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(data, platform) in platformData"
              :key="platform"
            >
              <td>
                <!-- {{ platform }} -->
                <v-img
                  max-height="20"
                  max-width="20"
                  :src="`/${platform}_icon.png`"
                  :alt="`${platform} icon`"
                  class="mx-auto"
                ></v-img>
              </td>
              <td class="primary--text">
                {{ (data.mentions * 100).toFixed(0) }}%
              </td>
              <td>
                <div
                  class="font-weight-medium"
                  v-if="overallStats.filters.date[0] === 'All'"
                >
                  -
                </div>
                <TrendAnalysisUpwardTrend v-else-if="data.trend > 0" :percentage-increase="data.trend"/>
                <TrendAnalysisDownwardTrend v-else-if="data.trend < 0" :percentage-decrease="data.trend"/>
                <TrendAnalysisNoTrend v-else/>
              </td>
            </tr> 
          </tbody>
        </template>
      </v-simple-table>
  </v-container>
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

