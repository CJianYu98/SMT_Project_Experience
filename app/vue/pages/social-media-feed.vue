<template>
  <div>
    <SearchFilters/>
    <v-row>
      <v-col cols="5">
        <TrendingTopics :top-five-topics="topFiveTopicsData"/>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import TrendingTopics from '@/components/TrendingTopics.vue'
import SearchFilters from '@/components/SearchFilters'
export default {
  components: { 
    TrendingTopics,            
    SearchFilters,
  },
  
}
</script>


<style>

</style>
