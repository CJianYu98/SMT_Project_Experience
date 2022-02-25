<template>
  <v-card
    elevation="3"
    class="mx-8 mt-8"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6">
      Noteworthy Comment
      <HelpTextTooltip :help-text="noteworthyCommentHelpText"/>
    </v-card-title>
    <NoteworthyComment />
  </v-card>
</template>


<script>
import NoteworthyComment from './NoteworthyComment.vue'
export default {
  components: { 
    NoteworthyComment 
  },
  
  data: () => ({
    noteworthyCommentHelpText: "Observe the insightful comments made by users across multiple platforms. These are determined based on (...)",
  }),
}
</script>


<style>

</style>








