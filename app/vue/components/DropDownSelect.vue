<template>
    <div class="d-block">
        <v-select
            d-block
            v-model="viewSelected"
            :items="viewFilter"
            item-text="view"
            label="View"
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
      }
    },
    data: () => ({
      items: [],
    //   viewSelected: "Number of Likes",
    //   viewFilter: [{view: 'Number of Likes'}, {view: 'Number of Comments'}, {view: 'Number of Shares'}]
    }),
  }
</script>