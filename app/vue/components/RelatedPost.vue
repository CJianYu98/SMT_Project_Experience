<template>
  <v-card 
    :href="link" target="_blank"
    :key="media" 
    class="mx-4 mb-4" 
    :style="`border: 1px primary solid;`"
    >
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
          {{formatedDate}}
        </p>
        &nbsp;
      </v-row>
      <!-- :href="link" target="_blank" -->
      <p class="text-wrap mt-1" >
        {{comment}}
      </p>
      <v-chip-group column>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-img
              max-height="30"
              max-width="30"
              :src="`/${sentiment}_sentiment.png`"
              :alt="`${sentiment} icon`"
              class="mt-1 mr-2"
              v-bind="attrs"
              v-on="on"
            ></v-img>
          </template>
          <span>{{sentiment}} sentiment</span>
        </v-tooltip>

        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-img
              max-height="30"
              max-width="30"
              :src="`/${emotion}.png`"
              :alt="`${emotion} icon`"
              class="mt-1 mr-2"
              v-bind="attrs"
              v-on="on"
            ></v-img>
          </template>
          <span>{{emotion}} </span>
        </v-tooltip>
        <template v-if="intent">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip 
                class="mb-2 mr-1 intent intent--text"
                outlined
                v-bind="attrs"
                v-on="on"
              >
                {{intent}}
              </v-chip>
            </template>
            <span> intent tag of comment </span>
          </v-tooltip>
        </template>
        <v-chip 
          class="mb-2 primary mr-1"
          v-for="indvTopic in topic"
          :key="indvTopic"
        >
          {{indvTopic}}
        </v-chip>
          <!-- class="mx-auto" -->
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
    sentiment: {
      type: String,
      required: true
    },
    emotion: {
      type: String,
      required: true
    },
    link: {
      type: String,
      required: true
    },
    img: {
      type: String,
      required: false
    },
    intent: {
      type: String,
      required: false
    },
  },
  data: () => ({

  }),
  computed: {
    formatedDate() {
      console.log("=== start formatedDate() ===")
      const [year, month, date] = String(this.date).split('T')[0].split('-')
      return `${date}/${month}/${year}`
    }
  }
}
</script>


<style>

</style>

