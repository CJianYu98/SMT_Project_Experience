// const sampleData = [
//   { label: 'Test 0 which should not render', value: 0 },
//   { label: 'Group-1', value: 55 },
//   { label: 'Group-2', value: 233 },
//   { label: 'Test 0 AGAIN which should not render', value: 0 },
//   { label: 'Group-3', value: 89 }
// ]

// export default sampleData

// // under groupData
// // group data for chart and filter out zero values
// const d3 = window.d3

// export default function (data, total) {
//   // use scale to get percent values
//   const percent = d3.scaleLinear()
//     .domain([0, total])
//     .range([0, 100])
//   // filter out data that has zero values
//   // also get mapping for next placement
//   // (save having to format data for d3 stack)
//   let cumulative = 0
//   const _data = data.map(d => {
//     cumulative += d.value
//     return {
//       value: d.value,
//       // want the cumulative to prior value (start of rect)
//       cumulative: cumulative - d.value,
//       label: d.label,
//       percent: percent(d.value)
//     }
//   }).filter(d => d.value > 0)
//   return _data
// }


// import sampleData from './sampleData'
// import groupData from './groupData'
// const d3 = window.d3

// function stackedBar (bind, data, config) {
//   config = {
//     f: d3.format('.1f'),
//     margin: {top: 20, right: 10, bottom: 20, left: 10},
//     width: 800,
//     height: 200,
//     barHeight: 100,
//     colors: ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33'],
//     ...config
//   }
//   const { f, margin, width, height, barHeight, colors } = config
//   const w = width - margin.left - margin.right
//   const h = height - margin.top - margin.bottom
//   const halfBarHeight = barHeight / 2

//   const total = d3.sum(data, d => d.value)
//   const _data = groupData(data, total)

//   // set up scales for horizontal placement
//   const xScale = d3.scaleLinear()
//     .domain([0, total])
//     .range([0, w])

//   // create svg in passed in div
//   const selection = d3.select(bind)
//     .append('svg')
//     .attr('width', width)
//     .attr('height', height)
//     .append('g')
//     .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

//   // stack rect for each data value
//   selection.selectAll('rect')
//     .data(_data)
//     .enter().append('rect')
//     .attr('class', 'rect-stacked')
//     .attr('x', d => xScale(d.cumulative))
//     .attr('y', h / 2 - halfBarHeight)
//     .attr('height', barHeight)
//     .attr('width', d => xScale(d.value))
//     .style('fill', (d, i) => colors[i])

//   // add values on bar
//   selection.selectAll('.text-value')
//     .data(_data)
//     .enter().append('text')
//     .attr('class', 'text-value')
//     .attr('text-anchor', 'middle')
//     .attr('x', d => xScale(d.cumulative) + (xScale(d.value) / 2))
//     .attr('y', (h / 2) + 5)
//     .text(d => d.value)

//   // add some labels for percentages
//   selection.selectAll('.text-percent')
//     .data(_data)
//     .enter().append('text')
//     .attr('class', 'text-percent')
//     .attr('text-anchor', 'middle')
//     .attr('x', d => xScale(d.cumulative) + (xScale(d.value) / 2))
//     .attr('y', (h / 2) - (halfBarHeight * 1.1))
//     .text(d => f(d.percent) + ' %')

//   // add the labels
//   selection.selectAll('.text-label')
//     .data(_data)
//     .enter().append('text')
//     .attr('class', 'text-label')
//     .attr('text-anchor', 'middle')
//     .attr('x', d => xScale(d.cumulative) + (xScale(d.value) / 2))
//     .attr('y', (h / 2) + (halfBarHeight * 1.1) + 20)
//     .style('fill', (d, i) => colors[i])
//     .text(d => d.label)
// }
// // render chart
// stackedBar('.chart', sampleData)