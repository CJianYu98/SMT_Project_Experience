<template>
  <v-container fluid class="px-0 py-0">
    <v-img
          max-height="40"
          contain
          :src="`/${platform.name}_icon.png`"
          :alt="`${platform.name} icon`"
          class="mx-auto"
        ></v-img>
        <p class="mb-1 accent--text text-h6 text-center">
          {{ platform.name.toUpperCase() }}
        </p>
        <p class="mb-0 primary--text text-h5 text-center">
          {{ platform.statistics.toLocaleString() }}
        </p>
        <p class="accent--text text-h7 text-center">
          {{ platform.description }}
        </p>
  </v-container>
</template>


<script>
export default {
  props: {
    platform: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    aggregatedStatsHelpText: "These aggregated statistics are based on the filters that are selected.",
  })
}
</script>


<style scoped>

</style>




