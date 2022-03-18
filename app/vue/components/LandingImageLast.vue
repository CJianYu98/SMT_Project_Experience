<template>
  <v-container fluid>
    <v-row>
      <v-col cols="8" class="pr-0 pb-0">
        <p class="pb-4 accent--text text-h4">
          {{ componentHeader }}
        </p>
      </v-col>
      <v-col class="pl-0 pb-0">
        <v-img
          max-height="70"
          max-width="70"
          contain
          :src="componentImage+`_icon.png`"
        ></v-img>
      </v-col>
    </v-row>
    <p class="pb-4 primary--text text-h5">
      {{ componentDesc }}
    </p>
    <v-img
      max-height="350"
      :src="componentImage+`.jpg`"
      contain
    ></v-img>
  </v-container>
</template>

<script>
export default {
  props: {
    componentImage: {
      type: String,
      required: true,
    },
    componentHeader: {
      type: String,
      required: true,
    },
    componentDesc: {
      type: String,
      required: true,
    },
  }
}
</script>

<style scoped>

</style>

