<template>
  <v-row class="px-4">
    <v-col cols="" class="py-0"> 
      <v-simple-table class="mb-2">
        <template v-slot:default>
          <thead class="deep-purple">
            <tr>
              <th class="white--text">
                Posts
              </th>
              <th class="white--text">
                Trend
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                {{ overallStats.posts }}
              </td>
              <td>
                <TrendAnalysisUpwardTrend v-if="overallStats.trend > 0" :percentage-increase="overallStats.trend"/>
                <TrendAnalysisDownwardTrend v-else-if="overallStats.trend < 0" :percentage-decrease="overallStats.trend"/>
              </td>
            </tr> 
          </tbody>

          <thead class="deep-purple">
            <tr>
              <th class="white--text">
                Comments
              </th>
              <th class="white--text">
                Likes
              </th>
              <th class="white--text">
                Shares
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                {{ overallStats.comments }}
              </td>
              <td>
                {{ overallStats.likes }}
              </td>              
              <td>
                {{ overallStats.shares }}
              </td>
            </tr> 
          </tbody>
        </template>
      </v-simple-table>

      <v-simple-table dense class="mb-3">
        <template v-slot:default>
          <thead class="deep-purple">
            <tr>
              <th class="white--text">
                Platform
              </th>
              <th class="white--text">
                Mentions
              </th>
              <th class="white--text">
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
                ></v-img>
              </td>
              <td>
                {{ (data.mentions * 100).toFixed(0) }}%
              </td>
              <td>
                <TrendAnalysisUpwardTrend v-if="data.trend > 0" :percentage-increase="data.trend"/>
                <TrendAnalysisDownwardTrend v-else-if="data.trend < 0" :percentage-decrease="data.trend"/>
              </td>
            </tr> 
          </tbody>
        </template>
      </v-simple-table>
    </v-col>
  </v-row>
</template>

<script>
import TrendAnalysisDownwardTrend from './TrendAnalysisDownwardTrend.vue'
import TrendAnalysisUpwardTrend from './TrendAnalysisUpwardTrend.vue'
export default {
  components: { 
    TrendAnalysisDownwardTrend, 
    TrendAnalysisUpwardTrend 
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

  }),
}
</script>

<style>
/* th {
  color: white;
} */

/* .v-application--is-ltr .v-data-table > .v-data-table__wrapper > table > tbody > tr > th, .v-application--is-ltr .v-data-table > .v-data-table__wrapper > table > thead > tr > th, .v-application--is-ltr .v-data-table > .v-data-table__wrapper > table > tfoot > tr > th {
  color: white;
} */


</style>

