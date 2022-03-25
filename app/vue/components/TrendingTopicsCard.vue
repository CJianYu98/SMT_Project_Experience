<template>
  <v-card
    elevation="3"
    class="ml-8 mr-2 mt-8 rounded-lg"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6">
      Trending Topics
      <HelpTextTooltip :help-text="trendingTopicsHelpText"/>
    </v-card-title>
    <v-row class="mx-1">
      <!-- <v-spacer></v-spacer> -->
      <v-col cols="5">
        <GraphLegend 
          :graph-legend="keywordsWordCloudLegend"
        />
      </v-col>
      <!-- <v-spacer></v-spacer> -->

      <v-col cols="7">
        <GraphLegend
          :graph-legend="trendingTopicsEmotionsLegend"
        />
      </v-col>
      <!-- <v-spacer></v-spacer> -->
    </v-row>
    
    <TrendingTopic 
      v-for="(topic, i) in topFiveTopics" 
      :key="i"
      :index="i" 
      :topic-assigned="topic" 
      @selectedTrendingTopicInTopics="passTrendingTopicToTopics"
    />
    
  </v-card>
</template>

<script>
import HelpTextTooltip from './HelpTextTooltip.vue'
import TrendingTopic from './TrendingTopic.vue'
import GraphLegend from './GraphLegend.vue'

export default {
  components: { 
    HelpTextTooltip,
    TrendingTopic,
    GraphLegend,
  },
  props: {
    topFiveTopics: {
      type: Array,
    },
    keywordsWordCloudLegend: {
      type: Object,
      required: true
    },
    trendingTopicsEmotionsLegend: {
      type: Object,
      required: true
    },
  },
  data: () => ({
    trendingTopicsHelpText: "Study the most popular topics talked about within the selected time period across the platform(s) selected.",
    selectedTrendingTopic: "",
  }),
  methods: {
    passTrendingTopicToTopics(topic) {
      console.log("=== START passTrendingTopicToTopics() ===")
      console.log(topic)
      this.$emit('selectedTrendingTopicInDashboard', topic)
      console.log("=== END passTrendingTopicToTopics() ===")
    }
  }
}
</script>


<style>

</style>
