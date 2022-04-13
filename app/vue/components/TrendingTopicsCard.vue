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
    <template v-if="pendingState">
      <LoadingPlaceholder/>
    </template>
    <template v-else-if="topFiveTopics.length === 0">
      <PlaceholderNoDataToShow/>
    </template>
    <template v-else>
      <v-row class="mx-1">
      <!-- <v-spacer></v-spacer> -->
        <v-col cols="6" class="pt-0">
          <GraphLegend 
            :graph-legend="keywordsWordCloudLegend"
            type="sentiment"
          />
        </v-col>
        <!-- <v-spacer></v-spacer> -->

        <v-col cols="6" class="pt-0">
          <GraphLegend
            :graph-legend="trendingTopicsEmotionsLegend"
            type="emotion"
          />
        </v-col>
        <!-- <v-spacer></v-spacer> -->
      </v-row>
      
      <TrendingTopic 
        v-for="(topic, i) in topFiveTopics" 
        :key="i"
        :index="i" 
        :topic-assigned="topic" 
        @selectedTrendingTopicInTopics="passTrendingTopicToDashboard"
      />
    </template>
  </v-card>
</template>

<script>
import HelpTextTooltip from './HelpTextTooltip.vue'
import TrendingTopic from './TrendingTopic.vue'
import GraphLegend from './GraphLegend.vue'
import PlaceholderNoDataToShow from './PlaceholderNoDataToShow.vue'
import LoadingPlaceholder from './LoadingPlaceholder.vue'

export default {
  components: { 
    HelpTextTooltip,
    TrendingTopic,
    GraphLegend,
    PlaceholderNoDataToShow,
    LoadingPlaceholder,
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
    pendingState: {
      type: Boolean,
      required: true
    },
  },
  data: () => ({
    trendingTopicsHelpText: "Study the 5 most popular topics out of 13 topics, associated sentiment and emotion analysis, number of mentions (posts and comments) related to the topic, and top 3 keywords associated with the topic.",
    selectedTrendingTopic: "",
  }),
  methods: {
    passTrendingTopicToDashboard(topic) {
      console.log("=== START passTrendingTopicToDashboard() ===")
      console.log(topic)
      this.$emit('clickQuery', topic)
      console.log("=== END passTrendingTopicToDashboard() ===")
    }
  }
}
</script>


<style>

</style>
