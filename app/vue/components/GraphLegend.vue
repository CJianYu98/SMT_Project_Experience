<template>
  <div class="mb-3 mt-3">
    <v-row>
      <p class="d-flex justify-center mb-0 primary--text font-weight-bold">
        {{ type }}
      </p>
    </v-row> 
    <v-row>
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
    </v-row>
  </div>
</template>

<script>
export default {
  props: {
    graphLegend: {
      type: Object,
      required: true
    },
    type: {
      type: String,
      required: true
    }
  }
}
</script>


<style scoped>
div
{
    display : block;
}
</style>






