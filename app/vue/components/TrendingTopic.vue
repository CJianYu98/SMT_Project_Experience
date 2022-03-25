<template>
  <v-container fluid>
  <v-list-item class="primary--text mx-2">
    <v-list-item-content class="pt-1 pb-0">
      <v-row>
        <v-col class="pb-0 pr-0">
          <v-list-item-title 
            class="mb-1 font-weight-bold pr-0" 
            v-text="`${index+1}. ${topicAssigned.name}`"
          >
          </v-list-item-title>
        </v-col>
        <v-col cols="5" class="pb-0">
          <v-list-item-subtitle class="primary--text text-right" v-text="`${topicAssigned.mentions.toLocaleString()} mentions`">></v-list-item-subtitle>
        </v-col>
      </v-row>
      <v-row class="mt-0 pl-3">
        <v-col class="pb-1 pt-0" cols="6">
          <TrendingTopicSentimentBarChart :trending-topic-sentiment="topicAssigned.sentiment" :sentiment-graph-id="'topic'+index"/>
        </v-col>
        <v-col class="pb-1 pt-0" cols="6">
          <TrendingTopicSentimentBarChart :trending-topic-sentiment="topicAssigned.emotions" :sentiment-graph-id="'topic'+`${index+5}`"/>
        </v-col>
      </v-row>

      <v-list-item-subtitle
        class="pl-3 mt-0" 
      >
        <span
          class="trending-category mr-1 text-wrap text-decoration-underline font-weight-medium trendingTopicsLink--text"
          v-for="(mention, index) in topicAssigned.topThreeMentions"
          :key="mention"
          @click="passSelectedTrendingTopicToTopics(mention)"
        >
          <template v-if="index !== 2">
            {{ mention }},
          </template>
          <template v-else>
            {{ mention }}
          </template>
        </span>
        <!-- <v-chip-group column>
          <v-chip
            class="primary trending-category mr-1"
            v-for="(mention) in topicAssigned.topThreeMentions"
            :key="mention"
            @click="passSelectedTrendingTopicToTopics(mention)"
          >
            {{ mention }}
          </v-chip>
        </v-chip-group> -->

        <!-- 
          1. pass the mention (inside trending topic component) to autocompleteModel (inside search filters component)
          2. pass the query into rerenderDashboard method (inside dashboard page)
        -->
      </v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
  <template v-if="index < 4">
    <v-divider class="mt-4 mb-n3"></v-divider>
  </template>
  </v-container>
</template>

<script>
import TrendingTopicSentimentBarChart from './TrendingTopicSentimentBarChart.vue'
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
