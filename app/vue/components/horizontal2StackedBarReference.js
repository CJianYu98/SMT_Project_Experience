// chart = {
//   const svg = d3.create("svg")
//       .attr("viewBox", [0, 0, width, height])
//       .style("display", "block");

//   svg.append("g")
//       .attr("stroke", "white")
//     .selectAll("rect")
//     .data(stack)
//     .join("rect")
//       .attr("fill", d => color(d.name))
//       .attr("x", d => x(d.startValue))
//       .attr("y", margin.top)
//       .attr("width", d => x(d.endValue) - x(d.startValue))
//       .attr("height", height-margin.top-margin.bottom)
//     .append("title")
//       .text(d => `${d.name}
// ${formatPercent(d.value)}`);

//   svg.append("g")
//       .attr("font-family", "sans-serif")
//       .attr("font-size", 12)
//     .selectAll("text")
//     .data(stack.filter(d => x(d.endValue) - x(d.startValue) > 40))
//     .join("text")
//       .attr("fill", d => d3.lab(color(d.name)).l < 50 ? "white" : "black")
//       .attr("transform", d => `translate(${x(d.startValue) + 6}, 6)`)
//       .call(text => text.append("tspan")
//           .attr("y", "0.7em")
//           .attr("font-weight", "bold")
//           .text(d => d.name))
//       .call(text => text.append("tspan")
//           .attr("x", 0)
//           .attr("y", "1.7em")
//           .attr("fill-opacity", 0.7)
//           .text(d => formatPercent(d.value)));

//   return svg.node();
// }

// data = d3.csvParse(await FileAttachment("population-by-age.csv").text(), d3.autoType)

// stack = {
//   const total = d3.sum(data, d => d.value);
//   let value = 0;
//   return data.map(d => ({
//     name: d.name,
//     value: d.value / total, // percentage
//     startValue: value / total, 
//     endValue: (value += d.value) / total
//   }));
// }

// color = d3.scaleOrdinal()
//     .domain(data.map(d => d.name))
//     .range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), data.length).reverse())

// x = d3.scaleLinear([0, 1], [margin.left, width - margin.right])

// formatPercent = x.tickFormat(null, "%")

// height = 33

// margin = ({top: 0, right: 0, bottom: 0, left: 0})

// d3 = require("d3@6")






