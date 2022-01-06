import dash
import dash_cytoscape as cyto
import dash_html_components as html
import Graph as gp
import dash_core_components as dcc
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)
graph = gp.graph()
graph.loadJson()
cyto.load_extra_layouts()

default_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'background-color': '#ff00ff',
            'label': 'data(label)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'line-color': '#800080',
        }
    }
]

nodes = [
    {
        'data': {'id': str(key.id), 'label': key.name, 'classes': 'blue'} 
    }
    for key in graph.graph]


edges = []
templist = []
for key in graph.graph:
    for value in graph.graph[key]:
        if value not in templist:
            edges.append({'data': {'source': str(key.id), 'target': str(value.id)}})   
    templist.append(key)

elements = nodes + edges

app.layout = html.Div([
    cyto.Cytoscape(
        id='main-cytoscape',
        elements=elements,
        stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '800px'},
        layout={
            'name': 'klay',
            'roots': '#van, #mtl'
        }   
    ),
    html.Button('Add Node', id='btn-add-node', n_clicks_timestamp=0),
    html.Button('Remove Node', id='btn-remove-node', n_clicks_timestamp=0),

    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'NodeId:',
        dcc.Input(id='node1-id', type='text')
    ]),
    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'NodeId2:',
        dcc.Input(id='node2-id', type='text')
    ]),
    html.Div(style={'width': '50%', 'display': 'inline'}, children=[
        'Name:',
        dcc.Input(id='node-name', type='text')
    ])
])

@app.callback(Output('main-cytoscape', 'elements'),  
              State('node1-id', 'value'),
              State('node2-id', 'value'),
              State('node-name', 'value'),             
              Input('btn-add-node', 'n_clicks_timestamp'),
              State('main-cytoscape','elements')
              )

def addnode(node1, node2, nodename, btn_add_node, elements):
    
    # If the add button was clicked most recently and there are nodes to add
    if int(btn_add_node) > 0 and node1  and nodename :
        # add a node
        elements = getnode()
        graph.addNode(int(node1), nodename)
        if int(node1) not in graph.nodesadded:
            elements.append([{'data': {'id': node1, 'label': nodename, 'classes': 'blue'} }])
            graph.nodesadded.append(int(node1))
        return elements

def getvalues():
    node1 = dcc.Input(id='node1-id', type='text') 
    node2 = dcc.Input(id='node2-id', type='text')   
    nodename = dcc.Input(id='node-name', type='text')
    return node1, node2, nodename

def getnode():
    nodes = [
        {
            'data': {'id': str(key.id), 'label': key.name, 'classes': 'blue'} 
        }
        for key in graph.graph]


    edges = []
    templist = []
    for key in graph.graph:
        for value in graph.graph[key]:
            if value not in templist:
                edges.append({'data': {'source': str(key.id), 'target': str(value.id)}})   
        templist.append(key)

    elements = nodes + edges
    return elements
    
if __name__ == '__main__':
    app.run_server(debug=True)