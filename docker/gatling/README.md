#Gatling Docker Image

![Gatling Logo](http://gatling.io/assets/images/img1.png)

# Gatling on CentOS 6

This image contains Gatling 2.0.0M3 running on CentOS 6 base image 
Default Java is Java 8

## Start Container 

### Interactive mode
    docker run -t -i hgomez/gatling

Then you could use Gatling 

    [root@5992fdbc4461 /]# gatling.sh --help
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

    [root@5992fdbc4461 /]# java -version
    java version "1.8.0_25"
    Java(TM) SE Runtime Environment (build 1.8.0_25-b17)
    Java HotSpot(TM) 64-Bit Server VM (build 25.25-b02, mixed mode)
    [root@5992fdbc4461 /]# 

