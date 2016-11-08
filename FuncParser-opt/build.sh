#!/bin/bash

set -o errexit

SOURCE_DIR='src'
BUILD_DIR='build'
JAR_DIR='jar'
#ANTLR_JAR='antlr-4.5.3-complete.jar'

ANTLR_JAR_1='antlr4-4.5.3.jar'
ANTLR_JAR_2='antlr4-runtime-4.5.3.jar'
ANTLR_JAR_3='antlr4-annotations-4.5.3.jar'
ANTLR_JAR_4='ST4-4.0.8.jar'
ANTLR_JAR_5='antlr-runtime-3.5.2.jar'

RESULT_JAR='FuncParser-opt.jar'

rm -rf ${RESULT_JAR}
rm -rf ${BUILD_DIR}
mkdir ${BUILD_DIR}

# Copy source files to build dir
cp ./${SOURCE_DIR}/*.g4 ${BUILD_DIR}
cp ./${SOURCE_DIR}/*.java ${BUILD_DIR}
cp ./manifest.mf ${BUILD_DIR}
#cp $ANTLR_JAR ${BUILD_DIR}
cp ./${JAR_DIR}/$ANTLR_JAR_1 ${BUILD_DIR}
cp ./${JAR_DIR}/$ANTLR_JAR_2 ${BUILD_DIR}
cp ./${JAR_DIR}/$ANTLR_JAR_3 ${BUILD_DIR}
cp ./${JAR_DIR}/$ANTLR_JAR_4 ${BUILD_DIR}
cp ./${JAR_DIR}/$ANTLR_JAR_5 ${BUILD_DIR}

cd ${BUILD_DIR}

# Generate Lexer and Parser from Grammar

#java -jar ../${ANTLR_JAR} CPPGrammar.g
#java -cp ${ANTLR_JAR_1} org.antlr.v4.Tool Module.g4 Function.g4
#java -cp ${ANTLR_JAR_1} org.antlr.v4.Tool Module.g4 Function.g4
java -cp ./${ANTLR_JAR_1}:./${ANTLR_JAR_2}:./${ANTLR_JAR_3}:./${ANTLR_JAR_4}:./${ANTLR_JAR_5} org.antlr.v4.Tool Module.g4 Function.g4

# Compile java-files
#javac -cp ./${ANTLR_JAR_1} ./*.java -Xlint:unchecked
javac -cp ./${ANTLR_JAR_1}:./${ANTLR_JAR_2}:./${ANTLR_JAR_3}:./${ANTLR_JAR_4}:./${ANTLR_JAR_5} ./*.java -Xlint:unchecked

# unpack ANTLR-jar since we need some of the class files
#jar xf ./${ANTLR_JAR_1}
jar xf ./${ANTLR_JAR_1}
jar xf ./${ANTLR_JAR_2}
jar xf ./${ANTLR_JAR_3}
jar xf ./${ANTLR_JAR_4}
jar xf ./${ANTLR_JAR_5}

# Create CodeSensor.jar
#jar cvfm ${RESULT_JAR} manifest.mf *.class org > /dev/null
jar cvfm ${RESULT_JAR} ../manifest.mf ./*.class org > out
cp ${RESULT_JAR} ../
