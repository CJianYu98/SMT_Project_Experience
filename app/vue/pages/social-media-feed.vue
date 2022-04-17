<template>
  <div class="mb-10">
    <SearchFilters @changeFilter="rerenderSocialMediaFeed"/>
    <!-- <p> {{ testData }} </p> -->
    <SocialMediaFeedAllPlatformMetrics
      :pending-state="$fetchState.pending"
      :aggregated-stats-all-platforms="aggregatedStatsAllPlatforms"
    />
    <v-row class="my-2">
      <v-spacer></v-spacer>
      <v-col cols="6">
          <!-- :pending-state="$fetchState.pending" -->
        <SocialMediaFeedCard
          :pending-state="$fetchState.pending"
          :platform-all-data="facebook"
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard
          :pending-state="$fetchState.pending"
          :platform-all-data="reddit"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row class="mb-2">
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard
          :pending-state="$fetchState.pending"
          :platform-all-data="twitter"
        />
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <SocialMediaFeedCard
          :pending-state="$fetchState.pending"
          :platform-all-data="youtube"
        />
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
import SocialMediaFeedCard from '../components/SocialMediaFeedCard.vue'
import SocialMediaFeedAllPlatformMetrics from '../components/SocialMediaFeedAllPlatformMetrics.vue'
import SearchFilters from '@/components/SearchFilters'
export default {
  components: { 
    SearchFilters,
    SocialMediaFeedAllPlatformMetrics,
    SocialMediaFeedCard,
  },
  computed: {
  },
  async fetch() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        { 
          "endDate": this.fetchEndDate,
          "numDays": this.fetchNumDays,
          "platforms": this.allPlatforms,
          "sentiments": this.fetchSentiments,
          "emotions": this.fetchEmotions,
          "query": this.fetchQuery,
        }
      )
    };

    const requestOptionsForFacebook = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        { 
          "endDate": this.fetchEndDate,
          "numDays": this.fetchNumDays,
          "platforms": this.facebookRequestStr,
          "sentiments": this.fetchSentiments,
          "emotions": this.fetchEmotions,
          "query": this.fetchQuery,
          "topN": 20
        }
      )
    };

    const requestOptionsForReddit = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        { 
          "endDate": this.fetchEndDate,
          "numDays": this.fetchNumDays,
          "platforms": this.redditRequestStr,
          "sentiments": this.fetchSentiments,
          "emotions": this.fetchEmotions,
          "query": this.fetchQuery,
          "topN": 20
        }
      )
    };

    const requestOptionsForTwitter = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        { 
          "endDate": this.fetchEndDate,
          "numDays": this.fetchNumDays,
          "platforms": this.twitterRequestStr,
          "sentiments": this.fetchSentiments,
          "emotions": this.fetchEmotions,
          "query": this.fetchQuery,
          "topN": 20
        }
      )
    };

    const requestOptionsForYoutube = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        { 
          "endDate": this.fetchEndDate,
          "numDays": this.fetchNumDays,
          "platforms": this.youtubeRequestStr,
          "sentiments": this.fetchSentiments,
          "emotions": this.fetchEmotions,
          "query": this.fetchQuery,
          "topN": 20
        }
      )
    };

    await fetch("http://127.0.0.1:8000/social-media-feed/get-all-aggregated-stats", requestOptions)
      .then(response => response.json())
      .then(data => 
        {

          /*
          { 
            // platform with data
            "facebook": { "mentions": 17772, 
            "sentiment": 
              [ { "sentiment": "positive", "count": 2080, "percentage": "11.7" }, { "sentiment": "neutral", "count": 8356, "percentage": "47.0" }, { "sentiment": "negative", "count": 7336, "percentage": "41.3" } ], 
            "emotions": [ { "emotion": "anger", "count": 80, "percentage": "0.5" }, { "emotion": "fear", "count": 146, "percentage": "0.8" }, { "emotion": "joy", "count": 645, "percentage": "3.6" }, { "emotion": "sadness", "count": 891, "percentage": "5.0" }, { "emotion": "neutral", "count": 16010, "percentage": "90.1" } ] }, 

            // platform with no data
            "twitter": { "mentions": 0, "sentiment": [ { "sentiment": "positive", "count": 0, "percentage": "NaN" }, { "sentiment": "neutral", "count": 0, "percentage": "NaN" }, { "sentiment": "negative", "count": 0, "percentage": "NaN" } ], "emotions": [ { "emotion": "anger", "count": 0, "percentage": "NaN" }, { "emotion": "fear", "count": 0, "percentage": "NaN" }, { "emotion": "joy", "count": 0, "percentage": "NaN" }, { "emotion": "sadness", "count": 0, "percentage": "NaN" }, { "emotion": "neutral", "count": 0, "percentage": "NaN" } ] }, 
          }
           */

          console.log("social-media-feed get-all-aggregated-stats data", data)
          // this.testData = data

          this.aggregatedStatsAllPlatforms = data
        }
      )
      // .catch((error) => {
      //   console.error(error)
      // })

    await fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-posts", requestOptionsForFacebook)
    .then(response => response.json())
      .then(data => 
        {
          // no data
          // { "twitter": { "likes": [], "date": [] } }

          // this.testData = data

          console.log("social-media-feed facebook data", data)

          // getting sum of posts in dictionary
          const numFacebookPosts = this.getNumPostsTotal(this.numFacebookPostsTotal, data)
          
          if (numFacebookPosts === 0) {
            this.facebook = {facebook: {}}
          } else {
            this.facebook = data
          }
          
          this.numFacebookPostsTotal = 0
        }
      )
    //   .catch((error) => {
    //     console.error(error);
    //   })

    await fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-posts", requestOptionsForReddit)
    .then(response => response.json())
      .then(data => 
        {
          // no data
          // { "twitter": { "likes": [], "date": [] } }

          // this.testData = data

          console.log("social-media-feed reddit data", data)

          // getting sum of posts in dictionary
          const numRedditPosts = this.getNumPostsTotal(this.numRedditPostsTotal, data)
          
          if (numRedditPosts === 0) {
            this.reddit = {reddit: {}}
          } else {
            this.reddit = data
          }
          
          this.numRedditPostsTotal = 0
        }
      )
    //   .catch((error) => {
    //     console.error(error);
    //   })

    await fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-posts", requestOptionsForYoutube)
    .then(response => response.json())
      .then(data => 
        {
          // no data
          // { "twitter": { "likes": [], "date": [] } }

          // this.testData = data

          console.log("social-media-feed youtube data", data)

          // getting sum of posts in dictionary
          const numYoutubePosts = this.getNumPostsTotal(this.numYoutubePostsTotal, data)
          
          if (numYoutubePosts === 0) {
            this.youtube = {youtube: {}}
          } else {
            this.youtube = data
          }
          
          this.numYoutubePostsTotal = 0
        }
      )
    //   .catch((error) => {
    //     console.error(error);
    //   })

    await fetch("http://127.0.0.1:8000/noteworthy-analysis/get-all-top5-noteworthy-posts", requestOptionsForTwitter)
    .then(response => response.json())
      .then(data => 
        {
          // no data
          // { "twitter": { "likes": [], "date": [] } }

          // this.testData = data

          console.log("social-media-feed twitter data", data)

          // getting sum of posts in dictionary
          const numTwitterPosts = this.getNumPostsTotal(this.numTwitterPostsTotal, data)
          
          if (numTwitterPosts === 0) {
            this.twitter = {twitter: {}}
          } else {
            this.twitter = data
          }
          
          this.numTwitterPostsTotal = 0
        }
      )
    //   .catch((error) => {
    //     console.error(error);
    //   })


  },
  data: () => ({
    aggregatedStatsAllPlatforms: {},
    testData: "",
    fetchQuery: null,
    fetchEndDate: "2021-04-06",
    fetchNumDays: 14,
    fetchSentiments: ["neutral", "negative", "positive"],
    fetchEmotions: ["neutral", "anger", "fear", "sadness", "joy"],
    allPlatforms: ["facebook", "reddit", "twitter", "youtube"],
    twitterRequestStr: ["twitter"],
    facebookRequestStr: ["facebook"],
    redditRequestStr: ["reddit"],
    youtubeRequestStr: ["youtube"],
    facebook: {},
    reddit: {},
    twitter: {},
    youtube: {},
    numFacebookPostsTotal: 0,
    numRedditPostsTotal: 0,
    numTwitterPostsTotal: 0,
    numYoutubePostsTotal: 0,
  }),
  methods: {
    getNumPostsTotal(baseCount, data) {
      // console.log("baseCount", baseCount)
      // console.log("data", data)
      for (const platform in data) {
        // console.log("platform", platform)
        for (const metric in data[platform]) {
          // console.log("metric", metric)
          baseCount += data[platform][metric].length
          // console.log("this.numComplaintPostsTotal", baseCount)
        }
      }
      return baseCount
    },
    rerenderSocialMediaFeed(updatedSentiments) {
      // console.log("=== START rerenderSocialMediaFeed ===")
      // console.log("rerenderSocialMeduaFeed updatedSentiments", updatedSentiments)

      this.fetchQuery = updatedSentiments[0]
      this.fetchEndDate = updatedSentiments[1]
      this.fetchNumDays = updatedSentiments[2]
      this.fetchSentiments = updatedSentiments[3]
      this.fetchEmotions = updatedSentiments[4]
      this.dateFilter = updatedSentiments[5]

      // console.log("this.fetchQuery", this.fetchQuery)
      // console.log("this.fetchEndDate", this.fetchEndDate)
      // console.log("this.fetchNumDays", this.fetchNumDays)
      // console.log("this.fetchSentiments", this.fetchSentiments)
      // console.log("this.fetchEmotions", this.fetchEmotions)

      this.$fetch()

      // console.log("=== END rerenderSocialMediaFeed ===")
    },
  },

}
</script>


<style>

</style>
