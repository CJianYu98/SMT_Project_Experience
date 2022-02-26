<template>
  <v-card
    elevation="3"
    class="mr-8 mt-8 rounded-lg"
    height="100%"
  >
  <v-row no-gutters class="fill-height">
    <v-col cols="6">
      <v-card-title class="pb-4 accent--text text-h6">
        Top Complaints
        <HelpTextTooltip :help-text="complaintsWordCloudHelpText"/>
      </v-card-title>
      <ComplaintsWordCloud />
    </v-col>
    <v-divider vertical></v-divider>
    <v-col cols="6">
        <v-card-title class="pb-4 accent--text text-h6">
        Related Comments
        <HelpTextTooltip :help-text="complaintsCommentsHelpText"/>
      </v-card-title>
      <ComplaintsRelatedComments />
    </v-col>
  </v-row>
    

  </v-card>
</template>

<script>
import ComplaintsRelatedComments from './ComplaintsRelatedComments.vue'
import ComplaintsWordCloud from './ComplaintsWordCloud.vue'
import HelpTextTooltip from './HelpTextTooltip.vue'
export default {
  components: { 
    ComplaintsWordCloud, 
    ComplaintsRelatedComments, 
    HelpTextTooltip 
  },

  data: () => ({
    complaintsWordCloudHelpText: "Observe the most common complaint topics mentioned across the selected time period and platform(s).",
    complaintsCommentsHelpText: "Study the most common complaints, or, if a complaint keyword has been selected, the comments related to that complaint. Words highlighted in red are indicative of the negative sentiment.",
  }),
  
}
</script>


<style>

</style>

