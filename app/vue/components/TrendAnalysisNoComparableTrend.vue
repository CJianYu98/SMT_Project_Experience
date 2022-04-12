<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on, attrs }">
      <span
        v-bind="attrs"
        v-on="on"
        class="primary--text"
      >━</span>
    </template>
    <span>{{ tooltipMsg }}</span>
  </v-tooltip>
</template>

<script>
export default {
  props: {
    tooltipMsg: {
      type: String,
      required: true,
    }
  }
}
</script>

<style>

</style>

