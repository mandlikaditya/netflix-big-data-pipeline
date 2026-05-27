#!/bin/bash
# 01_hdfs_ingestion.sh
# Milestone 2: Data Ingestion to Hadoop HDFS
# Author: Fnu Mandakini

# Define paths
LOCAL_FILE="data/raw/netflix_titles.csv"
HDFS_RAW_DIR="/user/hadoop/data/"
HDFS_PROCESSED_DIR="/user/hadoop/netflix_processed/"

echo "Starting HDFS Ingestion Process..."

# Create necessary HDFS directories
hdfs dfs -mkdir -p $HDFS_RAW_DIR
hdfs dfs -mkdir -p $HDFS_PROCESSED_DIR

# Put the raw Netflix dataset into HDFS
hdfs dfs -put $LOCAL_FILE ${HDFS_RAW_DIR}netflix_titles.csv

# Verify ingestion
hdfs dfs -ls $HDFS_RAW_DIR

echo "Data successfully ingested into HDFS."
