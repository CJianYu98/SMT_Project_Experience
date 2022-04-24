<template>
  <v-container fill-height fluid class="px-0">
    <v-row class="d-flex justify-center">
      <span
        class="primary--text body-1 text-center px-1"
      >
        <span :class="`${platformName}--text font-weight-bold`">
          {{ platformName.toUpperCase() }}
        </span>
        <br>
        {{ (platformPercentage * 100).toFixed(0) }}%
      </span>
    </v-row>
  </v-container>
</template>


<script>
export default {
  props: {
    platformPercentage: {
      type: Number,
      required: true,
    },
    platformName: {
      type: String,
      required: true,
    },
  }
}
</script>


<style scoped>

</style>
