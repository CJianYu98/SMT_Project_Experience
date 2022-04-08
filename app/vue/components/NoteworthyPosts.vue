<template>
  <v-card
    elevation="3"
    class="mr-8 mt-11 rounded-lg"
    height="100%"
  >
    <v-row>
      <v-col cols="8" class="pt-0">
        <v-card-title class="pb-4 accent--text text-h6">
          Noteworthy Posts
          <HelpTextTooltip :help-text="noteworthyCommentHelpText"/>
        </v-card-title>
      </v-col>
      <v-col class="pt-0">
        <DropDownSelect 
          :view-filter="sortView" 
          :label="label"
          :view-selected="viewSelected"
          @changeView="passViewToComments($event)">
        </DropDownSelect>
      </v-col>
    </v-row>
    <RelatedPosts
      :related-comments="relatedComments"
      :view-selected="viewSelected.toLowerCase()"
    />
  </v-card>
</template>


<script>
import RelatedPosts from './RelatedPosts.vue'
export default {
  components: { 
    RelatedPosts
  },
  props: {
    relatedComments: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    noteworthyCommentHelpText: "Observe the insightful comments made by users across multiple platforms. These are determined based on three classified intents: seeking/giving advice, educational or insightful.",
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








