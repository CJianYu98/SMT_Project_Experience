<template>
  <!-- <v-app> -->
  <div id="searchFilter" class="mt-2 mb-n3">
    <v-container fluid class="px-8 mt-n2 pb-0">
      <v-row align="stretch">
        <v-col
          cols="4"
          class="d-flex pb-0"
        >
          <v-combobox
            v-if="selectedTrendingQuery"
            v-model="autocompleteModel"
            :items="items"
            :loading="isLoading"
            clearable
            hide-no-data
            hide-details
            hide-selected
            label="Enter a query!"
            solo
            item-text="name"
            item-value="symbol"
            dense
          >
          </v-combobox>

          <v-combobox
            v-else
            v-model="autocompleteModel"
            :items="items"
            :loading="isLoading"
            :search-input.sync="search"
            clearable
            hide-no-data
            hide-details
            hide-selected
            item-text="name"
            item-value="symbol"
            label="Enter a query!"
            solo
            dense
          > 
          </v-combobox>
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
              @change="updateDatesToPassToDashboard()" 
            >
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
      isLoading: false,
      items: [],
      autocompleteModel: null, // stores the symbol (value), not the name (text)
      search: null,
      tab: null,
      menu1: false,
      menu: false,
      date: null,
      dateRange: ['2021-02-01', '2022-01-31'],
      dateSelected: "Past 7 Days",
      dateFilter: [{date: 'All'}, {date: 'Past 7 Days'}, {date: 'Past 14 Days'}, {date: 'Past 30 Days'}, {date: 'Past 6 Months'}, {date: 'Past Year'}, {date: 'Custom'}],
      emotionsSelected: ["Anger", "Fear", "Joy", "Neutral", "Sadness"],
      emotionsFilter: ["Anger", "Fear", "Joy", "Neutral", "Sadness"],
      dialog: false,
      sentimentsFilter: ['Negative', 'Neutral', 'Positive'],
      sentimentsSelected: ['Negative', 'Neutral', 'Positive'],
      platformsFilter: ['Facebook', 'Reddit', 'Twitter', 'YouTube'],
      platformsSelected: ['Facebook', 'Reddit', 'Twitter', 'YouTube'],
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
    },

    watch: {
      model (val) {
        if (val != null) this.tab = 0
        else this.tab = null
      },

      // search: {
      //   handler(val) {
      //     if (this.items.length > 0) return
      //       this.isLoading = true

      //     // Lazily load input items
      //     fetch('https://api.coingecko.com/api/v3/coins/list')
      //       .then(res => res.clone().json())
      //       .then(res => {
      //         this.items = res
      //         console.log("UNDER WATCH this.items", this.items)
      //       })
      //       .catch(err => {
      //         console.log(err)
      //       })
      //       .finally(() => (this.isLoading = false))
      //   },
      //   immediate: true
      // },

      selectedTrendingQuery (newVal, oldVal) { // watch it
        console.log('Prop changed: ', newVal, ' | was: ', oldVal)
        console.log("this.autocompleteModel 1", this.autocompleteModel)
        this.updateAutoComplete(newVal)

        this.emitFilterSelectionToDashboard(this.autocompleteModel, this.dateSelected, this.platformsSelected, this.sentimentsSelected, this.emotionsSelected)
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
      updateDatesToPassToDashboard() {
        console.log("=== start updateDates() ===")

        console.log("computedCustomDateFormatted", this.computedCustomDateFormatted)

        this.emitFilterSelectionToDashboard(this.autocompleteModel, this.computedCustomDateFormatted, this.platformsSelected, this.sentimentsSelected, this.emotionsSelected)

        console.log("=== end updateDates() ===")
      },
      // emitFilterSelectionToDashboard(autocompleteModel, dateSelected, platformsSelected, sentimentsSelected, emotionsSelected) {
      //   console.log("=== START emitFilterSelectionToDashboard() ===")
      //   this.$emit('changeFilter', [autocompleteModel, dateSelected, platformsSelected, sentimentsSelected, emotionsSelected])
      //   console.log("=== END emitFilterSelectionToDashboard() ===")
      // },
      emitFilterSelectionToDashboard() {
        console.log("=== START emitFilterSelectionToDashboard() ===")
        this.$emit('changeFilter', [this.autocompleteModel, this.dateSelected, this.platformsSelected, this.sentimentsSelected, this.emotionsSelected])
        console.log("=== END emitFilterSelectionToDashboard() ===")
      },

      updateAutoComplete(val) {
        console.log("=== START updateAutoComplete() === ")
        console.log("val", val)
        // if val is found in items, update autocompletemodel variable
        console.log("this.items", this.items)

        const checkValInAutoComplete = this.items.find(x => x.name === val)
        
        if (checkValInAutoComplete) {
          console.log("inside if loop")
          this.autocompleteModel = checkValInAutoComplete
          console.log("checkValInAutoComplete", checkValInAutoComplete)
        }
        
        console.log("this.autocompleteModel 2", this.autocompleteModel)
        console.log("=== END updateAutoComplete() === ")
      },

      openDialogueIfCustomSelected(dateSelected) {
        if (dateSelected === 'Custom') {
          this.dialog = true
          this.emitFilterSelectionToDashboard(this.autocompleteModel, this.computedCustomDateFormatted, this.platformsSelected, this.sentimentsSelected, this.emotionsSelected);
        } else {
          this.emitFilterSelectionToDashboard(this.autocompleteModel, this.dateSelected, this.platformsSelected, this.sentimentsSelected, this.emotionsSelected);
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
    left: 19%;
  }

</style>
