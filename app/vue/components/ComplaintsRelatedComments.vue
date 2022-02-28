<template>
  <div>
    <v-row no-gutters align="stretch">
      &nbsp; &nbsp; 
      <DropDownSelect 
      v-bind:viewFilter="sortView" v-bind:label="label" v-bind:viewSelected="viewSelected">
      </DropDownSelect>
    </v-row>
    <ComplaintsRelatedComment/>
    &nbsp;
    <ComplaintsRelatedComment/>
  </div>
</template>

<script>
import DropDownSelect from "./DropDownSelect.vue"
import ComplaintsRelatedComment from './ComplaintsRelatedComment.vue'

export default {
  components: {
    DropDownSelect, 
    ComplaintsRelatedComment 
  },
  data: () => ({
      sortView: [{view: 'Likes'}, {view: 'Date'}],
      label: 'Sort By',
      // viewSelected: 'Likes',
  }),
}
</script>


<style>

</style>

