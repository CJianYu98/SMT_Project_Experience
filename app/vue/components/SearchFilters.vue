<template>
  <v-app>
    <v-container fluid class="px-8 mt-n1">
      <v-row no-gutters align="stretch">
        <v-col
          cols="3"
          class="d-flex"
        >
          <v-autocomplete
            v-model="model"
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
          >
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
                color="blue-grey"
                class="white--text"
                v-on="on"
              >
                <v-icon left>
                  mdi-bitcoin
                </v-icon>
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
              <v-list-item-action>
                <v-icon>mdi-bitcoin</v-icon>
              </v-list-item-action>
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
            :items="dateFilter"
            item-text="date"
            label="Select a date period"
            outlined
            dense
          >
            <template slot="selection" slot-scope="data">
              <span v-if="data.item.date === 'Custom'" >{{ data.item.period }}</span>
              <span v-else >{{ data.item.date }}</span>
            </template>

          </v-select>
          <!-- <v-date-picker v-model="dateRange" no-title range scrollable v-if="dateSelected == 'Custom'">
            <v-spacer></v-spacer>
          </v-date-picker> -->

        </v-col>
        <!-- <v-spacer></v-spacer>
        <v-col> -->
          <!-- <v-date-picker
            v-model="dateRange"
            range
            no-title
            v-if="dateSelected == 'Custom'"
          ></v-date-picker> -->

        <!-- template for vmenu and date picker inside menu -->
        <!-- <v-menu
          ref="menu"
          v-model="menu"
          :close-on-content-click="false"
          :return-value.sync="date"
          transition="scale-transition"
          offset-y
          min-width="290px"
          nudge-right="300px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="date"
              label="Picker in menu"
              prepend-icon="event"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker v-model="date" no-title scrollable>
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
            <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
          </v-date-picker>
        </v-menu> -->

      <!-- <v-menu
          ref="menu"
          v-model="menu"
          :close-on-content-click="false"
          :return-value.sync="dateRange"
          transition="scale-transition"
          offset-y
          min-width="290px"
          nudge-right="300px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="dateRange"
              label="Picker in menu"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker v-model="dateRange" no-title range scrollable>
            <v-spacer></v-spacer>
          </v-date-picker>
        </v-menu> -->



          <!-- <v-date-picker v-model="dateRange" no-title range scrollable>
            <v-spacer></v-spacer>
          </v-date-picker> -->
        <!-- </v-col> -->
        <!-- </v-row>
        <v-row> -->
        <v-spacer></v-spacer>
        <v-col
          cols="2"
        >
          <v-select
            v-model="sentimentsSelected"
            :items="sentimentsFilter"
            small-chips
            label="Sentiment Filter"
            multiple
            outlined
            dense
          >
            <template #prepend-item>
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
            </template>
            <template #selection="{ item }">
              <v-chip 
                color="blue"
                outlined
                class="my-1"
              >
                {{item}}
              </v-chip>
            </template>
          </v-select>
        </v-col>
        <v-spacer></v-spacer>
        <v-col
          cols="4"
        >
          <v-select
            v-model="platformsSelected"
            :items="platformsFilter"
            small-chips
            label="Platform Filter"
            multiple
            outlined
            dense
          >
            <template #prepend-item>
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
            </template>
            <template #selection="{ item }">
              <v-chip 
                color="blue"
                outlined
                class="my-1"
              >
                {{item}}
              </v-chip>
            </template>
          </v-select>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
  export default {
    data: () => ({
      isLoading: false,
      items: [],
      model: null,
      search: null,
      tab: null,
      menu1: false,
      menu: false,
      date: null,
      dateRange: ['2019-09-10', '2019-09-20'],
      // date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
      dateSelected: "All",
      dateFilter: [{date: 'All'}, {date: 'Yesterday'}, {date: 'Past 7 Days'}, {date: 'Past 14 Days'}, {date: 'Past 30 Days'}, {date: 'Past 6 Months'}, {date: 'Past Year'}, {date: 'Custom', period: ['2019-09-10', '2019-09-20'].join()}],
      // this.dateRange.join()
      sentimentsFilter: ['Negative', 'Neutral', 'Positive'],
      sentimentsSelected: ['Negative', 'Neutral', 'Positive'],
      platformsFilter: ['Facebook', 'Instagram', 'Reddit', 'Twitter', 'YouTube'],
      platformsSelected: ['Facebook', 'Instagram', 'Reddit', 'Twitter', 'YouTube'],
    }),

    computed: {
      allPlatformsSelected () {
        return this.platformsSelected.length === this.platformsFilter.length
      },
      somePlatformsSelected () {
        return this.platformsSelected.length > 0 && !this.allPlatformsSelected
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
        return this.sentimentsSelected.length > 0 && !this.allSentimentsSelected
      },
      sentimentIcon () {
        if (this.allSentimentsSelected) return 'mdi-close-box'
        if (this.someSentimentsSelected) return 'mdi-minus-box'
        return 'mdi-checkbox-blank-outline'
      },
    },

    watch: {
      model (val) {
        if (val != null) this.tab = 0
        else this.tab = null
      },
      search (val) {
        // Items have already been loaded
        if (this.items.length > 0) return

        this.isLoading = true

        // Lazily load input items
        fetch('https://api.coingecko.com/api/v3/coins/list')
          .then(res => res.clone().json())
          .then(res => {
            this.items = res
          })
          .catch(err => {
            console.log(err)
          })
          .finally(() => (this.isLoading = false))
      },
    },

    methods: {
      toggle () {
        this.$nextTick(() => {
          if (this.allPlatformsSelected) {
            this.platformsSelected = []
          } else {
            this.platformsSelected = this.platformsFilter.slice()
          }
        })
      }
    },

  }
</script>

<style>

</style>


