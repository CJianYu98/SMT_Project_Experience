<template>
  <div>
    <v-icon
      color="light-green lighten-1"
    >
      mdi-trending-up
    </v-icon>
    <span class="light-green--text"> {{ percentageIncrease * 100 }}% </span>
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

