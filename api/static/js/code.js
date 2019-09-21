initialize = function(elements) {
    var cy = cytoscape({
      container: document.getElementById('cy'),

      boxSelectionEnabled: false,
      autounselectify: true,

      style: cytoscape.stylesheet()
        .selector('node')
        .style({
          'content': 'data(id)'
        })
        .selector('.highlighted-node')
        .style({
          'content': 'data(id)',
          'background-color': '#61bffc',
        })
      .selector('edge')
          .style({
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'width': 4,
            'line-color': '#ddd',
            'target-arrow-color': '#ddd'
          })
        .selector('.highlighted')
          .style({
            'background-color': '#61bffc',
            'line-color': '#61bffc',
            'target-arrow-color': '#61bffc',
            'transition-property': 'background-color, line-color, target-arrow-color',
            'transition-duration': '0.5s'
          })

          .selector('.highlighted-red')
              .style({
                'background-color': '#FF0000',
                'line-color': '#FF0000',
                'target-arrow-color': '#FF0000',
                'transition-property': 'background-color, line-color, target-arrow-color',
                'transition-duration': '0.5s'
          }),

      elements: elements,

      layout: {
        name: 'breadthfirst',
        directed: true,
        roots: '#a',
        padding: 5
      }
    });
}



// Highlight an edge (highlights target nodes and un-highlights source nodes)
function highlightEdge(id, color) {
  let edge = cy.edges().filter(x => x.data('id') == id)
  if (color == "red") {
    edge.addClass('highlighted-red');
  } else {
    edge.target().addClass("highlighted-node");
    edge.addClass('highlighted');
  }

}

function unHighlightEdge(id, color) {
  let edge = cy.edges().filter(x => x.data('id') == id)
  if (color == "red") {
    edge.removeClass('highlighted-red')
  } else {
    edge.removeClass('highlighted');
  }
  edge.target().removeClass("highlighted-node");
}

function highlightTick(i) {
  for (e = 0; e < tick_edges[i].length; e++) {
    highlightEdge(tick_edges[i][e][0], tick_edges[i][e][1]);
  }
}

function unHighlightTick(i) {
  for (e = 0; e < tick_edges[i].length; e++) {
    unHighlightEdge(tick_edges[i][e][0], tick_edges[i][e][1]);
  }
}

// Holds the current tick
var i = 0;

var tick_edges = [
  [
    ["ae", "red"],
    ["ab", "blue"],
  ],
  [
    ["bc", "red"],
    ["be", "blue"],
    ["ec", "red"],
  ],
  [
    ["cd", "red"],
  ],
  [
    ["di", "red"],
    ["dj", "red"],
    ["dg", "red"],
    ["dh", "red"],
  ],
]

// Performs highlights at each tick
var nextHighlight = function(){
  if (i < tick_edges.length) {
    console.log(tick_edges[i]);
    highlightTick(i);
    if (i > 0) {
      unHighlightTick(i - 1);
    }
    i++;
    // Kick off next highlight
    setTimeout(nextHighlight, 1000);
  } else {
    unHighlightTick(tick_edges.length - 1);
  }
};


// Kick off first highlight
nextHighlight();