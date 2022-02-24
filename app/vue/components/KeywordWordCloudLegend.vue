<template>
  <div class="d-flex justify-center mb-6">
    <span
      v-for="(colour, sentiment) in keywordsWordCloudLegend"
      :key="sentiment"
      class="px-3"
    >
      <v-icon
        :color="colour"
      >
        mdi-circle
      </v-icon>
      {{ sentiment }}
    </span>
  </div>
</template>

<script>
export default {
  props: {
    keywordsWordCloudLegend: {
      type: Object,
      required: true
    }
  }
}
</script>


<style>

</style>






