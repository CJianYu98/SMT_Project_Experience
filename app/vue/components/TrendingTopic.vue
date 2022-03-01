<template>
  <v-list-item class="primary--text mb-1">
    <v-list-item-content class="pt-1 pb-0">
      <v-list-item-title 
        class="mb-1 font-weight-bold" 
        v-text="`${index+1}. ${topicAssigned.name}`"
      >
      </v-list-item-title>
      <v-row class="mb-n1">
        <v-col class="pb-1">
          <v-list-item-subtitle class="pl-3 pr-3 primary--text" v-text="`${topicAssigned.mentions.toLocaleString()} posts`">></v-list-item-subtitle>
        </v-col>
        <v-col class="pb-1">
          <TrendingTopicSentimentBarChart :trending-topic-sentiment="topicAssigned.sentiment" :sentiment-graph-id="'topic'+index"/>
        </v-col>
      </v-row>

      <v-list-item-subtitle
        class="pl-3 primary--text" 
      >
        <v-chip-group column>
          <v-chip
            class="primary trending-category mr-1"
            v-for="(mention) in topicAssigned.topThreeMentions"
            :key="mention"
            @click="passSelectedTrendingTopicToTopics(mention)"
          >
            {{ mention }}
          </v-chip>
        </v-chip-group>

        <!-- 
          1. pass the mention (inside trending topic component) to autocompleteModel (inside search filters component)
          2. pass the query into rerenderDashboard method (inside dashboard page)
        -->
      </v-list-item-subtitle>
      <!-- <bar-chart class="chartBox"></bar-chart> -->
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import TrendingTopicSentimentBarChart from './TrendingTopicSentimentBarChart.vue'
// import BarChart from '@/components/TrendiingTopicSentimentBarChart'
export default {
  components: { TrendingTopicSentimentBarChart },
  props: {
    index: {
      type: Number,
      required: true,
    },
    topicAssigned: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    
  }),
  methods: {
    passSelectedTrendingTopicToTopics(topic) {
      console.log("=== START passSelectedTrendingTopicToTopics ===")
      this.$emit('selectedTrendingTopicInTopics', topic)
      console.log("=== END passSelectedTrendingTopicToTopics ===")

    }
  }
}
</script>


<style scoped>
  .chartBox {
    width: 800px;
    height: 300px;
  }
.trending-category {
  cursor: pointer;
}
</style>
