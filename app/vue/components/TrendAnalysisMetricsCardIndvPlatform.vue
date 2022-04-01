<template>
  <v-simple-table class="mb-3 text-center mt-4">
    <template v-slot:default>
      <thead class="deep-purple">
        <tr>
          <th class="white--text text-center"></th>
          <th class="white--text text-center">Mentions</th>
          <th class="white--text text-center">Trend</th>
          <th class="white--text text-center">Emotion</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(data, platform) in platformData"
          :key="platform"
          class="my-2"
        >
          <td>
            <!-- {{ platform }} -->
            <v-img
              max-height="30"
              max-width="30"
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
          <td>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-img
                  max-height="30"
                  max-width="30"
                  :src="`/${data.emotion}.png`"
                  :alt="`${data.emotion} icon`"
                  class="mx-auto"
                  v-bind="attrs"
                  v-on="on"
                ></v-img>
              </template>
              <span>{{data.emotion}}</span>
            </v-tooltip>
          </td>
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
    TrendAnalysisNoTrend,
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
}
</script>

<style scoped>
tr {
  height: 70px;
}
</style>


