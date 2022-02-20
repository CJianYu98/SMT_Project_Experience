<template>
  <v-card
    elevation="3"
    class="mx-8 mt-8"
  >
    <v-card-title class="pb-4 accent--text">
      Top Keywords
      <HelpTextTooltip :help-text="wordcloudHelpText"/>
    </v-card-title>
    <KeywordWordCloud :keywords-word-cloud="keywordsWordCloud"/>
  </v-card>
</template>

<script>
import HelpTextTooltip from './HelpTextTooltip.vue'
import KeywordWordCloud from './KeywordWordCloud.vue'
export default {
  components: {
    HelpTextTooltip,
    KeywordWordCloud
  },
  props: {
    keywordsWordCloud: {
      type: Array,
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

