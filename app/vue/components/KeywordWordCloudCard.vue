<template>
  <v-card
    elevation="3"
    class="ml-8 mr-2 mt-8 rounded-lg"
    height="100%"
  >
    <v-card-title class="pb-4 accent--text text-h6">
      Top Keywords
      <HelpTextTooltip :help-text="wordcloudHelpText"/>
    </v-card-title>
    <template v-if="pendingState">
      <LoadingPlaceholder/>
    </template>
    <template v-else-if="keywordsWordCloud.length > 0">
      <GraphLegend :graph-legend="keywordsWordCloudLegend" type="sentiment"/>
      <KeywordWordCloud :keywords-word-cloud="keywordsWordCloud" :keywords-word-cloud-legend="keywordsWordCloudLegend"/>
    </template>
    <template v-else>
      <PlaceholderNoDataToShow/>
    </template>
  </v-card>
</template>

<script>
import HelpTextTooltip from './HelpTextTooltip.vue'
import KeywordWordCloud from './KeywordWordCloud.vue'
import GraphLegend from './GraphLegend.vue'
import PlaceholderNoDataToShow from './PlaceholderNoDataToShow.vue'
import LoadingPlaceholder from './LoadingPlaceholder.vue'
export default {
  components: {
    HelpTextTooltip,
    KeywordWordCloud,
    GraphLegend,
    PlaceholderNoDataToShow,
    LoadingPlaceholder,
  },
  props: {
    keywordsWordCloud: {
      type: Array,
      required: true
    },
    keywordsWordCloudLegend: {
      type: Object,
      required: true
    },
    pendingState: {
      type: Boolean,
      required: true
    },
  },
  data: () => ({
    wordcloudHelpText: "Observe the most popular keywords associated with the query. In the case where there is no query, the keywords shown are aggregated across all data according to the filters.",
    })
}
</script>


<style>

</style>

