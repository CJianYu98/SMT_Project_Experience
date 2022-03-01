<template>
  <v-container align="center" class="mb-6">
    <v-img
      max-height="300"
      max-width="300"
      :src="`/tls_logo_landing_text.png`"
      class="mx-auto mt-13 mb-n5"
    ></v-img>

    <v-row class="justify-center my-7">
      <v-btn to="/dashboard" class="accent" align="center">Bring me to the Dashboard!</v-btn>
    </v-row>

    <v-row class="justify-center my-16">
      <v-icon>mdi-chevron-triple-down</v-icon>
    </v-row>

    <v-row align="stretch">
      <v-col 
        v-for="comp in modules" 
        :key="comp.name"
        cols="4"
      >
        <v-card class="card-container" height="100%">
          <v-img
            :src="`/${comp.imageName}.jpg`"
            height="200px"
          ></v-img>

          <v-card-title>
            {{ comp.name }}
          </v-card-title>

          <v-card-subtitle v-for="desc in comp.description" :key="desc">
            {{ desc }}
          </v-card-subtitle>

        

          <!-- <v-card-actions v-if="comp.additionalDesc">
            <v-btn
              color="orange lighten-2"
              text
            >
              See more
            </v-btn>

            <v-spacer></v-spacer>

            <v-btn
              icon
              @click="show = !show"
            >
              <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </v-card-actions>

          <v-expand-transition v-if="comp.additionalDesc">
            <div v-show="show">
              <v-divider></v-divider>

              <v-card-text>
                {{ comp.additionalDesc }}
              </v-card-text>
            </div>
          </v-expand-transition> -->
        </v-card>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'IndexPage',
  data: () => ({
    show: false,
    modules: [
      {
        imageName: 'filters',
        name: 'Filter Module',
        description: ['Customise data visualised on the dashboard based on date, sentiments, platforms and emotions!'],
        additionalDesc: "Sentiments include negative, neutral and positive. Platforms consist of Facebook, Reddit, Twitter and Youtube. Emotions include Anger, Joy, Fear, Sadness and Neutral.",
      },
      {
        imageName: 'trendAnalysis',
        name: 'Trend Analysis Module',
        description: ['See the top topics mentioned based on the selected filters, and the associated top keywords, along with sentiment breakdown of the topic!', 'Visualise the aggregated social media platform metrics, and the trend in number of posts across time! Gain insights into activities of Singaporeans on social media platforms, and changes in trend.'],
        additionalDesc: "Topics are pre-defined, with a total of 20 possible topics a post can belong to. These topics include arts and entertainment, business and economy, covid19, crime, culture, education, environment, fashion, food, healthcare, law, lifestyle, others, politics, science and medicine, society, sports, technology, transportation and travel.",
      },
      {
        imageName: 'keywordAnalysis',
        name: 'Keyword Analysis Module',
        description: ['See the top keywords associated with the selected filters, along with their sentiments, to find out what Singaporeans have been complaining about lately!'],
        // additionalDesc: "Topics are pre-defined, with a total of 20 possible topics a post can belong to. <br> These topics include arts and entertainment, business and economy, covid19, crime, culture, education, environment, fashion, food, healthcare, law, lifestyle, others, politics, science and medicine, society, sports, technology, transportation and travel.",
      },
      {
        imageName: 'complaints',
        name: "Complaint identification module",
        description: ['See the top complaint keywords associated with the selected filters, and related complaints!'],
      },
      {
        imageName: 'sentiment',
        name: "Online Mood Analysis module",
        description: ['See the sentiments associated with the top topics and top keywords, to know how people are feeling regarding these topics!'],
      }
    ]
  })
}
</script>

<style scoped>
  .card-container {
    margin: 10px;
    padding: 10px;
  }
</style>