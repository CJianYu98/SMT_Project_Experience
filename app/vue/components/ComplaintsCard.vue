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
      <ComplaintsWordCloud  :complaints-word-cloud="complaintsWordCloud"/>
    </v-col>
    <v-divider vertical></v-divider>
    <v-col cols="6">
      <v-row>
        <v-col cols="8">
          <v-card-title class="pb-4 accent--text text-h6">
            Related Posts
            <HelpTextTooltip :help-text="complaintsCommentsHelpText"/>
          </v-card-title>
        </v-col>
        <v-col>
          <DropDownSelect 
            :view-filter="sortView" 
            :label="label"
            :view-selected="viewSelected"
            @changeView="passViewToComments($event)">
          </DropDownSelect>
        </v-col>
      </v-row>
      <ComplaintsRelatedComments 
        :related-comments="relatedComments"
        :view-selected="viewSelected.toLowerCase()"
      />
    </v-col>
  </v-row>
    

  </v-card>
</template>

<script>
import ComplaintsRelatedComments from './RelatedPosts.vue'
import ComplaintsWordCloud from './ComplaintsWordCloud.vue'
import DropDownSelect from './DropDownSelect.vue'
import HelpTextTooltip from './HelpTextTooltip.vue'
export default {
  components: { 
    ComplaintsWordCloud, 
    ComplaintsRelatedComments, 
    HelpTextTooltip,
    DropDownSelect,
  },

  props: {
    complaintsWordCloud: {
      type: Array,
      required: true
    },
    relatedComments: {
      type: Object,
      required: true
    },
  },

  data: () => ({
    complaintsWordCloudHelpText: "Observe the most common keywords related to complaints mentioned across the selected time period and platform(s).",
    complaintsCommentsHelpText: "Study the most common complaints, or, if a complaint keyword has been selected, the comments related to that complaint. Words highlighted in red are indicative of the negative sentiment.",
    sortView: ['Likes', 'Date'],
    label: 'Sort By',
    viewSelected: 'Likes'
  }),
  methods: {
    passViewToComments(changedView) {
      console.log("=== start passViewToComments() ===")
      console.log("selectedView", changedView)
      this.viewSelected = changedView
    }
  },
  
}
</script>


<style>

</style>

