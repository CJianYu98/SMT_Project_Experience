<template>
  <v-card
    elevation="3"
    class="mr-8 mt-8 rounded-lg"
    height="100%"
  >

    <v-card-title class="pb-4 accent--text text-h6">
      Keyword Relational Graph
      <HelpTextTooltip :help-text="keywordAnalysisHelpText"/>
    </v-card-title>
    
    <v-row>
      <v-col cols="8">
        <KeywordRelationalGraph />
      </v-col>
      <v-col>
        <!-- <KeywordRelatedComments /> -->
      </v-col>
    </v-row>
  </v-card>
</template>


<script>
// import KeywordRelatedComments from './KeywordRelatedComments.vue'
import KeywordRelationalGraph from './KeywordRelationalGraph.vue'
import HelpTextTooltip from './HelpTextTooltip.vue'
export default {
  components: { 
    KeywordRelationalGraph, 
    // KeywordRelatedComments,
    HelpTextTooltip 
  },
  
  data: () => ({
    keywordAnalysisHelpText: "Study the words commonly associated with the selected keyword from the wordcloud. Select another word in the graph to see comments containing both words.",
  }),
}
</script>


<style>

</style>








