<template>
  <v-container 
    style="max-height: 450px" 
    class="overflow-y-auto"
  >
  <template
    v-for="(commentsObj, objIndex) in relatedComments"
  >
    <RelatedComment
      v-for="(comment, index) in commentsObj[viewSelected]"
      :key="index"
      :media="objIndex"
      :likes="comment.likes"
      :date="this.getFormatedDate(comment.datetime)"
      :comment="comment.comment"
      :topic="comment.topic"
      :sentiment="comment.sentiment"
      :emotion="comment.emotion"
      :link="comment.link"
      :img="comment.img"
      :intent="comment.intent"
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
    viewSelected: {
      type: String,
      required: true
    }
  },
  data: () => ({

  }),
  methods: {
    getFormatedDate(datetime) {
      const [year, month, date] = datetime.split('T')[0].split('-')
      return `${date}/${month}/${year}`
    }
    
  },
}
</script>


<style>

</style>

