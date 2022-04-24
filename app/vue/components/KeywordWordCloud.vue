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
    // maxWordCount: 0,
  }),
  watch: {
    keywordsWordCloud(val) {
      this.generateKeywordsWordcloud().update(val)
    }
  },
  mounted() {
    // this.generateKeywordsWordcloud();
    this.generateKeywordsWordcloud().update(this.keywordsWordCloud)
    // this.generateKeywordsWordcloud().update(this.keywordsWordCloud)
    // this.getMaxWordCount(this.keywordsWordCloud)
  },
  computed: {
    // maxWordCount() {
    //   return this.keywordsWordCloud.reduce((prev, current) => (parseInt(prev.count) > parseInt(current.count)) ? prev : current, 10).count
    // }
  },
  methods: {
    // getMaxWordCount(wordCloudArr) {
    //   console.log("=== START getMaxWordCount() ===")
    //   console.log("wordCloudArr", wordCloudArr)
    //   const maxFreq = wordCloudArr.reduce((prev, current) => (parseInt(prev.count) > parseInt(current.count)) ? prev : current, 10).count
    //   console.log("maxFreq", maxFreq)
    //   return maxFreq
    // },
    generateKeywordsWordcloud() {
      // console.log("=== start generateKeywordsWordcloud() ===")
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
        // console.log("=== start draw() ===")
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
                return d.sentiment === "positive" ? "#EFB727" : (d.sentiment === "negative" ? "#EB8159" : "#A0D6E8")
                }
              )
              .attr("text-anchor", "middle")
              .style("font-family", "Impact")
              .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
              })
              // .attr("transform", "translate(" + cloud.size()[0] / 2 + "," + cloud.size()[1] / 2 + ")")
              .text(function(d) { return d.text; })
              .on('mouseover', handleMouseOver)
              // .on("mousemove", handleMouseMove)
              .on('mouseout', handleMouseOut);

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

      function handleMouseOver(d) {
        console.log("=== START handleMouseOver() ===")

        console.log("d inside mouseover", d)
        console.log("d.srcElement.__data__.frequency", d.srcElement.__data__.frequency)
        console.log("d.srcElement.__data__.text", d.srcElement.__data__.text)


        // const group = focus.append('g')
        //             .attr('id', d.srcElement.__data__.text.replace(/\'/g, "").replaceAll(' ', ''));
        const group = focus.append('g')
        // eslint-disable-next-line
                    .attr('id', 'id' + d.srcElement.__data__.text.replace(/\'/g, "").replaceAll(' ', ''));
        // console.log("group", group)
        // const base = d.y - d.size;
        // const base = d.y - d.screenY;
        
        // eslint-disable-next-line
        console.log("id test", d.srcElement.__data__.text.replace(/\'/g, "").replaceAll(' ', ''))

        group.selectAll('text')
            .data(d.srcElement.__data__.frequency)
            .enter().append('text')
            .attr('x', d.screenX )
            .attr('y', d.screenY - 200)
            // .attr('y', function(title, i) {
            //   return (base - i*14);
            // })
            .attr('text-anchor', 'middle')
            .attr('fill', '#604AF0')
            .attr('font-weight', 'bolder')
            .text(function() { return 'The keyword "' + d.srcElement.__data__.text + '" has ' + d.srcElement.__data__.frequency + ' mentions'; });

        const bbox = group.node().getBBox();
        const bboxPadding = 5;

        // console.log("group 2", group)
        // console.log("group.node()", group.node())
        // console.log("group.node().getBBox()", group.node().getBBox())

        // place a white background to see text more clearly
        group.insert('rect', ':first-child')
                      .attr('x', bbox.x)
                      .attr('y', bbox.y)
                      .attr('width', bbox.width + bboxPadding)
                      .attr('height', bbox.height + bboxPadding)
                      .attr('rx', 10)
                      .attr('ry', 10)
                      .attr('class', 'label-background-strong');
        
        // console.log("=== END handleMouseOver() ===")
      }

      function handleMouseOut(d) {
        // console.log("=== START handleMouseOut() ===")
        // console.log("d inside mouseout", d)

        // eslint-disable-next-line
        // console.log("d3 select 4", 'id' + d.srcElement.__data__.text.replace(/\'/g, "").replaceAll(' ', ''))

        // eslint-disable-next-line
        d3.select("#id" + d.srcElement.__data__.text.replace(/\'/g, "").replaceAll(' ', '')).remove();

        // console.log("=== END handleMouseOut() ===")
      }

      function getMaxWordCount(wordCloudArr) {
        console.log("=== START getMaxWordCount() ===")
        console.log("wordCloudArr", wordCloudArr)
        const maxFreq = wordCloudArr.reduce((prev, current) => (parseInt(prev.count) > parseInt(current.count)) ? prev : current, 10).count
        console.log("maxFreq", maxFreq)
        return maxFreq
      }

        // Use the module pattern to encapsulate the visualisation code. We'll
        // expose only the parts that need to be public.
        return {

        // Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        // The outside world will need to call this function, so make it part
        // of the wordCloud return value.

          update(val) {
            // console.log("=== start update() ===")
            // console.log("words")

            // console.log("wordcloud length check", d3.select("#keywordWordcloud")._groups[0][0].childNodes.length)

            if (d3.select("#keywordWordcloud")._groups[0][0].childNodes.length > 1) {
              d3.select("#svgId").remove();
            }
            // const computedMaxWordCount = this.maxWordCount
            // console.log("computedMaxWordCount", computedMaxWordCount)

            const methodMaxWordCount = getMaxWordCount(val)
            console.log("methodMaxWordCount", methodMaxWordCount)

            // const methodMaxWordCount = this.getMaxWordCount(val)
            // console.log("methodMaxWordCount", methodMaxWordCount)

            layout = cloud()
              .size([width, height])
              .words(val.map(function(d) { return {text: d.word, size:(d.count/methodMaxWordCount)*150, sentiment:d.sentiment, frequency:d.count.toString()}; }))
              // .words(val.map(function(d) { return {text: d.word, size:d.count, sentiment:d.sentiment, frequency:d.count.toString()}; }))
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

