<template>
  <v-container 
    style="max-height: 500px" 
    class="overflow-y-auto"
  >
  <template
    v-for="(postsObj, objIndex) in relatedPosts"
  >
    <RelatedPost
      v-for="(post, index) in postsObj[viewSelected]"
      :key="index"
      :media="objIndex"
      :likes="post.likes"
      :date="post.datetime"
      :post="post.post"
      :topic="post.topic"
      :sentiment="post.sentiment"
      :emotion="post.emotion"
      :link="post.link"
      :img="post.img"
      :intent="post.intent"
    />
  </template>
  </v-container>
</template>

<script>
import RelatedPost from './RelatedPost.vue'

export default {
  components: {
    RelatedPost 
  },
  props: {
    relatedPosts: {
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
  },
}
</script>


<style>

</style>

