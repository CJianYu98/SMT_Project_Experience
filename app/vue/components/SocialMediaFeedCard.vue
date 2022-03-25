<template>
  <v-card
    elevation="3"
    class="mx-8 mr-2 mt-8 rounded-lg"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6 mx-4">
      <v-img
        max-height="30"
        max-width="30"
        src="/facebook_icon.png"
        alt="facebook icon"
        class="mr-3"
      ></v-img>
        <!-- class="mx-auto" -->
        <!-- :src="`/${platform}_icon.png`"
        :alt="`${platform} icon`" -->
      Facebook
      <!-- {{ platform.name }} -->
    </v-card-title>
    <RelatedComments :related-comments="relatedComments"/>
  </v-card>
</template>

<script>
import RelatedComments from './RelatedPosts.vue'
export default {
  components: { 
    RelatedComments ,
  },
  props: {
    platform: {
      type: Object,
      required: true,
    },
    relatedComments: {
      type: Array,
      required: true,
    },
  },
}
</script>


<style scoped>

</style>

