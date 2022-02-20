<template>
  <v-card
    elevation="3"
    class="mx-8 mt-8"
  >
    <v-card-title class="pb-4 accent--text">
      Top Keywords
      <HelpTextTooltip :help-text="wordcloudHelpText"/>
    </v-card-title>
    <KeywordWordCloudLegend :keywords-word-cloud-legend="keywordsWordCloudLegend"/>
    <KeywordWordCloud :keywords-word-cloud="keywordsWordCloud" :keywords-word-cloud-legend="keywordsWordCloudLegend"/>
  </v-card>
</template>

<script>
import HelpTextTooltip from './HelpTextTooltip.vue'
import KeywordWordCloud from './KeywordWordCloud.vue'
import KeywordWordCloudLegend from './KeywordWordCloudLegend.vue'
export default {
  components: {
    HelpTextTooltip,
    KeywordWordCloud,
    KeywordWordCloudLegend
  },
  props: {
    keywordsWordCloud: {
      type: Array,
      required: true
    },
    keywordsWordCloudLegend: {
      type: Object,
      required: true
    }
  },
  data: () => ({
    wordcloudHelpText: "Observe the most popular keywords associated with the query. In the case where there is no query, the default keywords shown will be related to the top trending topic.",
  })
}
</script>


<style>

</style>

