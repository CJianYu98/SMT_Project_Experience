<template>
  <v-card :key="media" class="mx-4 mb-4" :href="link" target="_blank">
    <v-list-item-subtitle
        class="px-3 primary--text" 
      >
      <v-row no-gutters align="stretch" class="mt-2">
        &nbsp;
        <v-img 
        max-height="30" 
        max-width="30" 
        :src="`/${media}_icon.png`">
        </v-img>
        &nbsp;&nbsp;
        <p class="mt-1">
          {{likes}}
          likes
        </p>
        <v-spacer></v-spacer>
        <p class="mt-1">
          {{date}}
        </p>
        &nbsp;
      </v-row>
      <p class="text-wrap mt-1">
      {{comment}}
      </p>
      <v-chip-group column>
        <v-chip 
          class="mb-2 primary trending-category mr-1"
          v-for="indvTopic in topic"
          :key="indvTopic"
        >
          {{indvTopic}}
        </v-chip>
      </v-chip-group>
    </v-list-item-subtitle>
  </v-card>
</template>

<script>
export default {
  props: {
    media: {
      type: String,
      required: true
    },
    likes: {
      type: String,
      required: true
    },
    date: {
      type: String,
      required: true
    },
    comment: {
      type: String,
      required: true
    },
    topic: {
      type: Array,
      required: true
    },
    link: {
      type: String,
      required: true
    }
  },
  data: () => ({

  }),
}
</script>


<style>

</style>

