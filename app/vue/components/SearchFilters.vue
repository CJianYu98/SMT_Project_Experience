<template>
  <!-- <v-app> -->
  <div id="searchFilter" class="mt-2 mb-n3">
    <v-container fluid class="px-8 mt-n2 pb-0">
      <v-row align="stretch">
        <v-col
          cols="4"
          class="d-flex pb-0"
        >
          <v-text-field
            v-model="autocompleteModel"
            outlined
            clearable
            dense
            label="Enter a search term!"
            class="accent--text change-query-colour"
          >
            
          </v-text-field>
        </v-col>
        <v-col
          class="d-flex pb-0"
          cols="4"
        >
          <v-select
            v-model="dateSelected"
            :items="dateFilter"
            item-text="date"
            label="Select a date period"
            outlined
            dense
            @change="openDialogueIfCustomSelected(dateSelected);"
          >
            <template slot="selection" slot-scope="data">
              <span v-if="data.item.date === 'Custom' && dateRange.length === 1" class="accent--text">{{ dateRange[0] }}</span>
              <span v-else-if="data.item.date === 'Custom' && dateRange.length > 1" class="accent--text">{{ computedCustomDateFormatted }}</span>
              <span v-else class="accent--text">{{ data.item.date }}</span>
            </template>
          </v-select>

          <v-dialog
            v-model="dialog"
            max-width="290"
            overlay-opacity="0"
            content-class="custom-dialog-datepicker"
          >
            <v-date-picker 
              v-model="dateRange" 
              d-block 
              no-title 
              range 
              scrollable
            >
              <!-- @change="updateDatesToPassToDashboard()"  -->
              <v-spacer></v-spacer>
            </v-date-picker>
          </v-dialog>
        </v-col>
        <v-col
          cols="4"
          class="pb-0"
        >
          <v-select
            v-if="isDashboard"
            v-model="platformsSelected"
            :items="platformsFilter"
            label="Platform Filter"
            multiple
            outlined
            dense
          >
            <template #selection="{ item }">
              <span v-if="platformsSelected.indexOf(item) != 0" class="accent--text">, {{item}}</span>
              <span v-else class="accent--text">{{item}}</span>
              <span> </span>
            </template>

            <!-- small-chips -->
          <!-- select all functionality -->
            <!-- <template #prepend-item>
              <v-list-item
                ripple
                @mousedown.prevent
                @click="toggle"
              >
                <v-list-item-action>
                  <v-icon :color="platformsSelected.length > 0 ? 'indigo darken-4' : ''">
                    {{ platformIcon }}
                  </v-icon>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>
                    Select All
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider class="mt-2"></v-divider>
            </template> -->

            <!-- <template #selection="{ item }">
              <v-chip 
                color="accent"
                outlined
                class="my-1"
                small
              >
                {{item}}
              </v-chip>
            </template> -->
          </v-select>
        </v-col>
      </v-row>
      <v-row class="mt-0">
        <v-col
          cols="4"
          class="pb-0 pt-1"
        >
          <v-select
            v-model="sentimentsSelected"
            :items="sentimentsFilter"
            label="Sentiment Filter"
            multiple
            outlined
            dense
          >

            <template #selection="{ item }">
              <span v-if="sentimentsSelected.indexOf(item) != 0" class="accent--text">, {{item}} </span>
              <span v-else class="accent--text"> {{item}} </span>
              <span> </span>
            </template>

          <!-- small-chips -->
          <!-- select all functionality -->
            <!-- <template #prepend-item>
              <v-list-item
                ripple
                @mousedown.prevent
                @click="toggle"
              >
                <v-list-item-action>
                  <v-icon :color="sentimentsSelected.length > 0 ? 'indigo darken-4' : ''">
                    {{ sentimentIcon }}
                  </v-icon>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>
                    Select All
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider class="mt-2"></v-divider>
            </template> -->
            
            <!-- <template #selection="{ item }">
              <v-chip 
                color="accent"
                outlined
                class="my-1"
                small
              >
                {{item}}
              </v-chip>
            </template> -->
          </v-select>
        </v-col>
        <v-col
          cols="4"
          class="pb-0 pt-1"
        >
          <v-select
            v-model="emotionsSelected"
            :items="emotionsFilter"
            label="Emotion Filter"
            multiple
            outlined
            dense
          >
            <template #selection="{ item }">
              <span v-if="emotionsSelected.indexOf(item) != 0" class="accent--text">, {{item}}</span>
              <span v-else class="accent--text">{{item}}</span>
              <span> </span>
            </template>

            <!-- small-chips -->
          <!-- select all functionality -->
            <!-- <template #prepend-item>
              <v-list-item
                ripple
                @mousedown.prevent
                @click="toggle"
              >
                <v-list-item-action>
                  <v-icon :color="platformsSelected.length > 0 ? 'indigo darken-4' : ''">
                    {{ platformIcon }}
                  </v-icon>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>
                    Select All
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider class="mt-2"></v-divider>
            </template> -->

            <!-- <template #selection="{ item }">
              <v-chip 
                color="accent"
                outlined
                class="my-1"
                small
              >
                {{item}}
              </v-chip>
            </template> -->
          </v-select>
        </v-col>
        <v-spacer></v-spacer>
        <v-col 
          cols="1"
          class="pb-0 pt-1">
          <v-btn
            depressed
            block
            color="primary"
            @click="emitFilterSelectionToDashboard()"
          >
            Search
          </v-btn>
        </v-col>
        <v-spacer></v-spacer>
        <v-col 
          cols="1"
          class="pb-0 pt-1">
          <v-btn
            depressed
            block
            color="accent"
            @click="resetSelections()"
          >
            Reset
          </v-btn>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </v-container>
  <!-- </v-app> -->
  </div>
