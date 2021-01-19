import xml.etree.ElementTree as ET
import json
from settings import OUT_PATH
import os

def extract_indexes(text):
    k1 = text.find('_')
    k2 = text.find('_', k1+1)
    first = int(text[k1+1:k2])
    last = int(text[k2+1:])
    return (first, last)

def extract_indexes_from_text(nodes, element):
    source_index = nodes.index(element.find('source').text)
    target_index = nodes.index(element.find('target').text)
    first = min(source_index, target_index)
    last = max(source_index, target_index)
    return (first, last)

def create_polska_json():
    XML_NETWORK_PATH = '../dane/polska.xml'

    tree = ET.parse(XML_NETWORK_PATH)
    root = tree.getroot()

    nodes = [n.get('id') for n in root.iter('node')]

    links = {}
    demands = {}
    for link in root.iter('link'):
        first, last = extract_indexes(link.get('id'))
        data = {}
        data['setupCost'] = float(link.find('setupCost').text)
        i = 0
        for module in link.iter('addModule'):
            data['capacity{}'.format(i)] = float(module.find('capacity').text)
            data['cost{}'.format(i)] = float(module.find('cost').text)
            i += 1
        links.setdefault(first, {})[last] = data

    for demand in root.iter('demand'):
        first, last = extract_indexes(demand.get('id'))
        demandValue = float(demand.find('demandValue').text)
        admissiblePaths = []
        for admissiblePath in demand.iter('admissiblePath'):
            path = [extract_indexes(link_id.text) for link_id in admissiblePath.iter('linkId')]
            admissiblePaths.append(path)
        
        link_data = links.setdefault(first, {}).setdefault(last, {})
        link_data['demand'] = demandValue
        link_data['admissiblePaths'] = admissiblePaths

        demand_data = demands.setdefault(first, {}).setdefault(last, {})
        demand_data['demand'] = demandValue
        demand_data['admissiblePaths'] = admissiblePaths

    polska = {
        'nodes': nodes,
        'links': links,
        'demands': demands
    }
    with open(os.path.join(OUT_PATH, 'polska.json'), 'w') as f:
        json.dump(polska, f)

create_polska_json()
with open(os.path.join(OUT_PATH, 'polska.json'), 'r') as f:
    data = json.load(f)
links = data['links']
nodes = data['nodes']
demands = data['demands']
