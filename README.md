# Analyzing twitter data using Hadoop streaming and Python (foler A2)
In this task, we will analyze a dataset of ~5.000.000 Twitter tweets collected using Twitters datastream API. The total size of the dataset is still a modest ~9GB uncompressed.

Each tweet is a JSON document http://en.wikipedia.org/wiki/JSON. JSON is one of the standard Markup formats used on the Web. For the specific case of Twitter tweets, you can read about the possible fields in the documents here: https://dev.twitter.com/overview/api/tweets

This particular Twitter dataset was collected by filtering the stream of tweets to store those containing the Swedish pronouns “han”, “hon”, “den”, “det”, “denna”, “denne”, and the gender neutral pronoun “hen”. 

We are going to count the number of original tweets which have these pronouns (**case insensitive**) and the exact number of times the pronouns occur

## Getting Started
1. Download Hadoop and set it up on a VM or local machine (I will be using a VM with Ubuntu Server)
2. [Download dataset](https://data-engineering-dna072.s3.eu-west-1.amazonaws.com/tweets.tar.gz)

3. Write mapper and reducer function in Python

4. Apply MapReduce on the dataset

### Setting up Hadoop (Assuming a virtual machine running Ubuntu 22.04)
1. You need to set the hostname of your instance in /etc/hosts. Print the hostname for your instance with the hostname command. Open the file (you need to be sudo to edit) and modify the first line: 127.0.0.1 localhost <your hostname>
Tip: use the nano editor.
2. Run `apt update`, and install the packages: `openjdk-11-jdk-headless net-tools`
3. The JAVA_HOME environment variable is used by applications like Hadoop to find the Java installation folder. We need to set this variable. To apply it in future restarts, add this line to /etc/environment `JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/`. And, to apply the environment variable for this shell session without rebooting: `export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/`
4. Use wget to download the .tar.gz binary release of version 3.3.4 of Hadoop. (not “aarch64”). Find the download link on the Hadoop website. Use the tar command to extract the archive directly into your home directory.
5. Verify we can query the Hadoop version without error: `./hadoop-3.3.4/bin/hadoop version`
6. (Optional) Add `./hadoop-3.3.4/bin` to your `$PATH` by editing `~/.bashrc` and adding this line `export PATH="[path]/hadoop-3.3.4/bin:$PATH"`. Replace `[path]` with the directory that contains your `hadoop-3.3.4` folder. For my case it's `/home/ubuntu` so my full export will be `export PATH="/home/ubuntu/hadoop-3.3.4/bin:$PATH"`. 
7. (Optional) After following step 6, run `source ~/.bashrc` for the environment variable updates to take effect. You can also logout and log back in.

#### Setup Hadoop in Psuedo Distributed mode
1. Add this configuration to `./hadoop-3.3.4/etc/hadoop/core-site.xml`
```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```
2. Add this configuration to `./hadoop-3.3.4/etc/hadoop/hdfs-site.xml`
```
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```
3. Serve both `DataNode` and `NameNode` with this commands
```
./hadoop-3.3.4/bin/hdfs --daemon start namenode
./hadoop-3.3.4/bin/hdfs --daemon start datanode
```
4. Verify that the daemons are running by using command `jps`. You should see a similar output
```
$ jps
17922 NameNode
18047 DataNode
18383 Jps
```

5. Make the HDFS directories required to execute MapReduce jobs:
```
  $ bin/hdfs dfs -mkdir /user
  $ bin/hdfs dfs -mkdir /user/ubuntu
```

### Dowload dataset
1. Create a directory **/twitter** in your user directory with `mkdir twitter` 
2. Run this command `wget https://data-engineering-dna072.s3.eu-west-1.amazonaws.com/tweets.tar.gz` to download this dataset.
4. Uncompress into the new directory `tar -xvf tweets.tar.gz --directory ./twitter`

### Create mapper.py
Clone this repo to get the `mapper.py` or simply create a file `mapper.py` and paste the contents of the same file from this repo there.

### Create reducer.py
Follow the same instructions as above for reducer

### Copy twitter dataset files from local file system to Hadoop Distributed File System
1. Run `./hadoop-3.3.4/bin/hdfs dfs -copyFromLocal ./twitter `
2. Confirm your dfs has the appropriate files by running `./hadoop-3.3.4/bin/hdfs dfs -ls`

### Run the MapReduce Job
Use this command to run the map-reduce job 
```
hadoop jar /home/ubuntu/hadoop-3.3.4/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar -file /home/ubuntu/twitter/mapper.py -mapper mapper.py -file /home/ubuntu/twitter/reducer.py -reducer reducer.py -input /user/ubuntu/twitter/* -output /user/ubuntu/twitter/twitter-output
```

### View output
Run this command to view the output
```
hdfs dfs -cat /user/ubuntu/twitter/twitter-output/part-00000
```
You should get this output 
```
-   2193698
den 1324057
denna	22716
denne	4015
det	532906
han	778945
hen	34419
hon	363764
```
Happy coding 😊






