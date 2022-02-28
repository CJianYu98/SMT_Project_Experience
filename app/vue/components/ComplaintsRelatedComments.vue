<template>
  <div>
    <ComplaintsRelatedComment
      v-for="complaint in complaintsRelatedComments"
      :key="complaint"
      :media="complaint.media"
      :likes="complaint.likes"
      :date="complaint.date"
      :comment="complaint.comment"
      :topic="complaint.topic"
    />
  </div>
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

