<template>
  <v-card :key="media" class="ml-3 mr-3">
    <v-list-item-subtitle
        class="pl-3 primary--text" 
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
      <v-chip class="mb-2 primary trending-category mr-1">
        {{topic}}
      </v-chip>
    </v-list-item-subtitle>
  </v-card>
</template>

<script>
export default {
  data () {
    return {
      media: 'facebook',
      likes: '65,000',
      date: '21 December 2021',
      comment: 'The dreadful breakthrough infection can effectively be prevented with VCO/Lauric Acid, and total community viral load can be lowered, do not play dice with Covid, try to protect the community and your loved ones at the same time.',
      topic: 'Healthcare',
    }
  }
}
</script>


<style>

</style>

