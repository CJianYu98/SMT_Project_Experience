<template>
    <div class="d-block pt-4 mr-3">
        <v-select
            d-block
            :v-model="viewSelected"
            :items="viewFilter"
            item-text="view"
            :label="label"
            outlined
            dense
        >
        </v-select>
    </div>
</template>

<script>
  export default {
    props:{
      viewFilter:{
        required: true
      },
      label: {
        required: true
      },
      // viewSelected: {
      //   required: true
      // }
    },
    data: () => ({
      items: [],
    //   viewSelected: "Number of Likes",
    //   viewFilter: [{view: 'Number of Likes'}, {view: 'Number of Comments'}, {view: 'Number of Shares'}]
    }),
  }
</script>