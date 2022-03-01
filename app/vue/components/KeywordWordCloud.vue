<template>
  <div id="keywordWordcloud" class="d-flex justify-center my-n3"></div>
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
    // cloudSvgTest: {testKey: "testValue"}
  }),
  computed: {
    
  },
  watch: {
    keywordsWordCloud(val) {
      this.generateKeywordsWordcloud().update(val)
    }
  },
  mounted() {
    // this.generateKeywordsWordcloud();
    this.generateKeywordsWordcloud().update(this.keywordsWordCloud)
    // this.generateKeywordsWordcloud().update(this.keywordsWordCloud)
  },
  methods: {
    generateKeywordsWordcloud() {
      console.log("=== start generateKeywordsWordcloud() ===")
      // console.log("this.keywordsWordCloud", this.keywordsWordCloud)

      // set the dimensions and margins of the graph
      const margin = {top: 10, right: 10, bottom: 10, left: 10}
      const width = 450 - margin.left - margin.right
      const height = 450 - margin.top - margin.bottom

      // append the svg object to the body of the page
      const svg = d3.select("#keywordWordcloud").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .attr("id","svgId")

      const focus = svg.append("g")
                    .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

      // This function takes the output of 'layout' above and draw the words
      // Wordcloud features that are THE SAME from one word to the other can be here
      // update(this.keywordsWordCloud)
      // console.log("bef function draw")

      let layout = {}
      // const self = this // for getting keywords in tooltip

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
            // this.cloudSvgTest = cloudSvg
            // console.log("this.cloudSvg 2", this.cloudSvgTest)

            cloudSvg.enter()
              .append("text")
              .style("font-size", function(d) { return d.size; })
              .style("fill", function(d) { 
                // console.log("d.sentiment", d.sentiment) 
                return d.sentiment === "positive" ? "#78D549" : (d.sentiment === "negative" ? "#EB8159" : "#EFB727")
                }
              )
              .attr("text-anchor", "middle")
              .style("font-family", "Impact")
              .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
              })
              // .attr("transform", "translate(" + cloud.size()[0] / 2 + "," + cloud.size()[1] / 2 + ")")
              .text(function(d) { return d.text; })
              // .on('mouseover', handleMouseOver)
              // .on("mousemove", handleMouseMove)
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


      // creating tooltip

      // const tooltip = d3.select("#keywordWordcloud")
      //   .append("div")
      //   .style("display", "inline")
      //   .style("opacity", 0)
      //   .attr("class", "tooltip")
      //   .style("background-color", "white")
      //   .style("border", "solid")
      //   .style("border-width", "1px")
      //   .style("border-radius", "5px")
      //   .style("padding", "10px")

      // function handleMouseOver(d) {
      //   console.log("=== START handleMouseOver() ===")
      //   // const subgroupName = d3.select(this.parentNode).datum().key;
      //   // const subgroupValue = d.data[subgroupName];
      //   // tooltip
      //   //     .html("subgroup: " + subgroupName + "<br>" + "Value: " + subgroupValue)
      //   //     .style("opacity", 1)

      //   const wordCount = self.keywordsWordCloud.find(x => x.word === d.target.__data__.text).hover
      //   console.log("wordCount", wordCount)
      //   tooltip
      //     .html(wordCount)
      //     .attr('x', d.x)
      //     .style("opacity", 1)

      //   d3.select(this)
      //   .style("stroke", "black")
      //   .style("opacity", 1)

        

      //   console.log("d", d)
      //   console.log("d.text", d.target.__data__.text)
      //   // console.log("this.cloudSvg 3", this.cloudSvg)
      //   // console.log("focus", focus)
      //   console.log("self.keywordsWordCloud", self.keywordsWordCloud)

      //   // const group = focus.append('g')
      //   //                 .attr('id', 'story-titles');
      //   // const base = d.y - d.screenY;
      //   // // console.log("base 1", base)
        
      //   // const hoverText = self.keywordsWordCloud.find(o => o.word === d.target.__data__.text).hover
      //   // // console.log("hoverText", hoverText)

      //   // group.selectAll('text')
      //   //     // .data(data['sample_title'][d.key])
      //   //     .data(hoverText)
      //   //     .enter().append('text')
      //   //     .attr('x', d.x)
      //   //     .attr('y', function(title, i) {
      //   //       console.log("i", i)
      //   //       console.log("base 2", this.base)
      //   //       console.log("base - i*14", base - i*14)
      //   //       return (base - i*14);
      //   //     })
      //   //     .attr('text-anchor', 'middle')
      //   //     .text(function(title) { return title; });

      //   // const bbox = group.node().getBBox();
      //   // const bboxPadding = 5;

      //   // // console.log("bbox", bbox)
      //   // // console.log("bboxPadding", bboxPadding)

      //   // // place a white background to see text more clearly
      //   // // var rect = group.insert('rect', ':first-child')
      //   // group.insert('rect', ':first-child')
      //   //     .attr('x', bbox.x)
      //   //     .attr('y', bbox.y)
      //   //     .attr('width', bbox.width + bboxPadding)
      //   //     // .attr('height', bbox.height + bboxPadding)
      //   //     .attr('height', 30)
      //   //     .attr('rx', 10)
      //   //     .attr('ry', 10)
      //   //     .attr('class', 'label-background-strong');
        
      //   console.log("=== END handleMouseOver() ===")
      // }

      // function handleMouseMove(d) {
      //   // tooltip
      //     // .style("left", (d3.pointer(this)[0]+90) + "px") // It is important to put the +90: other wise the tooltip is exactly where the point is an it creates a weird effect
      //     // .style("top", (d3.pointer(this)[1]) + "px")

      //     const wordCount = self.keywordsWordCloud.find(x => x.word === d.target.__data__.text).hover

      //     tooltip
      //       .html("The exact value of<br>this cell is: " + wordCount)
      //       .style("left", (d3.pointer(this)[0]+20) + "px")
      //       .style("top", (d3.pointer(this)[1]) + "px")
      // }

      // function handleMouseOut() {
      //   console.log("=== START handleMouseOut() ===")
      //   // console.log("d", d)
      //   // d3.select('#story-titles').remove();
      //   tooltip
      //     .style("opacity", 0)
      //   d3.select(this)
      //     .style("stroke", "none")
      //     .style("opacity", 0.8)
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

            console.log("wordcloud length check", d3.select("#keywordWordcloud")._groups[0][0].childNodes.length)

            if (d3.select("#keywordWordcloud")._groups[0][0].childNodes.length > 1) {
              d3.select("#svgId").remove();
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
.label-background-strong {
  fill: white;
  fill-opacity: .8;
}
</style>

