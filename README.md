# MetadataExtractor
Extract image metadata and write it to a JSON file
## To extract image metadata use the following commands in the terminal:
``` 
cd metadata_extractor/
python image_metadata_extractor.py -i input1.jpg input2.jpeg -o output_dir

```
## The `docker-compose.yml` file includes two services, app-dev and app-prod, for development and production respectively. Both services use the Dockerfile and mount the images and output directories as volumes.

To run the docker-compose.yml file use the following command:

```
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
