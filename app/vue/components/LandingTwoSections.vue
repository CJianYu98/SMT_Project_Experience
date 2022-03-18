<template>
  <v-container fluid class="header-bg py-4">
    <v-row class="mt-4">
      <v-spacer></v-spacer>
      <v-col cols="4" class="pr-0 pb-0">
        <p class="pb-4 accent--text text-h4">
          {{ componentHeader }}
        </p>
      </v-col>
      <v-col cols="1" class="pl-0 pb-0 mt-n5">
        <v-img
          max-height="70"
          contain
          :src="componentImageOne+`_icon.png`"
          class="ml-auto"
        ></v-img>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
    <v-row class="pb-6">
      <v-spacer></v-spacer>
      <v-col cols="4">
        <p class="pb-4 primary--text text-h5">
          {{ componentDescOne }}
        </p>
        <v-img
          :src="componentImageOne+`.png`" 
          max-height="330"
          contain
        ></v-img>
      </v-col>
      <v-spacer></v-spacer>
      <v-col cols="6">
        <p class="pt-5 pb-5 primary--text text-h5">
          {{ componentDescTwo }}
        </p>
        <v-row>
          <v-col cols="4">
            <v-img
              :src="componentImageTwo+`.jpg`"
              contain
            ></v-img>
              <!-- max-height="300" -->
          </v-col>
          <v-col cols="8">
            <v-img
              :src="componentImageThree+`.jpg`"
              contain
            ></v-img>
              <!-- max-height="300" -->
          </v-col>
        </v-row>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </v-container>
  
</template>

<script>
export default {
  props: {
    componentImageOne: {
      type: String,
      required: true,
    },
    componentImageTwo: {
      type: String,
      required: true,
    },
    componentImageThree: {
      type: String,
      required: true,
    },
    componentHeader: {
      type: String,
      required: true,
    },
    componentDescOne: {
      type: String,
      required: true,
    },
    componentDescTwo: {
      type: String,
      required: true,
    },
  }
}
</script>


<style scoped>
.header-bg {
  background: url("/index_background_dark.png");
  background-size: cover;
  -webkit-transform: scaleX(-1);
  transform: scaleX(-1);
}

/* reverse flipping for other child elements */
.header-bg * {
  -webkit-transform: scaleX(-1);
  transform: scaleX(-1);
}
</style>



