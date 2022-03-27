<template>
    <div class="d-block pt-4 mr-3">
        <v-select
            d-block
            v-model="selectedView"
            @change="onChange(selectedView)"
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
      selectedView: 'Number of Mentions'
      // items: [],
      // viewSelected: ["Number of Mentions"],
    //   viewFilter: [{view: 'Number of Likes'}, {view: 'Number of Comments'}, {view: 'Number of Shares'}]
    }),
    methods: {
      onChange:function onChange(event){
          // console.log(this.selectedView);
          this.$emit('changeView',this.selectedView);
      }
    }
  }
</script>