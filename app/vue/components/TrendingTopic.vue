<template>
  <v-list-item class="primary--text">
    <v-list-item-content class="pt-1">
      <v-row>
        <v-col class="pb-1">
          <v-list-item-title 
            class="mb-1 pl-3 font-weight-bold" 
            v-text="`${index+1}. ${topicAssigned.name}`"
          >
          </v-list-item-title>
        </v-col>
        <v-col>
          <v-list-item-subtitle class="text-right pr-3 primary--text" v-text="`${topicAssigned.mentions.toLocaleString()} mentions`">></v-list-item-subtitle>
        </v-col>
      </v-row>

      <v-list-item-subtitle
        class="pl-3 primary--text" 
      >
        <span 
          v-for="(mention, index) in topicAssigned.topThreeMentions"
          :key="mention"
          @click="emitQueryToDashboard(mention)"
        >
            {{ mention }}{{ (index+1 &lt; topicAssigned.topThreeMentions.length) ? ', ' : '' }}
        </span>

        <!-- 
          1. pass the mention (inside trending topic component) to autocompleteModel (inside search filters component)
          2. pass the query into rerenderDashboard method (inside dashboard page)
        -->
      </v-list-item-subtitle>

    </v-list-item-content>
  </v-list-item>
</template>

<script>
export default {
  props: {
    index: {
      type: Number,
      required: true,
    },
    topicAssigned: {
      type: Object,
      required: true,
    }
  },
  data: () => ({
    
  }),
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
