<template>
  <!-- <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
    </v-col>
  </v-row> -->
  <v-container class="mt-n7">
    <v-img
      max-height="300"
      max-width="300"
      :src="`/tls_logo_landing_text.png`"
      class="mx-auto mt-13 mb-n5"
    ></v-img>

    <v-card
      class="mx-auto"
      max-width="344"
    >
      <v-img
        src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
        height="200px"
      ></v-img>

      <v-card-title>
        Top western road trips
      </v-card-title>

      <v-card-subtitle>
        1,000 miles of wonder
      </v-card-subtitle>

      <v-card-actions>
        <v-btn
          color="orange lighten-2"
          text
        >
          Explore
        </v-btn>

        <v-spacer></v-spacer>

        <v-btn
          icon
          @click="show = !show"
        >
          <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-btn>
      </v-card-actions>

      <v-expand-transition>
        <div v-show="show">
          <v-divider></v-divider>

          <v-card-text>
            I'm a thing. But, like most politicians, he promised more than he could deliver. You won't have time for sleeping, soldier, not with all the bed making you'll be doing. Then we'll go with that data file! Hey, you add a one and two zeros to that or we walk! You're going to do his laundry? I've got to find a way to escape.
          </v-card-text>
        </div>
      </v-expand-transition>
    </v-card>

  </v-container>
</template>

<script>
export default {
  name: 'IndexPage',
  modules: {
    filters: {
      description: 'Filters'
    }
  }
}
</script>
