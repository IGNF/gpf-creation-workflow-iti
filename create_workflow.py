import argparse
import sys
import os

args = None
def parse() -> None:
    """Parse call arguments and check values

    Exit program if an error occured
    """
    global args

    # CLI call parser
    parser = argparse.ArgumentParser(
        prog="create_workflow.py",
        description="Tool to create a itinerary workflow",
        epilog="",
    )

    parser.add_argument(
        "--upload",
        metavar="bd_topo_upload",
        action="store",
        dest="upload",
        help="Upload's name (in case of the creation of an upload)",
        required=False,
    )

    parser.add_argument(
        "--stored_data_database",
        metavar="bd_topo_v1",
        action="store",
        dest="stored_data_database",
        help="Name of the stored data with the vector data (to create in case of the creation of an upload)",
        required=True,
    )

    parser.add_argument(
        "--stored_data_pivot",
        metavar="pivot",
        action="store",
        dest="stored_data_pivot",
        help="Name of the pivot",
        required=True,
    )

    parser.add_argument(
        "--graph",
        choices=["osrm", "pgrouting", "valhalla", "all"],
        nargs='*',
        action="store",
        dest="graph",
        help="Types of graph you want to create",
        required=True,
    )

    parser.add_argument(
        "--update",
        choices=["true", "false"],
        default="false",
        action="store",
        dest="update",
        help="true if you want to update existent stored data",
        required=False,
    )

    parser.add_argument(
        "--stored_data_graph_valhalla",
        metavar="graph_valhalla",
        action="store",
        dest="stored_data_graph_valhalla",
        help="Name of the graph valhalla (only for --graph=valhalla or all)",
        required=False,
    )

    parser.add_argument(
        "--configuration_name_valhalla",
        metavar="Service itinéraire Valhalla",
        action="store",
        dest="configuration_name_valhalla",
        help="Name of the configuration valhalla (only for --graph=valhalla or all and --update=false)",
        required=False,
    )

    parser.add_argument(
        "--configuration_layer_name_valhalla",
        metavar="bdtopo-valhalla",
        action="store",
        dest="configuration_layer_name_valhalla",
        help="Layer Name of the configuration valhalla (only for --graph=valhalla or all and --update=false)",
        required=False,
    )

    parser.add_argument(
        "--stored_data_graph_pgr",
        metavar="graph_pgr",
        action="store",
        dest="stored_data_graph_pgr",
        help="Name of the graph pgRouting (only for --graph=pgrouting or all)",
        required=False,
    )

    parser.add_argument(
        "--configuration_name_pgr",
        metavar="Service itinéraire pgRouting",
        action="store",
        dest="configuration_name_pgr",
        help="Name of the configuration pgRouting (only for --graph=pgrouting or all and --update=false)",
        required=False,
    )

    parser.add_argument(
        "--configuration_layer_name_pgr",
        metavar="bdtopo-pgr",
        action="store",
        dest="configuration_layer_name_pgr",
        help="Layer Name of the configuration pgRouting (only for --graph=pgrouting or all and --update=false)",
        required=False,
    )

    parser.add_argument(
        "--stored_data_graph_osrm",
        metavar="graph_osrm",
        action="store",
        dest="stored_data_graph_osrm",
        help="Name of the graph OSRM (only for --graph=osrm or all)",
        required=False,
    )

    parser.add_argument(
        "--configuration_name_osrm",
        metavar="Service itinéraire OSRM",
        action="store",
        dest="configuration_name_osrm",
        help="Name of the configuration OSRM (only for --graph=osrm or all and --update=false)",
        required=False,
    )

    parser.add_argument(
        "--configuration_layer_name_osrm",
        metavar="bdtopo-osrm",
        action="store",
        dest="configuration_layer_name_osrm",
        help="Layer Name of the configuration OSRM (only for --graph=osrm or all and --update=false)",
        required=False,
    )

    parser.add_argument(
        "--path_file",
        metavar="/path/to/file/to/create",
        action="store",
        dest="path_file",
        help="Path to save the workflow",
        required=True,
    )

    parser.add_argument(
        "--config",
        metavar="config.ini",
        action="store",
        default="config.ini",
        dest="config",
        help="Path to the config file",
        required=False,
    )

    parser.add_argument(
        "--run",
        choices=["true", "false"],
        default="true",
        action="store",
        dest="run",
        help="true if you want to run the workflow after his creation",
        required=False,
    )

    args = parser.parse_args()

    if ("valhalla" in args.graph or "all" in args.graph) and args.stored_data_graph_valhalla is None :
        print("Error : argument --stored_data_graph_valhalla is required if you want to create or update a graph valhalla")
        sys.exit(1)

    if ("pgrouting" in args.graph or "all" in args.graph) and args.stored_data_graph_pgr is None :
        print("Error : argument --stored_data_graph_pgr is required if you want to create or update a graph pgRouting")
        sys.exit(1)
    
    if ("osrm" in args.graph or "all" in args.graph) and args.stored_data_graph_osrm is None :
        print("Error : argument --stored_data_graph_osrm is required if you want to create or update a graph OSRM")
        sys.exit(1)

    if ("valhalla" in args.graph or "all" in args.graph) and args.update == "false" and (args.configuration_name_valhalla is None or args.configuration_layer_name_valhalla is None) :
        print("Error : argument --configuration_name_valhalla and --configuration_layer_name_valhalla are required if you want to create a graph valhalla")
        sys.exit(1)

    if ("pgrouting" in args.graph or "all" in args.graph) and args.update == "false" and (args.configuration_name_pgr is None or args.configuration_layer_name_pgr is None) :
        print("Error : argument --configuration_name_pgr and --configuration_layer_name_pgr are required if you want to create a graph pgRouting")
        sys.exit(1)

    if ("osrm" in args.graph or "all" in args.graph) and args.update == "false" and (args.configuration_name_osrm is None or args.configuration_layer_name_osrm is None) :
        print("Error : argument --configuration_name_osrm and --configuration_layer_name_osrm are required if you want to create a graph OSRM")
        sys.exit(1)

