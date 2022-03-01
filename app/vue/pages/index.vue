<template>
  <!-- <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
    </v-col>
  </v-row> -->
  <v-container class="mt-n7">
    <v-img
      max-height="300"
      max-width="300"
      :src="`/tls_logo_landing_text.png`"
      class="mx-auto mt-13 mb-n5"
    ></v-img>

    <v-autocomplete
      v-model="autocompleteModel"
      :items="items"
      :loading="isLoading"
      :search-input.sync="search"
      clearable
      hide-details
      hide-selected
      item-text="name"
      item-value="symbol"
      label="Enter a query!"
      solo
      dense
      return-object
    >
    </v-autocomplete>
  </v-container>
</template>

<script>
export default {
  name: 'IndexPage',
}
</script>
