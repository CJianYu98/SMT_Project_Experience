<template>
  <v-card
    elevation="3"
    class="mx-8 mt-8"
  >
    <v-card-title class="pb-4 accent--text">
      Trending Topics
      <HelpTextTooltip :help-text="trendingTopicsHelpText"/>
    </v-card-title>

    <v-row
      v-for="(topic, i) in topFiveTopics"
      :key="i"
    >
      <v-col class="py-0">
        <TrendingTopic :index="i" :topic-assigned="topic" v-on="$listeners"/>
      </v-col>
    </v-row>
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
  }),
}
</script>


<style>

</style>
