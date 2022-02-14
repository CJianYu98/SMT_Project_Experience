<template>
  <v-list-item>
    <v-list-item-content class="pt-1">
      <v-row>
        <v-col>
          <v-list-item-title 
            class="text-h6 mb-1" 
            v-text="`${index+1}. ${topicAssigned.name}`"
            @click="emitQueryToDashboard(topicAssigned.name)"
          >
          </v-list-item-title>
        </v-col>
        <v-col>
          <v-list-item-subtitle v-text="`${topicAssigned.mentions} mentions`"></v-list-item-subtitle>
        </v-col>
      </v-row>
      <v-list-item-subtitle v-text="`${topicAssigned.topThreeMentions.join(', ')}`"></v-list-item-subtitle>

      <v-list-item-subtitle 
        v-for="mention in topicAssigned.topThreeMentions"
        :key="mention"
        @click="emitQueryToDashboard(mention)"
      >
        <!-- {{ mention }} -->
        <!-- <a :href="'/job/' + r.id"></a> -->
      </v-list-item-subtitle>

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
  methods: {
    emitQueryToDashboard(topic) {
      console.log("=== START emitQueryToDashboard ===")
      this.$emit('clickQuery', topic)
      console.log("=== END emitQueryToDashboard ===")

    }
  }
}
</script>


<style>

</style>
