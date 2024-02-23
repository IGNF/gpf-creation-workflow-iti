# gpf-creation-workflow-iti
Tool to create a workflow itinerary. For use this tool, you need to install the "SDK Python pour la géoplateforme" (https://github.com/Geoplateforme/sdk-entrepot) :

```
python3 -m pip install "sdk_entrepot_gpf>=0.1.21"
```

An example of a file config.ini to complete to use the SDK.

## create_workflow.py

Tool to create a workflow itinerary with the possibility to run it immediately

```
options:
  -h, --help            show this help message and exit
  --upload bd_topo_upload
                        Upload's name (in case of the creation of an upload)
  --stored_data_database bd_topo_v1
                        Name of the stored data with the vector data (to create in case of the creation of an upload)
  --stored_data_pivot pivot
                        Name of the pivot
  --graph [{osrm,pgrouting,valhalla,all} ...]
                        Types of graph you want to create
  --update {true,false}
                        true if you want to update existent stored data
  --stored_data_graph_valhalla graph_valhalla
                        Name of the graph valhalla (only for --graph=valhalla or all)
  --configuration_name_valhalla Service itinéraire Valhalla
                        Name of the configuration valhalla (only for --graph=valhalla or all and --update=false)
  --configuration_layer_name_valhalla bdtopo-valhalla
                        Layer Name of the configuration valhalla (only for --graph=valhalla or all and --update=false)
  --stored_data_graph_pgr graph_pgr
                        Name of the graph pgRouting (only for --graph=pgrouting or all)
  --configuration_name_pgr Service itinéraire pgRouting
                        Name of the configuration pgRouting (only for --graph=pgrouting or all and --update=false)
  --configuration_layer_name_pgr bdtopo-pgr
                        Layer Name of the configuration pgRouting (only for --graph=pgrouting or all and --update=false)
  --stored_data_graph_osrm graph_osrm
                        Name of the graph OSRM (only for --graph=osrm or all)
  --configuration_name_osrm Service itinéraire OSRM
                        Name of the configuration OSRM (only for --graph=osrm or all and --update=false)
  --configuration_layer_name_osrm bdtopo-osrm
                        Layer Name of the configuration OSRM (only for --graph=osrm or all and --update=false)
  --path_file /path/to/file/to/create
                        Path to save the workflow
  --config config.ini   Path to the config file
  --run {true,false}    true if you want to run the workflow after his creation
  ```

To run the command use :

```
python3 create_workflow.py [--options]
```

## run_workflow.py

Run a workflow automatically with the option --behavior delete (tke workflow need to not have commentary inside)

```
options:
  -h, --help            show this help message and exit
  --path_file /path/to/file/to/create
                        Path to save the workflow
  --config config.ini   Path to the config file
```

To run the command use :

```
python3 run_workflow.py [--options]
```