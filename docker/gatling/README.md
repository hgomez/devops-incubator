#Gatling Docker Image

![Gatling Logo](http://gatling.io/assets/images/img1.png)

# Gatling on CentOS 6

This image contains Gatling 2.0.3 running on CentOS 6 base image and using Java 8u25

## Start Container 

### Direct interactive mode
    docker run -i -t hgomez/gatling -h

    GATLING_HOME is set to /opt/gatling

    Usage: gatling [options] 

      -h | --help
	    Show help (this message) and exit
      -nr | --no-reports
	    Runs simulation but does not generate reports
      -ro <directoryName> | --reports-only <directoryName>
	    Generates the reports for the simulation in <directoryName>
      -df <directoryPath> | --data-folder <directoryPath>
	    Uses <directoryPath> as the absolute path of the directory where feeders are stored
      -rf <directoryPath> | --results-folder <directoryPath>
	    Uses <directoryPath> as the absolute path of the directory where results are stored
      -bf <directoryPath> | --request-bodies-folder <directoryPath>
	    Uses <directoryPath> as the absolute path of the directory where request bodies are stored
      -sf <directoryPath> | --simulations-folder <directoryPath>
	    Uses <directoryPath> to discover simulations that could be run
      -sbf <directoryPath> | --simulations-binaries-folder <directoryPath>
	    Uses <directoryPath> to discover already compiled simulations
      -s <className> | --simulation <className>
	    Runs <className> simulation
      -on <name> | --output-name <name>
	    Use <name> for the base name of the output directory
      -sd <description> | --simulation-description <description>
	    A short <description> of the run to include in the report

### Use Volumes

You could overrides default directories to use dirs in host filesystem :

    mkdir -p /home/henri/gatling/conf
    mkdir -p /home/henri/gatling/results
    mkdir -p /home/henri/gatling/user-files

    docker run -i -t -v /home/henri/gatling/conf:/opt/gatling/conf \
                     -v /home/henri/gatling/results:/opt/gatling/results \
                     -v /home/henri/gatling/user-files:/opt/gatling/user-files hgomez/gatling


