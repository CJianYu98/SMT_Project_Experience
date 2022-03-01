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

export default {
  components: { 
    HelpTextTooltip,
    TrendingTopic,
  },
  props: {
    topFiveTopics: {
      type: Array,
    }
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
