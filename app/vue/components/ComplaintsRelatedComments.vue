<template>
  <v-container style="max-height: 450px" class="overflow-y-auto">
    <ComplaintsRelatedComment
      v-for="complaint in complaintsRelatedComments"
      :key="complaint"
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
import ComplaintsRelatedComment from './ComplaintsRelatedComment.vue'

export default {
  components: {
    ComplaintsRelatedComment 
  },
  props: {
    complaintsRelatedComments: {
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

