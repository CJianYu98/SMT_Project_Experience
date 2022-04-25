<template>
  <v-card
    elevation="3"
    class="mr-8 mt-11 rounded-lg"
    height="100%"
  >
    <v-row>
      <v-col cols="8" class="py-0">
        <v-card-title class="pb-4 accent--text text-h6">
          Noteworthy Posts
          <HelpTextTooltip :help-text="noteworthyPostHelpText"/>
        </v-card-title>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="3" class="py-0">
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
      <NoteworthyTopTopics
        v-if="noteworthyTopTopics.length > 0"
        :noteworthy-top-topics="noteworthyTopTopics"
      />
      <v-divider class="mb-2"></v-divider>
      <RelatedPosts
        :related-posts="relatedPosts"
        :view-selected="viewSelected.toLowerCase()"
      />
    </template>
  </v-card>
</template>


<script>
import LoadingPlaceholder from './LoadingPlaceholder.vue'
import NoteworthyTopTopics from './NoteworthyTopTopics.vue'
import RelatedPosts from './RelatedPosts.vue'
export default {
  components: { 
    RelatedPosts,
    LoadingPlaceholder,
    NoteworthyTopTopics,
  },
  props: {
    relatedPosts: {
      type: Object,
      required: true
    },
    pendingState: {
      type: Boolean,
      required: true
    },
    noteworthyTopTopics: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    noteworthyPostHelpText: "Observe the insightful posts made by users across multiple platforms. These are determined based on three classified intents: seeking/giving advice, educational or insightful.",
    sortView: ['Likes', 'Date'],
    label: 'Sort By (Descending)',
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








