<template>
  <v-row no-gutters align="stretch">
    <DropDownSelect v-bind:viewFilter="sortView"></DropDownSelect>
  </v-row>
</template>


<script>
import DropDownSelect from "./DropDownSelect.vue"
export default {
  components: {
    DropDownSelect,
  },
  data: () => ({
      sortView: [{view: 'Likes'}, {view: 'Comments'}],
  }),
}
</script>


<style>

</style>








