<template>
  <div class="mb-10">
    <SearchFilters/>
    <v-row>
      <v-col cols="3">
        <SocialMediaFeedAllPlatformMetrics/>
      </v-col>
      <v-col cols="3">
      </v-col>
      <v-col cols="3">
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="3">
      </v-col>
      <v-col cols="3">
      </v-col>
      <v-col cols="3">
      </v-col>
    </v-row>
  </div>
</template>

<script>
import SocialMediaFeedAllPlatformMetrics from '../components/SocialMediaFeedAllPlatformMetrics.vue'
import SearchFilters from '@/components/SearchFilters'
export default {
  components: { 
    SearchFilters,
    SocialMediaFeedAllPlatformMetrics,
  },
  data: () => ({
    
  })
}
</script>


<style>

</style>
