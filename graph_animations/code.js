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
      }),
      .selector('.highlighted-red')
      .style({
        'background-color': '#FF0000',
        'line-color': '#FF0000',
        'target-arrow-color': '#FF0000',
        'transition-property': 'background-color, line-color, target-arrow-color',
        'transition-duration': '0.5s'
      }),

  elements: {
      nodes: [
        { data: { id: 'a' } },
        { data: { id: 'b' } },
        { data: { id: 'c' } },
        { data: { id: 'd' } },
        { data: { id: 'e' } },
        { data: { id: 'g' } },
        { data: { id: 'h' } },
        { data: { id: 'i' } },
        { data: { id: 'j' } },
      ],

      edges: [
        { data: { id: 'ae', weight: 1, source: 'a', target: 'e' } },
        { data: { id: 'ab', weight: 3, source: 'a', target: 'b' } },
        { data: { id: 'be', weight: 4, source: 'b', target: 'e' } },
        { data: { id: 'bc', weight: 5, source: 'b', target: 'c' } },
        { data: { id: 'ec', weight: 6, source: 'e', target: 'c' } },
        { data: { id: 'cd', weight: 2, source: 'c', target: 'd' } },
        { data: { id: 'dh', weight: 7, source: 'd', target: 'h' } },
        { data: { id: 'di', weight: 7, source: 'd', target: 'i' } },
        { data: { id: 'dj', weight: 7, source: 'd', target: 'j' } },
        { data: { id: 'dg', weight: 7, source: 'd', target: 'g' } }
      ]
    },

  layout: {
    name: 'breadthfirst',
    directed: true,
    roots: '#a',
    padding: 5
  }
});

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

function unHighlightEdge(id) {
  let edge = cy.edges().filter(x => x.data('id') == id)
  edge.removeClass('highlighted');
  edge.target().removeClass("highlighted-node");
}

function highlightTick(i) {
  for (e = 0; e < ticks[i].length; e++) {
    highlightEdge(ticks[i][e][0], ticks[i][e][1]);
  }
}

function unHighlightTick(i) {
  for (e = 0; e < ticks[i].length; e++) {
    unHighlightEdge(ticks[i][e]);
  }
}

// Holds the current tick
var i = 0;

var ticks = [
  [
    {"ae" : "red"},
    "ab",
  ],
  [
    "bc",
    "be",
    "ec",
  ],
  [
    "cd",
  ],
  [
    "di",
    "dj",
    "dg",
    "dh",
  ],
]

// Performs highlights at each tick
var nextHighlight = function(){
  if (i < ticks.length) {
    console.log(ticks[i]);
    highlightTick(i);
    if (i > 0) {
      unHighlightTick(i - 1);
    }
    i++;
    // Kick off next highlight
    setTimeout(nextHighlight, 1000);
  } else {
    unHighlightTick(ticks.length - 1);
  }
};


// Kick off first highlight
nextHighlight();