<template>
  <!-- <v-app> -->
  <div id="searchFilter" class="mt-2 mb-n3">
    <v-container fluid class="px-8 mt-n2 pb-0">
      <v-row no-gutters align="stretch">
        <v-col
          cols="3"
          class="d-flex"
        >
          <v-autocomplete
            v-if="selectedTrendingQuery"
            v-model="autocompleteModel"
            :items="items"
            :loading="isLoading"
            chips
            clearable
            hide-details
            hide-selected
            item-text="name"
            item-value="symbol"
            label="Enter a keyword you are interested in!"
            solo
            dense
            return-object
          >
            <!-- :label="selectedTrendingQuery" -->
                      <!-- return-object -->
            <!-- <template v-slot:no-data>
              <v-list-item>
                <v-list-item-title>
                  Search for your favorite
                  <strong>Cryptocurrency</strong>
                </v-list-item-title>
              </v-list-item>
            </template> -->
            <template #selection="{ attr, on, item, selected }">
              <v-chip
                v-bind="attr"
                :input-value="selected"
                class="primary--text"
                v-on="on"
                small
              >
                <!-- <v-icon left>
                  mdi-bitcoin
                </v-icon> -->
                <span v-text="item.name"></span>
              </v-chip>
            </template>
            <template #item="{ item }">
              <v-list-item-avatar
                color="indigo"
                class="text-h5 font-weight-light white--text"
              >
                {{ item.name.charAt(0) }}
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-text="item.name"></v-list-item-title>
                <v-list-item-subtitle v-text="item.symbol"></v-list-item-subtitle>
              </v-list-item-content>
              <!-- <v-list-item-action>
                <v-icon>mdi-bitcoin</v-icon>
              </v-list-item-action> -->
            </template>
          </v-autocomplete>

          <v-autocomplete
            v-else
            v-model="autocompleteModel"
            :items="items"
            :loading="isLoading"
            :search-input.sync="search"
            chips
            clearable
            hide-details
            hide-selected
            item-text="name"
            item-value="symbol"
            label="Enter a keyword you are interested in!"
            solo
            dense
            return-object
          >
                      <!-- return-object -->
            <!-- <template v-slot:no-data>
              <v-list-item>
                <v-list-item-title>
                  Search for your favorite
                  <strong>Cryptocurrency</strong>
                </v-list-item-title>
              </v-list-item>
            </template> -->
            <template #selection="{ attr, on, item, selected }">
              <v-chip
                v-bind="attr"
                :input-value="selected"
                class="primary--text"
                v-on="on"
                small
              >
                <span v-text="item.name"></span>
              </v-chip>
            </template>
            <template #item="{ item }">
              <v-list-item-avatar
                color="indigo"
                class="text-h5 font-weight-light white--text"
              >
                {{ item.name.charAt(0) }}
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-text="item.name"></v-list-item-title>
                <v-list-item-subtitle v-text="item.symbol"></v-list-item-subtitle>
              </v-list-item-content>
              <!-- <v-list-item-action>
                <v-icon>mdi-bitcoin</v-icon>
              </v-list-item-action> -->
            </template>
          </v-autocomplete>
        </v-col>
        <v-spacer></v-spacer>
        <v-col
          class="d-flex"
          cols="2"
        >
          <v-select
            v-model="dateSelected"
            d-block
            :items="dateFilter"
            item-text="date"
            label="Select a date period"
            outlined
            @change="openDialogueIfCustomSelected(dateSelected);"
          >
            <template slot="selection" slot-scope="data">
              <span v-if="data.item.date === 'Custom' && dateRange.length === 1" class="accent--text">{{ dateRange[0] }}</span>
              <span v-else-if="data.item.date === 'Custom' && dateRange.length > 1" class="accent--text">{{ dateRange.join(" - ") }}</span>
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
              <v-spacer></v-spacer>
            </v-date-picker>
          </v-dialog>
        </v-col>
        <v-spacer></v-spacer>
        <v-col
          cols="3"
        >
          <v-select
            v-model="sentimentsSelected"
            :items="sentimentsFilter"
            small-chips
            label="Sentiment Filter"
            multiple
            outlined
            dense
            @change="emitFilterSelectionToDashboard(autocompleteModel, dateSelected, platformsSelected, sentimentsSelected)"
          >
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
            <template #selection="{ item }">
              <v-chip 
                color="accent"
                outlined
                class="my-1"
                small
              >
                {{item}}
              </v-chip>
            </template>
          </v-select>
        </v-col>
        <v-spacer></v-spacer>
        <v-col
          cols="3"
        >
          <v-select
            v-model="platformsSelected"
            :items="platformsFilter"
            small-chips
            label="Platform Filter"
            multiple
            outlined
            dense
            @change="emitFilterSelectionToDashboard(autocompleteModel, dateSelected, platformsSelected, sentimentsSelected)"
          >
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
            <template #selection="{ item }">
              <v-chip 
                color="accent"
                outlined
                class="my-1"
                small
              >
                {{item}}
              </v-chip>
            </template>
          </v-select>
        </v-col>
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

    data: () => ({
      isLoading: false,
      items: [],
      autocompleteModel: null, // stores the symbol (value), not the name (text)
      search: null,
      tab: null,
      menu1: false,
      menu: false,
      date: null,
      dateRange: ['2019-09-10', '2019-09-20'],
      dateSelected: "All",
      dateFilter: [{date: 'All'}, {date: 'Yesterday'}, {date: 'Past 7 Days'}, {date: 'Past 14 Days'}, {date: 'Past 30 Days'}, {date: 'Past 6 Months'}, {date: 'Past Year'}, {date: 'Custom'}],
      dialog: false,
      sentimentsFilter: ['Negative', 'Neutral', 'Positive'],
      sentimentsSelected: ['Negative', 'Neutral', 'Positive'],
      platformsFilter: ['Facebook', 'Reddit', 'Twitter', 'YouTube'],
      platformsSelected: ['Facebook', 'Reddit', 'Twitter', 'YouTube'],
    }),

    computed: {
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
    },

    watch: {
      model (val) {
        if (val != null) this.tab = 0
        else this.tab = null
      },

      search: {
        handler(val) {
          if (this.items.length > 0) return
            this.isLoading = true

          // Lazily load input items
          fetch('https://api.coingecko.com/api/v3/coins/list')
            .then(res => res.clone().json())
            .then(res => {
              this.items = res
              console.log("UNDER WATCH this.items", this.items)
            })
            .catch(err => {
              console.log(err)
            })
            .finally(() => (this.isLoading = false))
        },
        immediate: true
      },

      selectedTrendingQuery (newVal, oldVal) { // watch it
        console.log('Prop changed: ', newVal, ' | was: ', oldVal)
        console.log("this.autocompleteModel 1", this.autocompleteModel)
        this.updateAutoComplete(newVal)

        this.emitFilterSelectionToDashboard(this.autocompleteModel, this.dateSelected, this.platformsSelected, this.sentimentsSelected)
      },
    },

    mounted() {
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
      emitFilterSelectionToDashboard(autocompleteModel, dateSelected, platformsSelected, sentimentsSelected) {
        this.$emit('changeFilter', [autocompleteModel, dateSelected, platformsSelected, sentimentsSelected])
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
        }
        this.emitFilterSelectionToDashboard(this.autocompleteModel, dateSelected, this.platformsSelected, this.sentimentsSelected);
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
  >>> .custom-dialog-datepicker {
    position: absolute;
    top: 10%;
    left: 29%;
  }
</style>
