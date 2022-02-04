<template>
  <v-card
    elevation="3"
    class="mx-8 mt-8"
  >
    <v-card-title>Trending Topics</v-card-title>
  
  </v-card>
</template>

<script>
export default {
  top5topics: [
    {
    topic: 'GE2020', 
    mentions: 294940, 
    sentiment: {
      negative: 0.2, neutral: 0.6, positive: 0.2
      }
    },
    {
    topic: 'GE2024', 
    mentions: 29494, 
    sentiment: {
      negative: 0.2, neutral: 0.6, positive: 0.2
      }
    }
  ]
}
</script>


<style>

</style>
