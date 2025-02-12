import json
import networkx as nx
import matplotlib.pyplot as plt

# JSON data
json_data = """
{
  "Geology": {
    "Introduction to Geology": {
      "Definition and Scope": [],
      "Branches of Geology": [],
      "Importance of Geology": []
    },
    "Mineralogy": {
      "Mineral Properties": {
        "Physical Properties": [],
        "Chemical Properties": []
      },
      "Mineral Identification": [],
      "Crystallography": []
    },
    "Petrology": {
      "Igneous Rocks": {
        "Formation": [],
        "Classification": []
      },
      "Sedimentary Rocks": {
        "Formation": [],
        "Classification": []
      },
      "Metamorphic Rocks": {
        "Formation": [],
        "Classification": []
      }
    },
    "Structural Geology": {
      "Rock Deformation": {
        "Folding": [],
        "Faulting": []
      },
      "Geological Maps": []
    },
    "Paleontology": {
      "Fossilization Process": [],
      "Types of Fossils": [],
      "Evolutionary Biology": []
    },
    "Geophysics": {
      "Seismology": {
        "Earthquakes": [],
        "Seismic Waves": []
      },
      "Magnetism": [],
      "Gravimetry": []
    },
    "Hydrogeology": {
      "Water Cycle": [],
      "Groundwater Flow": [],
      "Aquifer Properties": []
    },
    "Environmental Geology": {
      "Natural Hazards": {
        "Earthquakes": [],
        "Volcanoes": [],
        "Landslides": []
      },
      "Pollution": {
        "Water Pollution": [],
        "Soil Pollution": [],
        "Air Pollution": []
      }
    },
    "Economic Geology": {
      "Ore Deposits": [],
      "Mining Techniques": [],
      "Resource Management": []
    },
    "Field Methods": {
      "Geological Mapping": [],
      "Sampling Techniques": [],
      "Geophysical Surveys": []
    },
    "Research and Careers": {
      "Academic Research": [],
      "Industry Careers": [],
      "Government and Policy": []
    }
  }
}
"""

# Convert JSON data to Python dictionary
data = json.loads(json_data)

# Create Graph object
graph = nx.Graph()

# Function to recursively add nodes and edges
def add_nodes_edges(data, parent=None):
    for key, value in data.items():
        # Add node for current key
        graph.add_node(key)
        
        # If parent exists, add edge from parent to current key
        if parent:
            graph.add_edge(parent, key)
        
        # If value is a dictionary, recursively call function
        if isinstance(value, dict):
            add_nodes_edges(value, parent=key)

# Start adding nodes and edges from the top-level key
add_nodes_edges(data)

# Draw graph
pos = nx.spring_layout(graph, k=0.5, iterations=50)  # Positions for all nodes
nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=8, font_color='black', edge_color='#666666', linewidths=0.5)

# Save plot as image
plt.savefig('roadmap.png', format='png', dpi=300)

# Display the plot
# plt.show()
