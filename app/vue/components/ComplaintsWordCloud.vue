<template>
  <div id="complaintWordcloud" class="d-flex justify-center mb-6"></div>
</template>

<script>
import * as d3 from "d3"
import * as cloud from 'd3-cloud';

export default {
  props: {
    complaintsWordCloud: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    cloudSvgTest: {hey: "test"}
  }),
  computed: {
    
  },
  watch: {
    complaintsWordCloud(val) {
      this.generateKeywordsWordcloud().update(val)
    }
  },
  mounted() {
    // this.generateKeywordsWordcloud();
    this.generateKeywordsWordcloud().update(this.complaintsWordCloud)
    // this.generateKeywordsWordcloud().update(this.keywordsWordCloud)
  },
  methods: {
    generateKeywordsWordcloud() {
      console.log("=== start generateKeywordsWordcloud() ===")
      // console.log("this.complaintsWordCloud", this.complaintsWordCloud)

      // set the dimensions and margins of the graph
      const margin = {top: 10, right: 10, bottom: 10, left: 10}
      const width = 450 - margin.left - margin.right
      const height = 450 - margin.top - margin.bottom

      // append the svg object to the body of the page
      const svg = d3.select("#complaintWordcloud").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id","complaintSvgId")
        
      const focus = svg.append("g")
                    .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

      // This function takes the output of 'layout' above and draw the words
      // Wordcloud features that are THE SAME from one word to the other can be here
      // update(this.keywordsWordCloud)
      // console.log("bef function draw")

      let layout = {} 

      function draw(words) {
        console.log("=== start draw() ===")
        // console.log("words", words)

        const cloudSvg = focus
          .append("g")
          .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
          .selectAll("text")
          .data(words)

            // cloud.attr("transform", "translate(" + cloud.size()[0] / 2 + "," + cloud.size()[1] / 2 + ")")
            // console.log("cloudSvg -1", cloudSvg)
            // console.log("this.cloudSvg 1", this.cloudSvgTest)
            // // this.cloudSvgTest = cloudSvg
            // console.log("this.cloudSvg 2", this.cloudSvgTest)

            cloudSvg.enter()
              .append("text")
              .style("font-size", function(d) { return d.size; })
              .style("fill", "#392A9B"
              )
              .attr("text-anchor", "middle")
              .style("font-family", "Impact")
              .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
              })
              // .attr("transform", "translate(" + cloud.size()[0] / 2 + "," + cloud.size()[1] / 2 + ")")
              .text(function(d) { return d.text; })
              // .on('mouseover', handleMouseOver)
              // .on('mouseout', handleMouseOut);

            // console.log("this.cloudSvg 4", this.cloudSvg)

            // Exiting words
            cloudSvg.exit()
            .transition()
                .duration(200)
                .style('fill-opacity', 1e-6)
                .attr('font-size', 1)
                .remove();

            // console.log("cloudSvg", cloudSvg)
            // console.log("this.cloudSvg 0", this.cloudSvg)
            // this.cloudSvg = cloudSvg
            // console.log("this.cloudSvg 1", this.cloudSvg)
            
      }

      // function handleMouseOver(d) {
      //   console.log("=== START handleMouseOver() ===")
      //   console.log("d", d)
      //   console.log("d.text", d.target.__data__.text)
      //   console.log("this.cloudSvg 3", this.cloudSvg)
      //   const group = this.cloudSvg.append('g')
      //                   .attr('id', 'story-titles');
      //   const base = d.y - d.size;
      //   const hoverText = this.complaintsWordCloud.find(o => o.word === d.target.__data__.text)
      //   console.log("hoverText", hoverText)

      //   group.selectAll('text')
      //       // .data(data['sample_title'][d.key])
      //       .data(hoverText)
      //       .enter().append('text')
      //       .attr('x', d.x)
      //       .attr('y', function(title, i) {
      //         return (base - i*14);
      //       })
      //       .attr('text-anchor', 'middle')
      //       .text(function(title) { return title; });

      //   const bbox = group.node().getBBox();
      //   const bboxPadding = 5;

      //   // place a white background to see text more clearly
      //   // var rect = group.insert('rect', ':first-child')
      //             group.insert('rect', ':first-child')
      //                 .attr('x', bbox.x)
      //                 .attr('y', bbox.y)
      //                 .attr('width', bbox.width + bboxPadding)
      //                 .attr('height', bbox.height + bboxPadding)
      //                 .attr('rx', 10)
      //                 .attr('ry', 10)
      //                 .attr('class', 'label-background-strong');
        
      //   console.log("=== END handleMouseOver() ===")
      // }

      // function handleMouseOut(d) {
      //   console.log("=== START handleMouseOut() ===")
      //   console.log("d", d)
      //   d3.select('#story-titles').remove();
      //   console.log("=== END handleMouseOut() ===")
      // }

        // Use the module pattern to encapsulate the visualisation code. We'll
        // expose only the parts that need to be public.
        return {

        // Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        // The outside world will need to call this function, so make it part
        // of the wordCloud return value.

          update(val) {
            console.log("=== start update() ===")
            // console.log("words")

            if (d3.select("#complaintWordcloud")._groups[0][0].childNodes.length > 1) {
              d3.select("#complaintSvgId").remove();
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
}
</script>


<style>

</style>

