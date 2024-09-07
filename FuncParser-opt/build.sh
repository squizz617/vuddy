#!/bin/bash

set -o errexit

SOURCE_DIR='src'
BUILD_DIR='build'
JAR_DIR='jar'
ANTLR_JAR='antlr-4.7.1-complete.jar'
RESULT_JAR='FuncParser-471.jar'

rm -rf ${RESULT_JAR}
rm -rf ${BUILD_DIR}
mkdir ${BUILD_DIR}

# Copy source files to build dir
cp ./${SOURCE_DIR}/*.g4 ${BUILD_DIR}
cp ./${SOURCE_DIR}/*.java ${BUILD_DIR}
cp ./manifest.mf ${BUILD_DIR}
cp ./${JAR_DIR}/$ANTLR_JAR ${BUILD_DIR}

cd ${BUILD_DIR}

# Generate Lexer and Parser from Grammar

java -cp ./${ANTLR_JAR} org.antlr.v4.Tool Module.g4 Function.g4

# Compile java-files
#javac -cp ./${ANTLR_JAR_1} ./*.java -Xlint:unchecked
javac -cp ./${ANTLR_JAR} ./*.java -Xlint:deprecation

# unpack ANTLR-jar since we need some of the class files
jar xf ./${ANTLR_JAR}

# Create ${RESULT_JAR}
#jar cvfm ${RESULT_JAR} manifest.mf *.class org > /dev/null
jar cvfm ${RESULT_JAR} ../manifest.mf ./*.class org > out
cp ${RESULT_JAR} ../
