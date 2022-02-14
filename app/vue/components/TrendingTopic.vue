<template>
  <v-list-item>
    <v-list-item-content class="pt-1">
      <v-row>
        <v-col class="pb-1">
          <v-list-item-title 
            class="text-h6 mb-1 pl-3" 
            v-text="`${index+1}. ${topicAssigned.name}`"
          >
          </v-list-item-title>
        </v-col>
        <v-col>
          <v-list-item-subtitle v-text="`${topicAssigned.mentions.toLocaleString()} mentions`" class="text-right pr-3">></v-list-item-subtitle>
        </v-col>
      </v-row>

      <v-list-item-subtitle
        class="pl-3" 
      >
        <span 
          v-for="(mention, index) in topicAssigned.topThreeMentions"
          :key="mention"
          @click="emitQueryToDashboard(mention)"
        >
            {{ mention }}{{ (index+1 &lt; topicAssigned.topThreeMentions.length) ? ', ' : '' }}
        </span>

        <!-- 
          need to pass the mention to model
        -->
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
