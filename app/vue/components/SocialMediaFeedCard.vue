<template>
  <v-card
    elevation="3"
    class="mx-8 mt-8 rounded-lg"
    height="100%"
  >
    <!-- :style="{'border': `2px ${$vuetify.theme.themes[light].facebook} solid;`}" -->
    <v-row>
      <v-col cols="8" class="py-0">
        <v-card-title class="pb-4 accent--text text-h6 mx-4">
          <v-img
            max-height="30"
            max-width="30"
            :src="`/${platform}_icon.png`"
            :alt="`${platform} icon`"
            class="mr-3"
          ></v-img>
          <span :class="`${platform}--text`">
            {{ platform.toUpperCase() }}
          </span>
        </v-card-title>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="3" class="py-0">
          <!-- v-if="!('platform' in relatedPosts)&& !pendingState" -->
        <DropDownSelect
          :view-filter="sortView" 
          :label="label"
          :view-selected="viewSelected"
          @changeView="passViewToPosts($event)">
        </DropDownSelect>
      </v-col>
    </v-row>
    <RelatedPosts
        :related-posts="platformAllData"
        :view-selected="viewSelected.toLowerCase()"
    />
  </v-card>
</template>

<script>
import RelatedPosts from './RelatedPosts.vue'
export default {
  components: { 
    RelatedPosts,
  },
  props: {
    platformAllData: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    sortView: ['Likes', 'Date'],
    label: 'Sort By',
    viewSelected: 'Likes'
  }),
  computed: {
    platform() {
      // console.log("this.platformAllData", this.platformAllData)
      // console.log("Object.keys(this.platformAllData)", Object.keys(this.platformAllData))
      // console.log("Object.keys(this.platformAllData)[0]", Object.keys(this.platformAllData)[0])
      return Object.keys(this.platformAllData)[0]
    },
  },
  methods: {
    passViewToPosts(changedView) {
      // console.log("=== start passViewToPosts() ===")
      // console.log("selectedView", changedView)
      this.viewSelected = changedView
    }
  },
}
</script>


<style scoped>

</style>

