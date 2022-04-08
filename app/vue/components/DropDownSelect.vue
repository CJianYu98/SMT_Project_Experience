<template>
    <div class="d-block pt-4 mr-3">
        <v-select
            d-block
            v-model="selectedView"
            @change="onChange()"
            :items="viewFilter"
            item-text="view"
            :label="label"
            outlined
            dense
        >
          <template #selection="{ item }">
            <span class="accent--text">{{ item }}</span>
          </template>
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
      viewSelected: {
        required: true
      },
    },
    data: (instance) => {
      return {
        selectedView: instance.viewSelected,
        // items: [],
        // viewSelected: ["Number of Mentions"],
        // viewFilter: [{view: 'Number of Likes'}, {view: 'Number of Comments'}, {view: 'Number of Shares'}]
      }
    },
    methods: {
      onChange:function onChange(){
          console.log("=== start onChange() ===")
          // console.log(this.selectedView);
          this.$emit('changeView',this.selectedView);
          console.log("=== end onChange() ===")
      }
    },
    watch:{
      viewSelected() {
        console.log("=== start viewSelected() watch ===")
        console.log("this.viewSelected", this.viewSelected)
        this.selectedView = this.viewSelected;
        console.log("=== end viewSelected() watch ===")
      }
    }
  }
</script>