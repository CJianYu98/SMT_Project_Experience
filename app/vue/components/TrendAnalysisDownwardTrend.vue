<template>
  <div>
    <v-icon
      color="red lighten-1"
    >
      mdi-trending-down
    </v-icon>
    <span class="red--text"> {{ percentageDecrease * 100 }}% </span>
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

