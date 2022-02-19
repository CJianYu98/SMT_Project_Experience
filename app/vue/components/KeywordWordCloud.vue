<template>
  <div id="keywordWordcloud"></div>
  <!-- <div>
    {{ keywordsWordCloud }}
  </div> -->
</template>

<script>
import * as d3 from "d3"
import * as cloud from 'd3-cloud';

export default {
  components: {

    },
  props: {
    keywordsWordCloud: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    // keywords: [
    //   {word: "Running", size: "10", sentiment: "positive"}, 
    //   {word: "Surfing", size: "20", sentiment: "neutral"}, 
    //   {word: "Climbing", size: "50", sentiment: "negative"}, 
    //   {word: "Kiting", size: "30", sentiment: "positive"}, 
    //   {word: "Sailing", size: "20", sentiment: "negative"}, 
    //   {word: "Snowboarding", size: "60", sentiment: "neutral"} 
    // ]
  }),
  mounted() {
    this.generateKeywordsWordcloud();
  },
  methods: {
    generateKeywordsWordcloud() {
      // set the dimensions and margins of the graph
      const margin = {top: 10, right: 10, bottom: 10, left: 10}
      const width = 450 - margin.left - margin.right
      const height = 450 - margin.top - margin.bottom

      // append the svg object to the body of the page
      const svg = d3.select("#keywordWordcloud").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

      // Constructs a new cloud layout instance. It run an algorithm to find the position of words that suits your requirements
      // Wordcloud features that are different from one word to the other must be here
      const layout = cloud()
        .size([width, height])
        .words(this.keywordsWordCloud.map(function(d) { return {text: d.word, size:d.size, sentiment:d.sentiment}; }))
        .padding(5)        // space between words
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .fontSize(function(d) { return d.size; })      // font size of words
        .on("end", draw);
      layout.start();

      // This function takes the output of 'layout' above and draw the words
      // Wordcloud features that are THE SAME from one word to the other can be here
      function draw(words) {
        svg
          .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
              .style("font-size", function(d) { return d.size; })
              .style("fill", function(d) { 
                console.log("d.sentiment", d.sentiment) 
                return d.sentiment === "positive" ? "#78D549" : (d.sentiment === "negative" ? "#EB8159" : "#EFB727")
                }
              )
              .attr("text-anchor", "middle")
              .style("font-family", "Impact")
              .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
              })
              .text(function(d) { return d.text; });
      }
    }
  }

}
</script>


<style>

</style>

