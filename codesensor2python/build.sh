#!/bin/bash

SOURCE_DIR='src'
BUILD_DIR='build'
ANTLR_JAR='antlr-4.5.3-complete.jar'
#RESULT_JAR='CodeSensor2.jar'

#rm -rf ${RESULT_JAR}
rm -rf ${BUILD_DIR}
mkdir ${BUILD_DIR}
rm -rf "__init__.pyc"

# Copy source files to build dir

cp ./${SOURCE_DIR}/*.g4 ${BUILD_DIR}
cp ./${SOURCE_DIR}/*.py ${BUILD_DIR}
#cp ./manifest.mf ${BUILD_DIR}
#cp $ANTLR_JAR ${BUILD_DIR}

cd ${BUILD_DIR}

# Generate Lexer and Parser from Grammar

#java -jar ../${ANTLR_JAR} CPPGrammar.g
java -cp ../${ANTLR_JAR} org.antlr.v4.Tool -Dlanguage=Python2 Module.g4

# Compile java-files
#javac -cp ./${ANTLR_JAR} ./*.java -Xlint:unchecked
##javac -cp ./${ANTLR_JAR} ./*.java

# unpack ANTLR-jar since we need some of the class files

##jar xf ./${ANTLR_JAR}

# Create CodeSensor.jar
##jar cvfm ${RESULT_JAR} manifest.mf *.class org > /dev/null
##cp ${RESULT_JAR} ../
