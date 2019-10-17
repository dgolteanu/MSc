#!/usr/bin/Rscript
library(affxparser)
files<- list.files(path='./', pattern='_SNP.chp')
colname<-vector()
genotyping<-vector()
 for (i in files) {
  name<-gsub("*_SNP.chp","",toString(i))
  lists<-assign(name,readChp(i))
  genotype<-cbind(lists$Genotype$Call)
  colname<-append(colname,name)
  genotyping<- cbind(genotyping,genotype)}
colnames(genotyping)=colname
row.names(genotyping)=lists$Genotype$ProbeNames
write.csv(genotyping,file="calls.csv", row.names=T)
 #should add function to check if variables are empty
