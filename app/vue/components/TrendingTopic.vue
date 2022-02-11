<template>
  <v-list-item>
    <v-list-item-content class="pt-1">
      <v-list-item-title class="text-h6 mb-1" v-text="`${index+1}. ${topicAssigned.name}`">
      </v-list-item-title>
      <v-list-item-subtitle v-text="`${topicAssigned.mentions} mentions`"></v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
export default {
  data: () => ({
    
  }),
  props: {
    index: {
      type: Number,
    },
    topicAssigned: {
      topic: Object,
    }
  },
}
</script>


<style>

</style>
