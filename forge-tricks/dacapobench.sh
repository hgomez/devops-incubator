#!/bin/sh
#
# Purpose : launch dacapo benchmarks
#

if [ ! -z "$WORKSPACE" ]; then
  BASE_DIR=$WORKSPACE
else
  BASE_DIR=`dirname $0`
fi

if [ ! -f $BASE_DIR/dacapo-9.12-bach.jar ]; then
  echo "Downloading dacapo-9.12 bench..."
  curl -L http://downloads.sourceforge.net/project/dacapobench/9.12-bach/dacapo-9.12-bach.jar -o $BASE_DIR/dacapo-9.12-bach.jar
fi


benchme() {
  local COUNT=$1
  local BENCH=$2

  rm -f dacapo-bench-$BENCH.log
#  echo "benching dacapo-9.12 - $BENCH - $COUNT iterations at `date`"
  java $JAVA_OPTS -jar $BASE_DIR/dacapo-9.12-bach.jar -n $COUNT $BENCH >>dacapo-bench-$BENCH.log 2>&1
  cat dacapo-bench-$BENCH.log | grep PASSED
}

benchme 10 avrora
benchme  2 eclipse
benchme 10 fop
benchme  2 h2
benchme  2 jython
benchme 10 luindex
benchme 10 lusearch
benchme  5 pmd
benchme 10 sunflow
benchme  5 tomcat
benchme  5 tradebeans
benchme  5 tradesoap
benchme 10 xalan
