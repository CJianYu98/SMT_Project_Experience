<template>
  <v-card
    elevation="3"
    class="mx-8 mt-8"
    height="100%"
  >
    <!-- <v-card-title class="pb-4 accent--text">
      Keyword Relational Graph
      <HelpTextTooltip :help-text="keywordAnalysisHelpText"/>
    </v-card-title> -->
    <v-row>
      <v-col>
        <v-card-title class="pb-4 accent--text">
          Keyword Relational Graph
          <HelpTextTooltip :help-text="keywordAnalysisHelpText"/>
        </v-card-title>
        <KeywordRelationalGraph />
      </v-col>
      <v-col>
        <v-card-title class="pb-4 accent--text">
          Related Comments
        </v-card-title>
        <KeywordRelatedComments />
      </v-col>
    </v-row>
  </v-card>
</template>


<script>
import KeywordRelatedComments from './KeywordRelatedComments.vue'
import KeywordRelationalGraph from './KeywordRelationalGraph.vue'
export default {
  components: { 
    KeywordRelationalGraph, 
    KeywordRelatedComments 
  },
  
  data: () => ({
    keywordAnalysisHelpText: "Study the words commonly associated with the selected keyword from the wordcloud. Select another word in the graph to see comments containing both words.",
  }),
}
</script>


<style>

</style>








