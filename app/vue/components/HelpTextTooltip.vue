<template>
  <div class="text-left ml-2 mb-1">
    <v-tooltip top max-width="350px">
      <template v-slot:activator="{ on, attrs }">
        <v-icon
          class="accent--text"
          v-bind="attrs"
          v-on="on"
        >
          mdi-help-circle-outline
        </v-icon>
      </template>
      <span> {{ helpText }} </span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  props: { 
    helpText: {
      type: String,
      required: true,
    }
  },
}
</script>

<style>
  
</style>

