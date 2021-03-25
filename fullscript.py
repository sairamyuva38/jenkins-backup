import subprocess as sp
import os.path
import sys
import boto3
import botocore
import glob

#convert directory into zip file
jenkinsbkpdir = '/apps/backup-jenkins'
dirtobkp = []

dirtbkp = "ls -d {0}/FULL-*"
dirtobkp = sp.getoutput(dirtbkp.format(jenkinsbkpdir)).split("\n")

if os.path.isdir(jenkinsbkpdir):
        print("--- archiving {0} dir ---".format(dirtobkp))

fulldatepart = []
full = []
fulldate = []

for x in dirtobkp:
    fulldatepart = x.split("-")
    print(fulldatepart)
    full = '-'.join(fulldatepart[2:])
    fulldate.append(full)


bkpzipfile = []

for x in fulldate:
    bkpcmd = "BACKUPSET_{0}_.zip"
    bkp = bkpcmd.format(x)
    bkpzipfile.append(bkp)

bkpfileloc = []

for x in bkpzipfile:
    bkpfile = jenkinsbkpdir + "/" + x
    bkpfileloc.append(bkpfile)

for x in bkpfileloc:
    for y in dirtobkp:
        sp.getoutput("sudo zip -r {0} {1}".format(x,y))

#push the zip file into s3
sp.getoutput("/snap/bin/aws s3 cp {0} s3://ad-jenkins-backup --recursive --exclude 'FULL*' ".format(jenkinsbkpdir))

print(bkpfileloc)
for x in bkpfileloc:
    sp.getoutput("rm -rvf {0}".format(x))


l1=[]
s3_resource=boto3.client("s3")
objects=s3_resource.list_objects(Bucket="ad-jenkins-backup")["Contents"]
a =len(objects)
#print(a)
if a > 6:
    p = int(a)-6
    #print(p)
    for x in range(p):
        l1.append(objects[x])
#print(l1)

for x in l1:
    if x in objects:
        s3_resource.delete_object(Bucket='ad-jenkins-backup',Key=x["Key"])


