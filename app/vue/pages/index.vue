<template>
  <v-container fluid align="center">
    <v-row class="header-bg fill-height">
      <v-col cols="5" class="px-3 py-4 d-flex align-center">
        <v-container class="mr-3 ml-5">
          <p class="pb-4 accent--text text-h3">
            {{ header }}
          </p>
          <p class="pb-4 primary--text text-h5">
            {{ headerDesc }}
          </p>
          <v-container class="d-flex justify-center">
            <v-btn to="/dashboard" class="accent text-h6">
              To the Dashboard!
            </v-btn>
          </v-container>
        </v-container>
      </v-col>
      <v-col>
        <v-img
          max-height="500"
          :aspect-ratio="16/9"
          :src="`/landing_page_components.png`"
        ></v-img>
      </v-col>
    </v-row>
    <v-row class="py-4 even-row">
      <v-spacer></v-spacer>
      <v-col cols="4">
        <LandingImageFirst 
          :component-image="filterComponent.componentImage"
          :component-header="filterComponent.componentHeader"
          :component-desc="filterComponent.componentDesc"
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="4">
        <LandingImageLast
          :component-image="keywordComponent.componentImage"
          :component-header="keywordComponent.componentHeader"
          :component-desc="keywordComponent.componentDesc"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>

    <v-row>
      <LandingTwoSections
        :component-image-one="trendingComponent.componentImageOne"
        :component-image-two="trendingComponent.componentImageTwo"
        :component-image-three="trendingComponent.componentImageThree"
        :component-header="trendingComponent.componentHeader"
        :component-desc-one="trendingComponent.componentDescOne"
        :component-desc-two="trendingComponent.componentDescTwo"
      />
    </v-row>


    <v-row class="py-4 even-row">
      <v-spacer></v-spacer>
      <v-col cols="5">
        <LandingImageLast
          :component-image="sentimentComponent.componentImage"
          :component-header="sentimentComponent.componentHeader"
          :component-desc="sentimentComponent.componentDesc"
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="5">
        <LandingImageFirst 
          :component-image="complaintComponent.componentImage"
          :component-header="complaintComponent.componentHeader"
          :component-desc="complaintComponent.componentDesc"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </v-container>
</template>

<script>
import LandingImageFirst from '../components/LandingImageFirst.vue'
import LandingImageLast from '../components/LandingImageLast.vue'
import LandingTwoSections from '../components/LandingTwoSections.vue'
export default {
  components: { 
    LandingImageFirst, 
    LandingImageLast,
    LandingTwoSections 
  },
  name: 'IndexPage',
  data: () => ({
    show: false,
    header: "SOCIAL LISTENING PLATFORM FOR SINGAPOREANS",
    headerDesc: "Gather insights on what Singaporeans have been talking about lately",
    filterComponent: {
      componentImage: 'filters',
      componentHeader: 'FILTERING DATA TO MEET YOUR NEEDS',
      componentDesc: 'Filters include date period, sentiment of posts, data platforms, and emotion of post',
    },
    keywordComponent: {
      componentImage: 'keyword',
      componentHeader: 'ANALYSE BUZZING KEYWORDS',
      componentDesc: 'Analyse buzzing keywords and associated public sentiment',
    },
    // to be updated:
    sentimentComponent: {
      componentImage: 'sentiment',
      componentHeader: 'VIEW ONLINE MOODS AND RELATED TOPICS',
      componentDesc: 'Analyse buzzing keywords and associated public sentiment',
    },
    complaintComponent: {
      componentImage: 'complaints',
      componentHeader: 'LEARN SINGAPOREANS’ COMPLAINTS',
      componentDesc: 'View most common complaints, their related comments and topics associated to the comments',
    },
    trendingComponent: {
      componentImageOne: 'trending',
      componentImageTwo: 'trendingMetrics',
      componentImageThree: 'trendingGraph',
      componentHeader: 'ANALYSE PATTERNS OVER TIME',
      componentDescOne: 'View top topics mentioned, associated top keywords, and sentiment breakdown of topic',
      componentDescTwo: 'Visualise aggregated metrics, and trend in number of posts across time',
    },

  })
}
</script>

<style scoped>
.header-bg {
  background: url("/index_background_dark.png");
  background-size: cover;
  /* opacity: 0.5; */
  /* height: 100vh; */
}

.even-row {
  background: url("/index_background_light.png");
  background-size: cover;
}
</style>