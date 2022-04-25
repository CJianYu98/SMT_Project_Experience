<template>
  <div>
    <v-icon
      small
      color="light-green lighten-1"
    >
      mdi-trending-up
    </v-icon>
    <span class="light-green--text"> {{ (percentageIncrease * 100).toFixed(0) }}% </span>
  </div>
</template>

<script>
export default {
  props: { 
    percentageIncrease: {
      type: Number,
      required: true,
    }
  },
}
</script>

<style>

</style>

