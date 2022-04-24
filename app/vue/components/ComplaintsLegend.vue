<template>
  <!-- <div class="mb-3 mt-3"> -->
  <v-container >
    <v-row class="d-flex justify-center">
      <p class="mb-0 primary--text font-weight-bold">
        Percentage Complaints Per Platform
      </p>
    </v-row> 
    <v-row class="mx-2">
      <v-col
        cols="3"
        v-for="(percentage, platform) in complaintMentionsPerPlatform"
        :key="platform"
        class="px-0 py-0">
        <ComplaintsPlatform :platform-name="platform" :platform-percentage="percentage"/>
      </v-col>
      
    </v-row>
  </v-container>
  <!-- </div> -->
</template>


<script>
import ComplaintsPlatform from './ComplaintsPlatform.vue'
export default {
  components: { ComplaintsPlatform },
  props: {
    complaintMentionsPerPlatform: {
      type: Object,
      required: true
    },
  },
}
</script>


<style scoped>

</style>
