import os

from pyspark.sql import SparkSession


base_path = '/nfs/turbo/midas-applied-ds/'
raw_data_path_ext = 'Data/Raw/VED/'
raw_data_path = os.path.join(base_path, raw_data_path_ext)

spark = SparkSession.builder \
		.master('local') \
		.appName('READS') \
		.getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

timeseries = spark.read.option('header', True).csv('/nfs/turbo/midas-applied-ds/Data/Raw/VED/VED_*.csv')
print(timeseries.count())
timeseries.show(n=3)

static = spark.read \
	      .option('header', True) \
	      .csv('/nfs/turbo/midas-applied-ds/Data/Processed/VED*.csv')

print(static.count())
static.show(n=3)
