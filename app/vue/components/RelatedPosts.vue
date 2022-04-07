<template>
  <v-container 
    style="max-height: 450px" 
    class="overflow-y-auto"
  >
  <!-- v-bind:style= "[condition ? {styleA} : {styleB}]" -->
  <template
    v-for="(commentsObj, index) in relatedComments"
  >
    <RelatedComment
      v-for="comment in commentsObj.likes"
      :key="comment"
      :media="index"
      :likes="comment.likes"
      :date="comment.date"
      :comment="comment.comment"
      :topic="comment.topic"
      :sentiment="comment.sentiment"
      :emotion="comment.emotion"
      :link="comment.link"
      :img="comment.img"
    />
  </template>
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
      type: Object,
      required: true
    },
    // selectedView: {
    //   type: String,
    //   required: true
    // }
  },
  data: () => ({

  }),
}
</script>


<style>

</style>

