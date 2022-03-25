<template>
  <v-container style="max-height: 450px" class="overflow-y-auto">
    <RelatedComment
      v-for="(complaint, index) in relatedComments"
      :key="index"
      :media="complaint.media"
      :likes="complaint.likes"
      :date="complaint.date"
      :comment="complaint.comment"
      :topic="complaint.topic"
      :link="complaint.link"
    />
  </v-container>
</template>

<script>
import RelatedComment from './RelatedPost.vue'

export default {
  components: {
    RelatedComment 
  },
  props: {
    relatedComments: {
      type: Array,
      required: true
    },
  },
  data: () => ({

  }),
}
</script>


<style>

</style>

