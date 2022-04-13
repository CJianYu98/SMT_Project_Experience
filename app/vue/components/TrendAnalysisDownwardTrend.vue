<template>
  <div>
    <v-icon
      small
      color="red lighten-1"
    >
      mdi-trending-down
    </v-icon>
    <span class="red--text"> {{ (percentageDecrease * 100).toFixed(1) }}% </span>
  </div>
</template>

<script>
export default {
  props: { 
    percentageDecrease: {
      type: Number,
      required: true,
    }
  },
}
</script>

<style>

</style>