</template>

<script>
  export default {
    props: {
      selectedTrendingQuery: {
        type: String,
        default: null,
      }
    },
    mounted() {
      console.log("this.$route.name", this.$route.name)
    },
    data: () => ({
      autocompleteModel: null, 
      date: null,
      dateRange: ['2021-02-01', '2022-01-31'],
      dateSelected: "Past 7 Days",
      dateFilter: [{date: 'Past 7 Days'}, {date: 'Past 14 Days'}, {date: 'Past 30 Days'}, {date: 'Past 6 Months'}, {date: 'Past Year'}, {date: 'Custom'}],
      // dateFilter: [{date: 'All'}, {date: 'Past 7 Days'}, {date: 'Past 14 Days'}, {date: 'Past 30 Days'}, {date: 'Past 6 Months'}, {date: 'Past Year'}, {date: 'Custom'}],
      numDaysFromDateFilter: [
        {date: 'Yesterday', numDays: 1}, 
        {date: 'Past 7 Days', numDays: 7}, 
        {date: 'Past 14 Days', numDays: 14}, 
        {date: 'Past 30 Days', numDays: 30}, 
        {date: 'Past 6 Months', numDays: 180}, 
        {date: 'Past Year', numDays: 365}
      ],
      emotionsSelected: ["Anger", "Fear", "Joy", "Neutral", "Sadness"],
      emotionsFilter: ["Anger", "Fear", "Joy", "Neutral", "Sadness"],
      dialog: false,
      sentimentsFilter: ['Negative', 'Neutral', 'Positive'],
      sentimentsSelected: ['Negative', 'Neutral', 'Positive'],
      platformsFilter: ['Facebook', 'Reddit', 'YouTube'],
      platformsSelected: ['Facebook', 'Reddit', 'YouTube'],
    }),

    computed: {
      computedCustomDateFormatted() {
        return this.formatDate(this.dateRange[0], this.dateRange[1])
      },
      allPlatformsSelected () {
        return this.platformsSelected.length === this.platformsFilter.length
      },
      somePlatformsSelected () {
        return this.platformsSelected.length >= 0 && !this.allPlatformsSelected
      },
      platformIcon () {
        if (this.allPlatformsSelected) return 'mdi-close-box'
        if (this.somePlatformsSelected) return 'mdi-minus-box'
        return 'mdi-checkbox-blank-outline'
      },
      allSentimentsSelected () {
        return this.sentimentsSelected.length === this.sentimentsFilter.length
      },
      someSentimentsSelected () {
        return this.sentimentsSelected.length >= 0 && !this.allSentimentsSelected
      },
      sentimentIcon () {
        if (this.allSentimentsSelected) return 'mdi-close-box'
        if (this.someSentimentsSelected) return 'mdi-minus-box'
        return 'mdi-checkbox-blank-outline'
      },
      customDateRangeSelected () {
        return this.dateRange.join()
      },
      isDashboard() {
        return this.$route.name === 'dashboard'
      },
      getDateStringFromNonCustomDate() {
        let endDate = new Date()
        const offset = endDate.getTimezoneOffset()
        endDate = new Date(endDate.getTime() - (offset*60*1000))
        return endDate.toISOString().split('T')[0]
      },
      numDaysBetweenCustomDate() {
      console.log("=== start numDaysBetweenCustomDate() ===")

      const [startYear, startMonth, startDay] = this.dateRange[0].split("-")
      const [endYear, endMonth, endDay] = this.dateRange[1].split("-")

      const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
      const customStartDate = new Date(startYear, startMonth-1, startDay);
      const customEndDate = new Date(endYear, endMonth-1, endDay);

      // console.log("this.customStartDate", this.customStartDate)
      // console.log("this.customEndDate", this.customEndDate)

      const diffDays = (Math.round(Math.abs((customStartDate - customEndDate) / oneDay))) + 1
      console.log("diffDays", diffDays)
      return diffDays
    }
    },

    watch: {
      // model (val) {
      //   if (val != null) this.tab = 0
      //   else this.tab = null
      // },

      selectedTrendingQuery (newVal, oldVal) { 
        console.log('Prop changed: ', newVal, ' | was: ', oldVal)
        console.log("this.autocompleteModel 1", this.autocompleteModel)
        this.autocompleteModel = newVal
      },
    },
    methods: {
      // select all functionality in filters, to separate according to sentiment and platforms
    //   toggle () {
    //     this.$nextTick(() => {
    //       // if all platforms are selected, we see the close icon
    //       // make the selected platforms an empty list, see the minus icon
    //       // if we close icon is selected, then minus all icon is shown
    //       // this.nextTick -> when data is changed and dom has to be updated

    //       if (this.allPlatformsSelected) {
    //         this.platformsSelected = []
    //       } 
    //       else if (this.somePlatformsSelected) {
    //         this.platformsSelected = this.platformsFilter.slice()
    //       }

    //       if (this.allSentimentsSelected) {
    //         this.sentimentsSelected = []
    //       } else if (this.someSentimentsSelected) {
    //         this.sentimentsSelected = this.sentimentsFilter.slice()
    //       }
    //     })
    //   }
      formatDate(startDate, endDate) {
        // console.log("=== start formatDate() ===")
        // console.log("startDate", startDate)
        // console.log("endDate", endDate)
        if (!startDate && !endDate) return null

        const [startYear, startMonth, startDay] = startDate.split('-')
        const [endYear, endMonth, endDay] = endDate.split('-')
        const combinedDates = `${startDay}/${startMonth}/${startYear}-${endDay}/${endMonth}/${endYear}`
        // console.log("combinedDates", combinedDates

        return combinedDates
      },

      resetSelections() {
        // console.log("=== START resetSelections() ")

        this.autocompleteModel = null
        this.dateSelected = "Past 7 Days"
        this.emotionsSelected = this.emotionsFilter
        this.sentimentsSelected = this.sentimentsFilter

        if (this.$route.name === "dashboard") {
          this.platformsSelected = this.platformsFilter
        }

        // console.log("=== END resetSelections() ")
      },

      emitFilterSelectionToDashboard() {
        console.log("=== START emitFilterSelectionToDashboard() ===")

        const formattedSentimentsSelected = this.sentimentsSelected.map(v => v.toLowerCase())
        const formattedEmotionsSelected = this.emotionsSelected.map(v => v.toLowerCase())
        let formattedDateSelected = ""
        let numDays = 0
        let trendHoverDate = ""

        if (this.dateSelected === 'Custom') {
          console.log("inside if loop, custom date selected")
          formattedDateSelected = this.dateRange[1]
          numDays = this.numDaysBetweenCustomDate
          trendHoverDate = this.dateRange
        } else {
          formattedDateSelected = this.getDateStringFromNonCustomDate
          numDays = this.numDaysFromDateFilter.find(obj => obj.date === this.dateSelected).numDays
          trendHoverDate = this.dateSelected
        }
        console.log("trendHoverDate", trendHoverDate)

        if (this.$route.name === "dashboard") {

          console.log("inside if loop, dashboard page")

          const formattedPlatformsSelected = this.platformsSelected.map(v => v.toLowerCase())
          
          this.$emit('changeFilter', [this.autocompleteModel, formattedDateSelected, numDays, formattedPlatformsSelected, formattedSentimentsSelected, formattedEmotionsSelected, trendHoverDate])

        } else if (this.$route.name === "social-media-feed") {

          console.log("in else if loop, social media feed page")

          this.$emit('changeFilter', [this.autocompleteModel, formattedDateSelected, numDays, formattedSentimentsSelected, formattedEmotionsSelected, trendHoverDate])

        }
        
        console.log("=== END emitFilterSelectionToDashboard() ===")
      },

      openDialogueIfCustomSelected(dateSelected) {
        if (dateSelected === 'Custom') {
          this.dialog = true
        } 
      }
    },

  }
</script>

<style>
#searchFilter {
  background-color: #ffffff !important;
}
</style>

<style scoped>
::v-deep .custom-dialog-datepicker {
  position: absolute;
  top: 10%;
  left: 40%;
}
::v-deep .change-query-colour input {
  color: #604AF0 !important;
}
</style>
