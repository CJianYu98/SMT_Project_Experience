<template>
  <div id="keywordWordcloud" class="d-flex justify-center mb-6"></div>
</template>

<script>
import * as d3 from "d3"
import * as cloud from 'd3-cloud';

export default {
  props: {
    keywordsWordCloud: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    // layout: {

    // }
  }),
  mounted() {
    // this.generateKeywordsWordcloud();
    this.generateKeywordsWordcloud().update(this.keywordsWordCloud)
    // this.generateKeywordsWordcloud().update(this.keywordsWordCloud)
  },
  methods: {
    generateKeywordsWordcloud() {
      console.log("=== start generateKeywordsWordcloud() ===")
      console.log("this.keywordsWordCloud", this.keywordsWordCloud)

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

      // This function takes the output of 'layout' above and draw the words
      // Wordcloud features that are THE SAME from one word to the other can be here
      // update(this.keywordsWordCloud)
      console.log("bef function draw")

      let layout = {} 

      function draw(words) {
        console.log("=== start draw() ===")
        console.log("words", words)

        const cloud = svg
          .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)

            // cloud.attr("transform", "translate(" + cloud.size()[0] / 2 + "," + cloud.size()[1] / 2 + ")")

            cloud.enter()
              .append("text")
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
              // .attr("transform", "translate(" + cloud.size()[0] / 2 + "," + cloud.size()[1] / 2 + ")")
              .text(function(d) { return d.text; });


            // Exiting words
            cloud.exit()
            .transition()
                .duration(200)
                .style('fill-opacity', 1e-6)
                .attr('font-size', 1)
                .remove();
      }

        // Use the module pattern to encapsulate the visualisation code. We'll
        // expose only the parts that need to be public.
        return {

        // Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        // The outside world will need to call this function, so make it part
        // of the wordCloud return value.

          update(val) {
            console.log("=== start update() ===")
            console.log("words")

            if (d3.select("#keywordWordcloud")._groups[0][0].childNodes.length > 1) {
              d3.select("svg").remove();
            }

            layout = cloud()
              .size([width, height])
              .words(val.map(function(d) { return {text: d.word, size:d.size, sentiment:d.sentiment}; }))
              .padding(5)        // space between words
              .rotate(function() { return ~~(Math.random() * 2) * 90; })
              .fontSize(function(d) { return d.size; })      // font size of words
              .on("end", draw);
            layout.start();
          }
      }
    }
  },
  computed: {
    
  },
  watch: {
    keywordsWordCloud(val) {
      this.generateKeywordsWordcloud().update(val)
    }
  },

}

</script>

<style>
</style>

