<template>
  <div class="d-flex justify-center mb-2">
    <span
      v-for="(colour, key) in graphLegend"
      :key="key"
      class="primary--text body-1 text-center px-1"
    >
      <v-icon
        :color="colour"
        small
      >
        mdi-circle
      </v-icon>
      <br>
      {{ key }}
    </span>
  </div>
</template>

<script>
export default {
  props: {
    graphLegend: {
      type: Object,
      required: true
    }
  }
}
</script>


<style>

</style>






