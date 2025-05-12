# Data Engineering Task
## Data Overview
string -> ShipmentID,Origin,OriginCountry,OriginRegion,Destination,DestinationCountry,DestinationRegion,PackageID

float -> Weight,Cost

datetime -> EventTime

## Tasks
* Study the files carefully to understand the data you are working with
* Write a script/program that will parse the CSV files and generate a new report that will, for every shipment, contain the shipment's origin, destination, total number of packages, the total time it took the shipment to arrive at its destination, the total weight of the shipment, and the total cost of the shipment
  * Weight values are all in grams and do not need to be changed/converted
  * The final currency of the report should be in USD. Assume the currency of the "cost" column works like this:
    * If the origin and destination countries are the same, then it's that country's currency
    * If the origin and destination countries are different, it's the destination country's currency
    * Use the current currency conversation rates (bonus points, however, if you can align them to match the times in which the actual shipment occurred!)
* Visualize the number of shipments that go into the US (from non-US locations) and leave the US (to non-US locations) for each month that the sample data covers
* Write a script/program that will use the provided data to infer the route a shipment from Los Angeles would take to reach Doncaster
  * The only thing used by the script must be the CSV files; the output MUST display the route to be taken (any format – can even be output to the console)