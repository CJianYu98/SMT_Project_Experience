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
      <template v-if="pendingState">
        <LoadingPlaceholder/>
      </template>
      <template v-else-if="complaintsWordCloud.length > 0">
        <ComplaintsWordCloud  :complaints-word-cloud="complaintsWordCloud"/>
      </template>
      <template v-else>
        <PlaceholderNoDataToShow />
      </template>
    </v-col>
    <v-divider vertical></v-divider>
    <v-col cols="6">
      <v-row>
        <v-col cols="6" class="pb-0">
          <v-card-title class="pb-4 accent--text text-h6">
            Related Posts
            <HelpTextTooltip :help-text="complaintsPostsHelpText"/>
          </v-card-title>
        </v-col>
        <v-col cols="6" class="pb-0">
          <DropDownSelect 
            v-if="!('platform' in relatedPosts) && !pendingState"
            :view-filter="sortView" 
            :label="label"
            :view-selected="viewSelected"
            @changeView="passViewToPosts($event)">
          </DropDownSelect>
        </v-col>
      </v-row>
      <template v-if="pendingState">
        <LoadingPlaceholder/>
      </template>
      <template v-else-if="'platform' in relatedPosts">
        <PlaceholderNoDataToShow />
      </template>
      <template v-else>
        <ComplaintsRelatedPosts 
          :related-posts="relatedPosts"
          :view-selected="viewSelected.toLowerCase()"
        />
      </template>
    </v-col>
  </v-row>
    

  </v-card>
</template>

<script>
import ComplaintsRelatedPosts from './RelatedPosts.vue'
import ComplaintsWordCloud from './ComplaintsWordCloud.vue'
import DropDownSelect from './DropDownSelect.vue'
import HelpTextTooltip from './HelpTextTooltip.vue'
import PlaceholderNoDataToShow from './PlaceholderNoDataToShow.vue'
import LoadingPlaceholder from './LoadingPlaceholder.vue'
export default {
  components: { 
    ComplaintsWordCloud, 
    ComplaintsRelatedPosts, 
    HelpTextTooltip,
    DropDownSelect,
    PlaceholderNoDataToShow,
    LoadingPlaceholder,
  },

  props: {
    complaintsWordCloud: {
      type: Array,
      required: true
    },
    relatedPosts: {
      type: Object,
      required: true
    },
    pendingState: {
      type: Boolean,
      required: true
    },
  },

  data: () => ({
    complaintsWordCloudHelpText: "Observe the most common keywords related to complaints mentioned across the selected time period and platform(s).",
    complaintsPostsHelpText: "Study the most common complaints, or, if a complaint keyword has been selected, the posts related to that complaint. Words highlighted in red are indicative of the negative sentiment.",
    sortView: ['Likes', 'Date'],
    label: 'Sort By',
    viewSelected: 'Likes'
  }),
  methods: {
    passViewToPosts(changedView) {
      console.log("=== start passViewToPosts() ===")
      console.log("selectedView", changedView)
      this.viewSelected = changedView
    }
  },
  
}
</script>


<style>

</style>

