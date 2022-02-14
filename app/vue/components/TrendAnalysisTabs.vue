<template>
  <!-- <v-card>
    <v-tabs
      background-color="deep-purple"
      center-active
      dark
    >
      <v-tab><v-img src="facebook_icon.png"></v-img>Facebook</v-tab>
      <v-tab><v-img src="instagram_icon.png"></v-img>Instagram</v-tab>
      <v-tab><v-img src="reddit_icon.png"></v-img>Reddit</v-tab>
      <v-tab><v-img src="twitter_icon.png"></v-img>Twitter</v-tab>
      <v-tab><v-img src="youtube_icon.png"></v-img>Youtube</v-tab>
    </v-tabs>
  </v-card> -->

  <v-card>
    <v-tabs
        v-model="tabs"
        centered
    >
        <v-tab
            v-for="item in items"
            :key="item"
        >
            <v-img :src="`/${item}_icon.png`">
            </v-img>
            &nbsp;
            {{ item }}
        </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tabs">
      <v-tab-item>
        <v-card flat>
          <v-card-title class="text-h5">
            Number of Posts
          </v-card-title>
          <v-img
            :aspect-ratio="2.8"
            :width="width"
            src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-title class="text-h5">
            Number of Posts
          </v-card-title>
          <v-img
            :aspect-ratio="2.8"
            :width="width"
            src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-title class="text-h5">
            Number of Posts
          </v-card-title>
          <v-img
            :aspect-ratio="2.8"
            :width="width"
            src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-title class="text-h5">
            Number of Retweets
          </v-card-title>
          <v-img
            :aspect-ratio="2.8"
            :width="width"
            src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-title class="text-h5">
            Number of Comments
          </v-card-title>
          <v-img
            :aspect-ratio="2.8"
            :width="width"
            src="https://cdn.vuetifyjs.com/images/parallax/material.jpg"
            ></v-img>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>

</template>

<script>
  export default {
    components: {
        
    },
    data () {
      return {
        tabs: null,
        items: ['facebook','instagram','reddit','twitter','youtube'],
      }
    },
  }
</script>