def creation_workflow(args) -> str :
    """Create the workflow of the actions to perform

    Return a string of the workflow
    """
    text = """{
    "workflow": {
        "steps": {"""
    if args.upload is not None :
        text += '''
            "mise-en-base": {
                "actions": [
                    {
                        "type": "processing-execution",
                        "body_parameters": {
                            "processing": "{store_entity.processing.infos._id [INFOS(name=Intégration de données vecteur livrées en base)]}",
                            "inputs": {
                                "upload": [
                                    "{store_entity.upload.infos._id [INFOS(name=''' + args.upload + ''')]}"
                                ]
                            },
                            "output": {
                                "stored_data": {
                                    "name": "''' + args.stored_data_database + '''"
                                }
                            },
                            "parameters": {
                            
                            }
                        },
                        "comments": [
                            "Ajout d'un département de la BDTopo"
                        ]
                    }
                ],
                "parents": []
            },'''
    
    text += '''
            "vector-db-to-pivot-road2": {
                "actions": [
                    {
                        "type": "processing-execution",
                        "body_parameters": {
                            "processing": "{store_entity.processing.infos._id [INFOS(name=vector-db-to-pivot-road2)]}",
                            "inputs": {
                                "stored_data": [
                                    "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_database + ''')]}"
                                ]
                            },
                            "output": {
                                "stored_data": {
                                    "name": "''' + args.stored_data_pivot + '''",
                                    "storage_tags": ["IGN","VECTEUR"]
                                }
                            },
                            "parameters": {
                            
                            }
                        },
                        "comments": [
                            "Création de base pivot Road2"
                        ]
                    }
                ],
                "parents": []
            },'''
    
    if ("valhalla" in args.graph or "all" in args.graph) and args.update == "false" :
        text += '''
            "pivot-road2-to-graph-valhalla": {
                "actions": [
                    {
                        "type": "processing-execution",
                        "body_parameters": {
                            "processing": "{store_entity.processing.infos._id [INFOS(name=pivot-road2-to-graph-valhalla)]}",
                            "inputs": {
                                "stored_data": [
                                    "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_pivot + ''')]}"
                                ]
                            },
                            "output": {
                                "stored_data": {
                                    "name": "''' + args.stored_data_graph_valhalla + '''",
                                    "storage_tags": ["OTHERS","PERF"]
                                }
                            },
                            "parameters": {
                                "cost_calculations": [
                                    {
                                        "name": "CC_car",
                                        "variables": [
                                            {
                                                "name": "nature",
                                                "column_name": "nature",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "length_m",
                                                "column_name": "length_m",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "vitesse_voiture",
                                                "column_name": "vitesse_moyenne_vl",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "sens",
                                                "column_name": "direction",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "urbain",
                                                "column_name": "urbain",
                                                "mapping": {
                                                    "True": 5,
                                                    "False": 0
                                                }
                                            }
                                        ],
                                        "outputs": [
                                            {
                                                "name": "cost_m_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "distance",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ]
                                                ]
                                            },
                                            {
                                                "name": "cost_s_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "duration",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ],
                                                    [
                                                        "divide",
                                                        "vitesse_voiture"
                                                    ],
                                                    [
                                                        "multiply",
                                                        3.6
                                                    ],
                                                    [
                                                        "add",
                                                        "urbain"
                                                    ]
                                                ]
                                            },
                                            {
                                              "name": "cost_m_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "distance",
                                              "operations": [
                                                ["add", "length_m"]
                                              ]
                                            },
                                            {
                                              "name": "cost_s_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "duration",
                                              "operations": [
                                                ["add", "length_m"],
                                                ["multiply", 0.9]
                                              ]
                                            }
                                        ]
                                    }
                                ],
                                "costs": [
                                    {
                                        "profile": "car",
                                        "optimization": "fastest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "fastest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "cost_calculation": "CC_car"
                                    }
                                ]
                            }
                        },
                        "comments": [
                            "Création d'un graph valhalla'"
                        ]
                    }
                ],
                "parents": ["vector-db-to-pivot-road2"]
            },
            "configuration-iti-valhalla": {
                "actions": [
                    {
                        "type": "configuration",
                        "body_parameters": {
                            "type": "ITINERARY-ISOCURVE",
                            "name": "''' + args.configuration_name_valhalla + '''",
                            "layer_name": "''' + args.configuration_layer_name_valhalla + '''",
                            "type_infos": {
                                "title": "itineraire_valahalla",
                                "abstract": "Publication du service Itinéraire via Valhalla",
                                "keywords": ["valhalla", "itineraire", "publication"],
                                "used_data": [
                                    {
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_valhalla + ''')]}",
                                        "profile": "car",
                                        "optimization": "fastest",
                                        "cost_type": "time",
                                        "costing": "auto"
                                    },
                                    {
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_valhalla + ''')]}",
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "cost_type": "distance",
                                        "costing": "auto_shorter"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "cost_type": "distance",
                                        "costing": "pedestrian",
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_valhalla + ''')]}"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "fastest",
                                        "cost_type": "time",
                                        "costing": "pedestrian",
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_valhalla + ''')]}"
                                    }
                                ],
                                "constraints": {
                                    "defaultPreferredCostRatio": 0.8,
                                    "defaultAvoidCostRatio": 1.2,
                                    "values": [
                                        {
                                            "keyType": "name-valhalla",
                                            "key": "wayType",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "availableValues": [
                                                {
                                                    "value": "autoroute",
                                                    "field": "exclude_tolls"
                                                },
                                                {
                                                    "value": "pont",
                                                    "field": "exclude_bridges"
                                                },
                                                {
                                                    "value": "tunnel",
                                                    "field": "exclude_tunnels"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        },
                        "comments": [
                            "Configuration d'un flux itinéraire valhalla"
                        ]
                    }
                ],
                "parents": [
                    "pivot-road2-to-graph-valhalla"
                ]
            },
            "publication-itineraire-valhalla": {
                "actions": [
                    {
                        "type": "offering",
                        "url_parameters": {
                            "configuration": "{store_entity.configuration.infos._id [INFOS(name=''' + args.configuration_name_valhalla + ''')]}"
                        },
                        "body_parameters": {
                            "endpoint": "{store_entity.endpoint.infos._id [INFOS(technical_name=gpf-road2)]}",
                            "visibility": "PUBLIC",
                            "open": true
                        }
                    }
                ],
                "parents": []
            },'''
    if ("valhalla" in args.graph or "all" in args.graph) and args.update == "true" :
        text += '''
            "pivot-road2-to-graph-valhalla": {
                "actions": [
                    {
                        "type": "processing-execution",
                        "body_parameters": {
                            "processing": "{store_entity.processing.infos._id [INFOS(name=pivot-road2-to-graph-valhalla)]}",
                            "inputs": {
                                "stored_data": [
                                    "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_pivot + ''')]}"
                                ]
                            },
                            "output": {
                                "stored_data": {
                                    "id": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_valhalla + ''')]}"
                                }
                            },
                            "parameters": {
                                "cost_calculations": [
                                    {
                                        "name": "CC_car",
                                        "variables": [
                                            {
                                                "name": "nature",
                                                "column_name": "nature",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "length_m",
                                                "column_name": "length_m",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "vitesse_voiture",
                                                "column_name": "vitesse_moyenne_vl",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "sens",
                                                "column_name": "direction",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "urbain",
                                                "column_name": "urbain",
                                                "mapping": {
                                                    "True": 5,
                                                    "False": 0
                                                }
                                            }
                                        ],
                                        "outputs": [
                                            {
                                                "name": "cost_m_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "distance",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ]
                                                ]
                                            },
                                            {
                                                "name": "cost_s_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "duration",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ],
                                                    [
                                                        "divide",
                                                        "vitesse_voiture"
                                                    ],
                                                    [
                                                        "multiply",
                                                        3.6
                                                    ],
                                                    [
                                                        "add",
                                                        "urbain"
                                                    ]
                                                ]
                                            },
                                            {
                                              "name": "cost_m_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "distance",
                                              "operations": [
                                                ["add", "length_m"]
                                              ]
                                            },
                                            {
                                              "name": "cost_s_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "duration",
                                              "operations": [
                                                ["add", "length_m"],
                                                ["multiply", 0.9]
                                              ]
                                            }
                                        ]
                                    }
                                ],
                                "costs": [
                                    {
                                        "profile": "car",
                                        "optimization": "fastest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "fastest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "cost_calculation": "CC_car"
                                    }
                                ]
                            }
                        },
                        "comments": [
                            "Création d'un graph valhalla'"
                        ]
                    }
                ],
                "parents": ["vector-db-to-pivot-road2"]
            },
            "synchronisation-offering-valhalla": {
                "actions": [
                    {
                        "type": "synchronize-offering",
                        "filter_infos": {"configuration" : "{store_entity.configuration.infos._id [INFOS(stored_data={store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_valhalla + ''')]})]}"}
                    }
                ],
                "parents": []
            },'''
    if ("pgrouting" in args.graph or "all" in args.graph) and args.update == "false" :
        text += '''
            "pivot-road2-to-graph-db": {
                "actions": [
                    {
                        "type": "processing-execution",
                        "body_parameters": {
                            "processing": "{store_entity.processing.infos._id [INFOS(name=pivot-road2-to-graph-db)]}",
                            "inputs": {
                                "stored_data": [
                                    "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_pivot + ''')]}"
                                ]
                            },
                            "output": {
                                "stored_data": {
                                    "name": "''' + args.stored_data_graph_pgr + '''",
                                    "storage_tags": ["IGN","VECTEUR"]
                                }
                            },
                            "parameters": {
                                "cost_calculations": [
                                    {
                                        "name": "CC_car",
                                        "variables": [
                                            {
                                                "name": "nature",
                                                "column_name": "nature",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "length_m",
                                                "column_name": "length_m",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "vitesse_voiture",
                                                "column_name": "vitesse_moyenne_vl",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "sens",
                                                "column_name": "direction",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "urbain",
                                                "column_name": "urbain",
                                                "mapping": {
                                                    "True": 5,
                                                    "False": 0
                                                }
                                            }
                                        ],
                                        "outputs": [
                                            {
                                                "name": "cost_m_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "distance",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ]
                                                ]
                                            },
                                            {
                                                "name": "cost_s_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "duration",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ],
                                                    [
                                                        "divide",
                                                        "vitesse_voiture"
                                                    ],
                                                    [
                                                        "multiply",
                                                        3.6
                                                    ],
                                                    [
                                                        "add",
                                                        "urbain"
                                                    ]
                                                ]
                                            },
                                            {
                                              "name": "cost_m_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "distance",
                                              "operations": [
                                                ["add", "length_m"]
                                              ]
                                            },
                                            {
                                              "name": "cost_s_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "duration",
                                              "operations": [
                                                ["add", "length_m"],
                                                ["multiply", 0.9]
                                              ]
                                            }
                                        ]
                                    }
                                ],
                                "costs": [
                                    {
                                        "profile": "car",
                                        "optimization": "fastest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "fastest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "cost_calculation": "CC_car"
                                    }
                                ]
                            }
                        },
                        "comments": [
                            "Création d'un graph pgr'"
                        ]
                    }
                ],
                "parents": ["vector-db-to-pivot-road2"]
            },
            "configuration-iti-pgr": {
                "actions": [
                    {
                        "type": "configuration",
                        "body_parameters": {
                            "type": "ITINERARY-ISOCURVE",
                            "name": "''' + args.configuration_name_pgr + '''",
                            "layer_name": "''' + args.configuration_layer_name_pgr + '''",
                            "type_infos": {
                                "title": "pgrouting",
                                "abstract": "Publication du service Itinéraire / Isochrone via PGRouting",
                                "keywords": ["pgrouting", "itineraire", "publication", "isochrone"],
                                "used_data": [
                                    {
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_pgr + ''')]}",
                                        "profile": "car",
                                        "optimization": "fastest",
                                        "cost_column": "cost_s_car",
                                        "reverse_cost_column": "reverse_cost_s_car",
                                        "cost_type": "time",
                                        "attributes": [
                                            {
                                                "public_name": "name",
                                                "native_name": "name",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "nom_1_gauche",
                                                "native_name": "nom_1_gauche",
                                                "default": "true"
                                            },
                                            {
                                                "public_name": "nom_1_droite",
                                                "native_name": "nom_1_droite",
                                                "default": "true"
                                            },
                                            {
                                                "public_name": "cpx_numero",
                                                "native_name": "cpx_numero",
                                                "default": "true"
                                            },
                                            {
                                                "public_name": "cpx_toponyme_route_nommee",
                                                "native_name": "cpx_toponyme_route_nommee",
                                                "default": "true"
                                            },
                                            {
                                                "public_name": "cleabs",
                                                "native_name": "cleabs",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "nature",
                                                "native_name": "nature",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "importance",
                                                "native_name": "importance",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "position_par_rapport_au_sol",
                                                "native_name": "position_par_rapport_au_sol",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "nombre_de_voies",
                                                "native_name": "nombre_de_voies",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "largeur_de_chaussee",
                                                "native_name": "largeur_de_chaussee",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "itineraire_vert",
                                                "native_name": "itineraire_vert",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "sens_de_circulation",
                                                "native_name": "sens_de_circulation",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "bande_cyclable",
                                                "native_name": "bande_cyclable",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "reserve_aux_bus",
                                                "native_name": "reserve_aux_bus",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "urbain",
                                                "native_name": "urbain",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "vitesse_moyenne_vl",
                                                "native_name": "vitesse_moyenne_vl",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "acces_vehicule_leger",
                                                "native_name": "acces_vehicule_leger",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "acces_pieton",
                                                "native_name": "acces_pieton",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "nature_de_la_restriction",
                                                "native_name": "nature_de_la_restriction",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_hauteur",
                                                "native_name": "restriction_de_hauteur",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_poids_total",
                                                "native_name": "restriction_de_poids_total",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_poids_par_essieu",
                                                "native_name": "restriction_de_poids_par_essieu",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_largeur",
                                                "native_name": "restriction_de_largeur",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_longueur",
                                                "native_name": "restriction_de_longueur",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "matieres_dangereuses_interdites",
                                                "native_name": "matieres_dangereuses_interdites",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "insee_commune_gauche",
                                                "native_name": "insee_commune_gauche",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "insee_commune_droite",
                                                "native_name": "insee_commune_droite",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "cpx_numero_route_europeenne",
                                                "native_name": "cpx_numero_route_europeenne",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "cpx_classement_administratif",
                                                "native_name": "cpx_classement_administratif",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "cpx_gestionnaire",
                                                "native_name": "cpx_gestionnaire",
                                                "default": "false"
                                            }
                                        ]
                                    },
                                    {
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_pgr + ''')]}",
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "cost_column": "cost_m_car",
                                        "reverse_cost_column": "reverse_cost_m_car",
                                        "cost_type": "distance",
                                        "attributes": [
                                            {
                                                "public_name": "name",
                                                "native_name": "name",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "nom_1_gauche",
                                                "native_name": "nom_1_gauche",
                                                "default": "true"
                                            },
                                            {
                                                "public_name": "nom_1_droite",
                                                "native_name": "nom_1_droite",
                                                "default": "true"
                                            },
                                            {
                                                "public_name": "cpx_numero",
                                                "native_name": "cpx_numero",
                                                "default": "true"
                                            },
                                            {
                                                "public_name": "cpx_toponyme_route_nommee",
                                                "native_name": "cpx_toponyme_route_nommee",
                                                "default": "true"
                                            },
                                            {
                                                "public_name": "cleabs",
                                                "native_name": "cleabs",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "nature",
                                                "native_name": "nature",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "importance",
                                                "native_name": "importance",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "position_par_rapport_au_sol",
                                                "native_name": "position_par_rapport_au_sol",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "nombre_de_voies",
                                                "native_name": "nombre_de_voies",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "largeur_de_chaussee",
                                                "native_name": "largeur_de_chaussee",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "itineraire_vert",
                                                "native_name": "itineraire_vert",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "sens_de_circulation",
                                                "native_name": "sens_de_circulation",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "bande_cyclable",
                                                "native_name": "bande_cyclable",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "reserve_aux_bus",
                                                "native_name": "reserve_aux_bus",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "urbain",
                                                "native_name": "urbain",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "vitesse_moyenne_vl",
                                                "native_name": "vitesse_moyenne_vl",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "acces_vehicule_leger",
                                                "native_name": "acces_vehicule_leger",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "acces_pieton",
                                                "native_name": "acces_pieton",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "nature_de_la_restriction",
                                                "native_name": "nature_de_la_restriction",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_hauteur",
                                                "native_name": "restriction_de_hauteur",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_poids_total",
                                                "native_name": "restriction_de_poids_total",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_poids_par_essieu",
                                                "native_name": "restriction_de_poids_par_essieu",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_largeur",
                                                "native_name": "restriction_de_largeur",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "restriction_de_longueur",
                                                "native_name": "restriction_de_longueur",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "matieres_dangereuses_interdites",
                                                "native_name": "matieres_dangereuses_interdites",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "insee_commune_gauche",
                                                "native_name": "insee_commune_gauche",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "insee_commune_droite",
                                                "native_name": "insee_commune_droite",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "cpx_numero_route_europeenne",
                                                "native_name": "cpx_numero_route_europeenne",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "cpx_classement_administratif",
                                                "native_name": "cpx_classement_administratif",
                                                "default": "false"
                                            },
                                            {
                                                "public_name": "cpx_gestionnaire",
                                                "native_name": "cpx_gestionnaire",
                                                "default": "false"
                                            }
                                        ]
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "fastest",
                                        "cost_column": "cost_s_pedestrian",
                                        "reverse_cost_column": "reverse_cost_s_pedestrian",
                                        "cost_type": "time",
                                        "attributes": [
                                            {
                                                "table_name": "ways",
                                                "native_name": "name",
                                                "public_name": "name",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "insee_commune_droite",
                                                "public_name": "insee_commune_droite",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_poids_par_essieu",
                                                "public_name": "restriction_de_poids_par_essieu",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nature",
                                                "public_name": "nature",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "importance",
                                                "public_name": "importance",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "insee_commune_gauche",
                                                "public_name": "insee_commune_gauche",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "acces_pieton",
                                                "public_name": "acces_pieton",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "bande_cyclable",
                                                "public_name": "bande_cyclable",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nombre_de_voies",
                                                "public_name": "nombre_de_voies",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_poids_total",
                                                "public_name": "restriction_de_poids_total",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "position_par_rapport_au_sol",
                                                "public_name": "position_par_rapport_au_sol",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "urbain",
                                                "public_name": "urbain",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_hauteur",
                                                "public_name": "restriction_de_hauteur",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "itineraire_vert",
                                                "public_name": "itineraire_vert",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cleabs",
                                                "public_name": "cleabs",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "sens_de_circulation",
                                                "public_name": "sens_de_circulation",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "vitesse_moyenne_vl",
                                                "public_name": "vitesse_moyenne_vl",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_numero",
                                                "public_name": "cpx_numero",
                                                "default": true
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_classement_administratif",
                                                "public_name": "cpx_classement_administratif",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_gestionnaire",
                                                "public_name": "cpx_gestionnaire",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_toponyme_route_nommee",
                                                "public_name": "cpx_toponyme_route_nommee",
                                                "default": true
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "acces_vehicule_leger",
                                                "public_name": "acces_vehicule_leger",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nom_1_gauche",
                                                "public_name": "nom_1_gauche",
                                                "default": true
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "largeur_de_chaussee",
                                                "public_name": "largeur_de_chaussee",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nature_de_la_restriction",
                                                "public_name": "nature_de_la_restriction",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_numero_route_europeenne",
                                                "public_name": "cpx_numero_route_europeenne",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "reserve_aux_bus",
                                                "public_name": "reserve_aux_bus",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "matieres_dangereuses_interdites",
                                                "public_name": "matieres_dangereuses_interdites",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_largeur",
                                                "public_name": "restriction_de_largeur",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nom_1_droite",
                                                "public_name": "nom_1_droite",
                                                "default": true
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_longueur",
                                                "public_name": "restriction_de_longueur",
                                                "default": false
                                            }
                                        ],
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_pgr + ''')]}"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "cost_column": "cost_m_pedestrian",
                                        "reverse_cost_column": "reverse_cost_m_pedestrian",
                                        "cost_type": "distance",
                                        "attributes": [
                                            {
                                                "table_name": "ways",
                                                "native_name": "name",
                                                "public_name": "name",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "insee_commune_droite",
                                                "public_name": "insee_commune_droite",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_poids_par_essieu",
                                                "public_name": "restriction_de_poids_par_essieu",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nature",
                                                "public_name": "nature",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "importance",
                                                "public_name": "importance",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "insee_commune_gauche",
                                                "public_name": "insee_commune_gauche",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "acces_pieton",
                                                "public_name": "acces_pieton",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "bande_cyclable",
                                                "public_name": "bande_cyclable",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nombre_de_voies",
                                                "public_name": "nombre_de_voies",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_poids_total",
                                                "public_name": "restriction_de_poids_total",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "position_par_rapport_au_sol",
                                                "public_name": "position_par_rapport_au_sol",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "urbain",
                                                "public_name": "urbain",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_hauteur",
                                                "public_name": "restriction_de_hauteur",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "itineraire_vert",
                                                "public_name": "itineraire_vert",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cleabs",
                                                "public_name": "cleabs",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "sens_de_circulation",
                                                "public_name": "sens_de_circulation",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "vitesse_moyenne_vl",
                                                "public_name": "vitesse_moyenne_vl",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_numero",
                                                "public_name": "cpx_numero",
                                                "default": true
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_classement_administratif",
                                                "public_name": "cpx_classement_administratif",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_gestionnaire",
                                                "public_name": "cpx_gestionnaire",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_toponyme_route_nommee",
                                                "public_name": "cpx_toponyme_route_nommee",
                                                "default": true
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "acces_vehicule_leger",
                                                "public_name": "acces_vehicule_leger",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nom_1_gauche",
                                                "public_name": "nom_1_gauche",
                                                "default": true
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "largeur_de_chaussee",
                                                "public_name": "largeur_de_chaussee",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nature_de_la_restriction",
                                                "public_name": "nature_de_la_restriction",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "cpx_numero_route_europeenne",
                                                "public_name": "cpx_numero_route_europeenne",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "reserve_aux_bus",
                                                "public_name": "reserve_aux_bus",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "matieres_dangereuses_interdites",
                                                "public_name": "matieres_dangereuses_interdites",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_largeur",
                                                "public_name": "restriction_de_largeur",
                                                "default": false
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "nom_1_droite",
                                                "public_name": "nom_1_droite",
                                                "default": true
                                            },
                                            {
                                                "table_name": "ways",
                                                "native_name": "restriction_de_longueur",
                                                "public_name": "restriction_de_longueur",
                                                "default": false
                                            }
                                        ],
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_pgr + ''')]}"
                                    }
                                ],
                                "constraints": {
                                    "defaultPreferredCostRatio": 0.8,
                                    "defaultAvoidCostRatio": 1.2,
                                    "values": [
                                        {
                                            "keyType": "name-pgr",
                                            "key": "wayType",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "availableValues": [
                                                {
                                                    "value": "autoroute",
                                                    "field": "acces_vehicule_leger",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$A péage$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "tunnel",
                                                    "field": "position_par_rapport_au_sol",
                                                    "condition": {
                                                        "type": "less",
                                                        "value": "0"
                                                    }
                                                },
                                                {
                                                    "value": "pont",
                                                    "field": "position_par_rapport_au_sol",
                                                    "condition": {
                                                        "type": "greater",
                                                        "value": "0"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "keyType": "numerical-pgr",
                                            "key": "largeur_de_chaussee",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "field": "largeur_de_chaussee"
                                        },
                                        {
                                            "keyType": "numerical-pgr",
                                            "key": "importance",
                                            "availableConstraintType": [
                                                "banned",
                                                "prefer",
                                                "avoid"
                                            ],
                                            "field": "importance"
                                        },
                                        {
                                            "keyType": "name-pgr",
                                            "key": "nature",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "availableValues": [
                                                {
                                                    "value": "sentier",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Sentier$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "bac_ou_liaison_maritime",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Bac ou liaison maritime$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "bretelle",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Bretelle$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "chemin",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Chemin$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "escalier",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Escalier$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "piste_cyclable",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Piste cyclable$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "rond-point",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Rond-point$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "route_a_1_chaussee",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Route à 1 chaussée$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "route_a_2_chaussees",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Route à 2 chaussées$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "route_empierree",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Route empierrée$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "type_autoroutier",
                                                    "field": "nature",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Type autoroutier$niv4$"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "keyType": "numerical-pgr",
                                            "key": "restriction_de_hauteur",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "field": "restriction_de_hauteur"
                                        },
                                        {
                                            "keyType": "numerical-pgr",
                                            "key": "restriction_de_largeur",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "field": "restriction_de_largeur"
                                        },
                                        {
                                            "keyType": "numerical-pgr",
                                            "key": "restriction_de_poids_total",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "field": "restriction_de_poids_total"
                                        },
                                        {
                                            "keyType": "numerical-pgr",
                                            "key": "restriction_de_poids_par_essieu",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "field": "restriction_de_poids_par_essieu"
                                        },
                                        {
                                            "keyType": "name-pgr",
                                            "key": "matieres_dangereuses_interdites",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "availableValues": [
                                                {
                                                    "value": "vrai",
                                                    "field": "matieres_dangereuses_interdites",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "true"
                                                    }
                                                },
                                                {
                                                    "value": "faux",
                                                    "field": "matieres_dangereuses_interdites",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "false"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "keyType": "name-pgr",
                                            "key": "itineraire_vert",
                                            "availableConstraintType": [
                                                "banned",
                                                "prefer",
                                                "avoid"
                                            ],
                                            "availableValues": [
                                                {
                                                    "value": "vrai",
                                                    "field": "itineraire_vert",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "true"
                                                    }
                                                },
                                                {
                                                    "value": "faux",
                                                    "field": "itineraire_vert",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "false"
                                                    }
                                                }
                                            ]
                                        },
                                        {
                                            "keyType": "name-pgr",
                                            "key": "cpx_classement_administratif",
                                            "availableConstraintType": [
                                                "banned",
                                                "prefer",
                                                "avoid"
                                            ],
                                            "availableValues": [
                                                {
                                                    "value": "vide",
                                                    "field": "cpx_classement_administratif",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "autoroute",
                                                    "field": "cpx_classement_administratif",
                                                    "condition": {
                                                        "type": "like",
                                                        "value": "$niv4$%Autoroute%$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "nationale",
                                                    "field": "cpx_classement_administratif",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Nationale$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "departementale",
                                                    "field": "cpx_classement_administratif",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Départementale$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "voie_communale",
                                                    "field": "cpx_classement_administratif",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Voie communale$niv4$"
                                                    }
                                                },
                                                {
                                                    "value": "chemin_rural",
                                                    "field": "cpx_classement_administratif",
                                                    "condition": {
                                                        "type": "equal",
                                                        "value": "$niv4$Chemin rural$niv4$"
                                                    }
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        },
                        "comments": [
                            "Configuration d'un flux itinéraire pgr"
                        ]
                    }
                ],
                "parents": [
                    "pivot-road2-to-graph-db"
                ]
            },
            "publication-itineraire-pgr": {
                "actions": [
                    {
                        "type": "offering",
                        "url_parameters": {
                            "configuration": "{store_entity.configuration.infos._id [INFOS(name=''' + args.configuration_name_pgr + ''')]}"
                        },
                        "body_parameters": {
                            "endpoint": "{store_entity.endpoint.infos._id [INFOS(technical_name=gpf-road2)]}",
                            "visibility": "PUBLIC",
                            "open": true
                        }
                    }
                ],
                "parents": []
            },'''
    if ("pgrouting" in args.graph or "all" in args.graph) and args.update == "true" :
        text += '''
            "pivot-road2-to-graph-db": {
                "actions": [
                    {
                        "type": "processing-execution",
                        "body_parameters": {
                            "processing": "{store_entity.processing.infos._id [INFOS(name=pivot-road2-to-graph-db)]}",
                            "inputs": {
                                "stored_data": [
                                    "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_pivot + ''')]}"
                                ]
                            },
                            "output": {
                                "stored_data": {
                                    "id": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_pgr + ''')]}"
                                }
                            },
                            "parameters": {
                                "cost_calculations": [
                                    {
                                        "name": "CC_car",
                                        "variables": [
                                            {
                                                "name": "nature",
                                                "column_name": "nature",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "length_m",
                                                "column_name": "length_m",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "vitesse_voiture",
                                                "column_name": "vitesse_moyenne_vl",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "sens",
                                                "column_name": "direction",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "urbain",
                                                "column_name": "urbain",
                                                "mapping": {
                                                    "True": 5,
                                                    "False": 0
                                                }
                                            }
                                        ],
                                        "outputs": [
                                            {
                                                "name": "cost_m_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "distance",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ]
                                                ]
                                            },
                                            {
                                                "name": "cost_s_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "duration",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ],
                                                    [
                                                        "divide",
                                                        "vitesse_voiture"
                                                    ],
                                                    [
                                                        "multiply",
                                                        3.6
                                                    ],
                                                    [
                                                        "add",
                                                        "urbain"
                                                    ]
                                                ]
                                            },
                                            {
                                              "name": "cost_m_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "distance",
                                              "operations": [
                                                ["add", "length_m"]
                                              ]
                                            },
                                            {
                                              "name": "cost_s_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "duration",
                                              "operations": [
                                                ["add", "length_m"],
                                                ["multiply", 0.9]
                                              ]
                                            }
                                        ]
                                    }
                                ],
                                "costs": [
                                    {
                                        "profile": "car",
                                        "optimization": "fastest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "fastest",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "cost_calculation": "CC_car"
                                    }
                                ]
                            }
                        },
                        "comments": [
                            "Création d'un graph pgr'"
                        ]
                    }
                ],
                "parents": ["vector-db-to-pivot-road2"]
            },
            "synchronisation-offering-pgr": {
                "actions": [
                    {
                        "type": "synchronize-offering",
                        "filter_infos": {"configuration" : "{store_entity.configuration.infos._id [INFOS(stored_data={store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_pgr + ''')]})]}"}
                    }
                ],
                "parents": []
            },'''
    if ("osrm" in args.graph or "all" in args.graph) and args.update == "false" :
        text += '''
            "pivot-road2-to-graph-osrm": {
                "actions": [
                    {
                        "type": "processing-execution",
                        "body_parameters": {
                            "processing": "{store_entity.processing.infos._id [INFOS(name=pivot-road2-to-graph-osrm)]}",
                            "inputs": {
                                "stored_data": [
                                    "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_pivot + ''')]}"
                                ]
                            },
                            "output": {
                                "stored_data": {
                                    "name": "''' + args.stored_data_graph_osrm + '''",
                                    "storage_tags": ["OTHERS","PERF"]
                                }
                            },
                            "parameters": {
                                "cost_calculations": [
                                    {
                                        "name": "CC_car",
                                        "variables": [
                                            {
                                                "name": "nature",
                                                "column_name": "nature",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "length_m",
                                                "column_name": "length_m",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "vitesse_voiture",
                                                "column_name": "vitesse_moyenne_vl",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "sens",
                                                "column_name": "direction",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "urbain",
                                                "column_name": "urbain",
                                                "mapping": {
                                                    "True": 5,
                                                    "False": 0
                                                }
                                            }
                                        ],
                                        "outputs": [
                                            {
                                                "name": "cost_m_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "distance",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ]
                                                ]
                                            },
                                            {
                                                "name": "cost_s_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "duration",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ],
                                                    [
                                                        "divide",
                                                        "vitesse_voiture"
                                                    ],
                                                    [
                                                        "multiply",
                                                        3.6
                                                    ],
                                                    [
                                                        "add",
                                                        "urbain"
                                                    ]
                                                ]
                                            },
                                            {
                                              "name": "cost_s_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "duration",
                                              "operations": [
                                                ["add", "length_m"],
                                                ["multiply", 0.9]
                                              ]
                                            }
                                        ]
                                    }
                                ],
                                "costs": [
                                    {
                                        "profile": "car",
                                        "optimization": "fastest",
                                        "name" : "cost_m_car",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "name" : "cost_s_car",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "name" : "cost_s_pedestrian",
                                        "cost_calculation": "CC_car"
                                    }
                                ]
                            }
                        },
                        "comments": [
                            "Création d'un graph OSRM"
                        ]
                    }
                ],
                "parents": ["vector-db-to-pivot-road2"]
            },
            "configuration-iti-osrm": {
                "actions": [
                    {
                        "type": "configuration",
                        "body_parameters": {
                            "type": "ITINERARY-ISOCURVE",
                            "name": "''' + args.configuration_name_osrm + '''",
                            "layer_name": "''' + args.configuration_layer_name_osrm + '''",
                            "type_infos": {
                                "title": "itineraire_osrm",
                                "abstract": "Publication du service Itinéraire via OSRM",
                                "keywords": ["osrm", "itineraire", "publication"],
                                "used_data": [
                                    {
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_osrm + ''')]}",
                                        "profile": "car",
                                        "optimization": "fastest"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_osrm + ''')]}"
                                    },
                                    {
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "stored_data": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_osrm + ''')]}"
                                    }
                                ],
                                "constraints": {
                                    "defaultPreferredCostRatio": 0.8,
                                    "defaultAvoidCostRatio": 1.2,
                                    "values": [
                                        {
                                            "keyType": "name-osrm",
                                            "key": "wayType",
                                            "availableConstraintType": [
                                                "banned"
                                            ],
                                            "availableValues": [
                                                {
                                                    "value": "autoroute",
                                                    "field": "toll"
                                                },
                                                {
                                                    "value": "tunnel",
                                                    "field": "tunnel"
                                                },
                                                {
                                                    "value": "pont",
                                                    "field": "bridge"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        },
                        "comments": [
                            "Configuration d'un flux itinéraire osrm"
                        ]
                    }
                ],
                "parents": [
                    "pivot-road2-to-graph-osrm"
                ]
            },
            "publication-itineraire-osrm": {
                "actions": [
                    {
                        "type": "offering",
                        "url_parameters": {
                            "configuration": "{store_entity.configuration.infos._id [INFOS(name=''' + args.configuration_name_osrm + ''')]}"
                        },
                        "body_parameters": {
                            "endpoint": "{store_entity.endpoint.infos._id [INFOS(technical_name=gpf-road2)]}",
                            "visibility": "PUBLIC",
                            "open": true
                        }
                    }
                ],
                "parents": [
                    "configuration-iti-osrm"
                ]
            },'''
    if ("osrm" in args.graph or "all" in args.graph) and args.update == "true" :
        text += '''
            "pivot-road2-to-graph-osrm": {
                "actions": [
                    {
                        "type": "processing-execution",
                        "body_parameters": {
                            "processing": "{store_entity.processing.infos._id [INFOS(name=pivot-road2-to-graph-osrm)]}",
                            "inputs": {
                                "stored_data": [
                                    "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_pivot + ''')]}"
                                ]
                            },
                            "output": {
                                "stored_data": {
                                    "id": "{store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_osrm + ''')]}"
                                }
                            },
                            "parameters": {
                                "cost_calculations": [
                                    {
                                        "name": "CC_car",
                                        "variables": [
                                            {
                                                "name": "nature",
                                                "column_name": "nature",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "length_m",
                                                "column_name": "length_m",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "vitesse_voiture",
                                                "column_name": "vitesse_moyenne_vl",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "sens",
                                                "column_name": "direction",
                                                "mapping": "value"
                                            },
                                            {
                                                "name": "urbain",
                                                "column_name": "urbain",
                                                "mapping": {
                                                    "True": 5,
                                                    "False": 0
                                                }
                                            }
                                        ],
                                        "outputs": [
                                            {
                                                "name": "cost_m_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "distance",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ]
                                                ]
                                            },
                                            {
                                                "name": "cost_s_car",
                                                "speed_value": "vitesse_voiture",
                                                "direct_conditions": "sens>=0;vitesse_voiture>0",
                                                "reverse_conditions": "sens<=0;vitesse_voiture>0",
                                                "turn_restrictions": true,
                                                "cost_type": "duration",
                                                "operations": [
                                                    [
                                                        "add",
                                                        "length_m"
                                                    ],
                                                    [
                                                        "divide",
                                                        "vitesse_voiture"
                                                    ],
                                                    [
                                                        "multiply",
                                                        3.6
                                                    ],
                                                    [
                                                        "add",
                                                        "urbain"
                                                    ]
                                                ]
                                            },
                                            {
                                              "name": "cost_s_pedestrian",
                                              "speed_value": 4,
                                              "direct_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "reverse_conditions" : "nature~='Type autoroutier';nature~='Bretelle'",
                                              "turn_restrictions": false,
                                              "cost_type": "duration",
                                              "operations": [
                                                ["add", "length_m"],
                                                ["multiply", 0.9]
                                              ]
                                            }
                                        ]
                                    }
                                ],
                                "costs": [
                                    {
                                        "profile": "car",
                                        "optimization": "fastest",
                                        "name" : "cost_m_car",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "car",
                                        "optimization": "shortest",
                                        "name" : "cost_s_car",
                                        "cost_calculation": "CC_car"
                                    },
                                    {
                                        "profile": "pedestrian",
                                        "optimization": "shortest",
                                        "name" : "cost_s_pedestrian",
                                        "cost_calculation": "CC_car"
                                    }
                                ]
                            }
                        },
                        "comments": [
                            "Création d'un graph OSRM"
                        ]
                    }
                ],
                "parents": ["vector-db-to-pivot-road2"]
            },
            "synchronisation-offering-osrm": {
                "actions": [
                    {
                        "type": "synchronize-offering",
                        "filter_infos": {"configuration" : "{store_entity.configuration.infos._id [INFOS(stored_data={store_entity.stored_data.infos._id [INFOS(name=''' + args.stored_data_graph_osrm + ''')]})]}"}
                    }
                ],
                "parents": [
                ]
            },'''
    text = text[:-1]
    text += """
        }
    }
}"""
    return text

def save_workflow(args, workflow) -> None:
    """Save the workflow in a file
    """
    with open(args.path_file,"w") as file:
        file.write(workflow)

def run_workflow(args) -> None:
    """Run the workflow
    """
    if args.upload is not None :
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s mise-en-base")

    os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s vector-db-to-pivot-road2")

    if ("valhalla" in args.graph or "all" in args.graph) and args.update == "false" :
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s pivot-road2-to-graph-valhalla")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s configuration-iti-valhalla")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s publication-itineraire-valhalla")
    
    if ("valhalla" in args.graph or "all" in args.graph) and args.update == "true" :
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s pivot-road2-to-graph-valhalla")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s synchronisation-offering-valhalla --behavior delete")

    if ("pgrouting" in args.graph or "all" in args.graph) and args.update == "false" :
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s pivot-road2-to-graph-db")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s configuration-iti-pgr")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s publication-itineraire-pgr")

    if ("pgrouting" in args.graph or "all" in args.graph) and args.update == "true" :
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s pivot-road2-to-graph-db")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s synchronisation-offering-pgr --behavior delete")

    if ("osrm" in args.graph or "all" in args.graph) and args.update == "false" :
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s pivot-road2-to-graph-osrm")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s configuration-iti-osrm")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s publication-itineraire-osrm")

    if ("osrm" in args.graph or "all" in args.graph) and args.update == "true" :
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s pivot-road2-to-graph-osrm")
        os.system("python3 -m sdk_entrepot_gpf --ini " + str(args.config) + " workflow -f " + str(args.path_file) + " -s synchronisation-offering-osrm --behavior delete")


def main() -> None:
    """Main function

    Return 0 if success, 1 if an error occured
    """

    parse()

    workflow = creation_workflow(args)

    save_workflow(args, workflow)

    if args.run == "true" :
        run_workflow(args)

    sys.exit(0)

if __name__ == "__main__":
    main()