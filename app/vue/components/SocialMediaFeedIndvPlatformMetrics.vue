<template>
  <v-container fluid class="px-0 py-0">
    <v-row class="d-flex align-center">
      <v-col cols="5" class="pr-0 py-0">
        <v-img
          max-height="40"
          contain
          :src="`/${platformString}_icon.png`"
          :alt="`${platformString} icon`"
          class="mx-auto"
        ></v-img>
        <p :class="`${platformString}--text mt-2 mb-1 text-h6 text-center`">
            {{ platformString.toUpperCase() }}
        </p>
      </v-col>
      <v-col cols="6" class="pl-0 py-0">
        <p class="mb-0 primary--text text-h5 text-center pt-6">
          {{ platformAllData.mentions.toLocaleString() }}
        </p>
        <p class="accent--text text-h7 text-center font-weight-medium">
          mentions
        </p>
      </v-col>
    </v-row>
    <v-row class="mb-2">
      <v-col cols="11" class="py-0">
        <template v-if="!platformAllData.sentiment.find(sentimentObj => sentimentObj.percentage === 'NaN')">
          <TrendingTopicSentimentBarChart
            :trending-topic-sentiment="platformAllData.sentiment"
            :sentiment-graph-id="'sentiment'+platformString" 
          />
        </template>
      </v-col>
    </v-row>
    <v-row class="mb-1">
      <v-col cols="11" class="py-0">
        <template v-if="!platformAllData.emotions.find(emotionObj => emotionObj.percentage === 'NaN')">
          <TrendingTopicSentimentBarChart 
          :trending-topic-sentiment="platformAllData.emotions" 
          :sentiment-graph-id="'emotion'+platformString"
        />
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>


<script>
export default {
  components: { 
  },
  props: {
    platformAllData: {
      type: Object,
      required: true,
    },
    platformString: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    aggregatedStatsHelpText: "These aggregated statistics are based on the filters that are selected.",
  })
}
</script>


<style scoped>

</style>




