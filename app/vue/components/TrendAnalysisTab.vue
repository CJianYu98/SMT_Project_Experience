<template>
<v-card>
    <v-card flat >
        <v-container fluid class="px-4 mt-n4 pb-0">
            <v-row no-gutters align="stretch">
                <v-col class="d-flex">
                  <v-card-title class="text-h5">
                    Number of Posts
                  </v-card-title>
                  <v-spacer></v-spacer>
                  <DropDownSelect :viewFilter="allView" :label="label"></DropDownSelect>
                </v-col>
            </v-row>
        </v-container>
    </v-card>
    <v-card>
        <line-chart class="chartBox" :chartData="allChartData"></line-chart>
    </v-card> 
</v-card>
</template>

<script>
import DropDownSelect from "./DropDownSelect.vue"
import LineChart from '@/components/TrendAnalysisLineChart'

export default {
    props:{
        // chartData
    },
    components: {
        DropDownSelect,
        LineChart,
    },
    data: () => {
        
    }
}
</script>

<style>
  .chartBox {
    width: 800px;
    height: 360px;
  }
</style>