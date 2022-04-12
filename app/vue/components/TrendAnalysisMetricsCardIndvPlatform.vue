<template>
  <v-simple-table class="mb-3 text-center mt-4">
    <template v-slot:default>
      <thead class="deep-purple">
        <tr>
          <th class="white--text text-center px-0"></th>
          <th class="white--text text-center px-0">Mentions</th>
          <!-- <th class="white--text text-center">Trend</th> -->
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <th class="white--text text-center"
                v-bind="attrs"
                v-on="on"
              >
                <span>Trend</span>
              </th>
            </template>
            <span>{{ getCombinedString }}</span>
            <template>{{ passCombinedStringToOverallTrend()  }}</template>
          </v-tooltip>
          <th class="white--text text-center">Emotion</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(data, platform) in platformMetrics"
          :key="platform"
          class="my-2"
        >
          <td>
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
              v-if="selectedDateFilter === 'All'"
            >
              <span>━</span>
              <!-- <v-img
                  max-height="20"
                  max-width="20"
                  :src="`/dash.png`"
                  class="mx-auto"
                  v-bind="attrs"
                  v-on="on"
                ></v-img> -->
            </div>
            <TrendAnalysisUpwardTrend v-else-if="platformTrend[platform]['trend'] > 0" :percentage-increase="platformTrend[platform]['trend']"/>
            <TrendAnalysisDownwardTrend v-else-if="platformTrend[platform]['trend'] < 0" :percentage-decrease="platformTrend[platform]['trend']"/>
            <TrendAnalysisNoTrend v-else-if="platformTrend[platform]['trend'] === 0"/>
            <TrendAnalysisNoComparableTrend v-else/>
          </td>
          <td>
            <template v-if="data[emotion] == null">
              <TrendAnalysisNoComparableTrend :tooltipMsg="`no emotion data`"/>
            </template>
            <template v-else>
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
            </template>
          </td>
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
    TrendAnalysisNoComparableTrend,
  },
  props: {
    selectedDateFilter: {
      type: String,
      required: true
    },
    platformTrend: {
      type: Object,
      required: true
    },
    platformMetrics: {
      type: Object,
      required: true
    },
  },
  data: () => ({
    numDaysFromDateFilter: [
        {date: 'Yesterday', numDays: 1}, 
        {date: 'Past 7 Days', numDays: 7}, 
        {date: 'Past 14 Days', numDays: 14}, 
        {date: 'Past 30 Days', numDays: 30}, 
        {date: 'Past 6 Months', numDays: 180}, 
        {date: 'Past Year', numDays: 365}
      ],
    customStartDate: null,
    customEndDate: null,
    nullData: '-'
  }),
  methods: {
    passCombinedStringToOverallTrend() {
      // console.log("=== start passCombinedStringToOverallTrend() ===")
      // console.log("this.getCombinedString", this.getCombinedString)
      this.$emit('passCombinedStringToOverallTrend', this.getCombinedString)
    },
    getNumDaysFromDateFilter() {
      // console.log("=== start getNumDaysFromDateFilter() ===")

      if (!this.isCustomDate) {
        return this.numDaysBetweenCustomDate(this.selectedDateFilter)
      } else {
        return this.isCustomDate.numDays
      }
    },
    numDaysBetweenCustomDate(dateString) {
      // console.log("=== start numDaysBetweenCustomDate() ===")
      // console.log("dateString", dateString)

      const startDateStr = dateString.split("-")[0]
      const endDateStr = dateString.split("-")[1]
      // console.log("startDateStr", startDateStr)
      // console.log("endDateStr", endDateStr)

      const [startDay, startMonth, startYear] = startDateStr.split('/')
      const [endDay, endMonth, endYear] = endDateStr.split('/')

      // console.log("startDateStr.split('/')", startDateStr.split('/'))
      // console.log("endDateStr.split('/')", endDateStr.split('/'))

      const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
      this.customStartDate = new Date(startYear, startMonth-1, startDay);
      this.customEndDate = new Date(endYear, endMonth-1, endDay);

      // console.log("this.customStartDate", this.customStartDate)
      // console.log("this.customEndDate", this.customEndDate)

      const diffDays = Math.round(Math.abs((this.customStartDate - this.customEndDate) / oneDay))
      // console.log("diffDays", diffDays)
      return diffDays
    }
  },
  computed: {
    numDays() {
      return this.getNumDaysFromDateFilter()
    },
    getCombinedString() {
      // console.log("=== start getCombinedString() ===")

      if (this.selectedDateFilter !== 'All') {
        const combinedStr = "Percentage change in number of mentions from " + this.getCurrDatePeriod + " against " + this.getPrevDatePeriod
        // console.log("combinedStr", combinedStr)
        return combinedStr
      } else {
        const combinedStr = "No percentage change comparable"
        // console.log("combinedStr", combinedStr)
        return combinedStr
      }      
    },
    isCustomDate() {
      // console.log("=== start isCustomDate() ===")
      const result = this.numDaysFromDateFilter.find(obj => obj.date === this.selectedDateFilter)
      return result
    },
    getCurrDatePeriod() {
      // console.log("=== start getCurrDatePeriod() ===")

      const triggerNumDays = this.numDays // so that custom start and end dates are set prior
        // if not assigned, this.customEndDate will be null when called later on

      let endDate = new Date();
      let startDate = new Date();
      
      // console.log("outside of if loop")
      // console.log("this.isCustomDate", this.isCustomDate)
      if (this.isCustomDate == null) {
        // console.log("if it is a custom date")
        // console.log("=== inside if loop of isCustomDate ===")
        
        endDate = this.customEndDate;
        startDate = this.customStartDate;
        // console.log("endDate", endDate)
        // console.log("startDate in if loop", startDate)
      }
      
      if (this.isCustomDate != null) {
        // if is not custom date, minus date
        // console.log("inside if loop, not custom date")
        endDate.setDate(endDate.getDate()-1)
        startDate.setDate(startDate.getDate()-triggerNumDays)
        // console.log("startDate", startDate)
      }
      
      // console.log("endDate", endDate)
      const endDateStr = endDate.toLocaleString('en-GB').split(',')[0]
      // console.log("endDateStr", endDateStr)

      // console.log("startDate outside if loop", startDate)
      // startDate.setDate(startDate.getDate()-this.numDays)
      const startDateStr = startDate.toLocaleString('en-GB').split(',')[0]
      // console.log("startDateStr", startDateStr)

      const combinedDateStr = startDateStr + "-" + endDateStr

      return combinedDateStr
    },

    getPrevDatePeriod() {
      // console.log("=== start getPrevDatePeriod() ===")

      const triggerNumDays = this.numDays

      let endDate = new Date();
      let startDate = new Date();

      if (this.isCustomDate == null) {
        // console.log("is a custom date, if loop")

        endDate = new Date(this.customStartDate-1000*60*60*24*1)
        startDate = new Date(endDate-1000*60*60*24*this.numDays)

        // console.log("endDate after setting", endDate)
        // console.log("startDate after setting", startDate)

      } else {
        // console.log("not a custom date, else loop")
        endDate.setDate(endDate.getDate()-(triggerNumDays+1))
        startDate.setDate(startDate.getDate()-(triggerNumDays*2))
      }

      // console.log("endDate", endDate)
      const endDateStr = endDate.toLocaleString('en-GB').split(',')[0]
      // console.log("endDateStr", endDateStr)

      // console.log("startDate", startDate)
      const startDateStr = startDate.toLocaleString('en-GB').split(',')[0]
      // console.log("startDateStr", startDateStr)

      const combinedDateStr = startDateStr + "-" + endDateStr

      return combinedDateStr
    }
  },
}
</script>

<style scoped>
tr {
  height: 70px;
}
</style>


