#!/usr/env/bin python

# run:
# spark-submit --master yarn --num-executors 50 --executor-memory 5g --executor-cores 5 --driver-memory 3g ./spark_sample_data.py

def main():
    from pyspark import SparkConf, SparkContext
    sc = SparkContext("", "sample_task")

    # api ref: http://spark.apache.org/docs/1.6.2/api/python/pyspark.html?highlight=sample#pyspark.RDD.sample
    rawRDD = sc.textFile("hdfs://m1-baidu-hdfs:8020/home/work/data/live/")
    sampledRDD = rawRDD.sample(False, 0.03, 2342345)
    sampledRDD.saveAsTextFile("hdfs://m1-baidu-hdfs:8020/home/work/data/sampled")

    #cnt = rawRDD.count()
    #print("line number: ")
    #print(cnt)

if __name__ == '__main__':
    main()
