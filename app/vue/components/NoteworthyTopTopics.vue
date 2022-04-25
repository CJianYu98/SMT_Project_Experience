<template>
  <v-chip-group column class="mx-7 mt-n6 mb-1">
    <p class="font-weight-medium primary--text mr-3 pt-1 text-h6">Most common topics </p>
    <v-chip
      class="primary trending-category mr-1 font-weight-bold"
      v-for="(topic) in noteworthyTopTopics"
      :key="topic"
    >
      {{ topic }}
    </v-chip>
  </v-chip-group>
</template>


<script>
export default {
  props: {
    noteworthyTopTopics: {
      type: Array,
      required: true
    }
  }
}
</script>


<style scoped>
.trending-category {
  cursor: default;
}
</style>