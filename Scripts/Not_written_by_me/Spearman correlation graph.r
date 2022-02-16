### libraries ###
library(readxl)
library(tidyverse)  
library(cluster)    
library(factoextra)
library(hexbin)
library(ggrepel)
### end of libraries ###

##########################
### auxiliary functions ##
##########################

correlation.groups.f <- function(data_g1,data_g2,comparison_label, x_label, y_label,out_dir,plot_file_name,pc,kmer){
  
  mean_counts_g1 <- apply(data_g1[,-1],1,function(x){mean(as.numeric(x))})
  mean_counts_g2 <- apply(data_g2[,-1],1,function(x){mean(as.numeric(x))})
  
  #mean_counts_g1 <- apply(data_g1[,-1],1,function(x){median(as.numeric(x))})
  #mean_counts_g2 <- apply(data_g2[,-1],1,function(x){median(as.numeric(x))})
  
  cor_test <- cor.test(x = mean_counts_g1,y=mean_counts_g2, method= "spearman")
  cor_test_rho <- cor_test$estimate
  cor_test_pvalue <- cor_test$p.value
  
  if(cor_test_pvalue < 1e-05){
    plot_title <- paste0(comparison_label," rho=",round(cor_test_rho,2),", p < 1e-05")}else{
      plot_title <- paste0(comparison_label," rho=",round(cor_test_rho,2),", p=",round(cor_test$p.value,5))  
    }
  
  # pdf(file=paste0(out_dir,plot_file_name,".pdf"))
  # plot(mean_counts_g1,mean_counts_g2,main=plot_title,
  #      ylab=x_label,xlab=y_label,
  #      col= "blue", pch = 21, cex.main = 1, 
  #      ylim= c(min(mean_counts_g2),max(mean_counts_g2)+200),xlim=c(min(mean_counts_g1),max(mean_counts_g1)))
  #      text(mean_counts_g1[ind_plot],mean_counts_g2[ind_plot],labels=sequences[ind_plot], cex= 0.7, pos=3)
  # dev.off()
  
  q1_g1 <- quantile(mean_counts_g1,(1-pc)/2)
  q1_g2 <- quantile(mean_counts_g2,(1-pc)/2)
  
  #q1_g1 <- round(quantile(mean_counts_g1,(1-pc)/2))
  #q1_g2 <- round(quantile(mean_counts_g2,(1-pc)/2))
  
  q2_g1 <- quantile(mean_counts_g1,(pc + (1-pc)/2))
  q2_g2 <- quantile(mean_counts_g2,(pc+ (1-pc)/2))
  
  #q2_g1 <- round(quantile(mean_counts_g1,(pc + (1-pc)/2)))
  #q2_g2 <- round(quantile(mean_counts_g2,(pc+ (1-pc)/2)))
  
  ind_min_g1 <-  which(mean_counts_g1 < q1_g1)
  ind_min_g2 <-  which(mean_counts_g2 < q1_g2)
  ind_max_g1 <-  which(mean_counts_g1 > q2_g1)
  ind_max_g2 <-  which(mean_counts_g2 > q2_g2)
  
  ind_plot <- unique(c(ind_min_g1,ind_min_g2,ind_max_g1,ind_max_g2))
  sequences <- data_g2[,1]    
  
  mylabel <- sequences[ind_plot]
  
  df <- as.data.frame(cbind(mean_counts_g2,mean_counts_g1))
  
  if(kmer < 5){
    p <- ggplot(df, aes(x=mean_counts_g1, y=mean_counts_g2)) + 
    geom_label_repel(data=df[ind_plot,], aes(x=mean_counts_g1,y=mean_counts_g2,label=mylabel),hjust = 0, nudge_x = 0.15,check_overlap=TRUE) +
      geom_point() +
      geom_smooth(method=lm) +
      labs(y = y_label) +
      labs(x = x_label) +
    # ylim(max( c((min(df$mean_counts_g2) - 50),0)), max(df$mean_counts_g2) + 50) +
    # xlim(max( c((min(df$mean_counts_g2) - 50),0)), max(df$mean_counts_g1) + 50) +
      geom_hline(yintercept = q2_g2, size = 0.5,color="red",linetype = 2) +
      geom_vline(xintercept = q2_g1, size = 0.5,color="red",linetype = 2) +
      geom_hline(yintercept = q1_g2, size = 0.5,color="red",linetype = 2) +
      geom_vline(xintercept = q1_g1, size = 0.5,color="red",linetype = 2) +
      theme_bw() +
      theme(axis.text=element_text(size=12),axis.title=element_text(size=14,face="bold")) +
      ggtitle(plot_title)
    
    ggsave(p,file=paste0(out_dir,plot_file_name,".pdf"),width = 5,height = 6)  
    
  }
  
  if(kmer >= 5){
    
    p = ggplot(data=df, aes(x=mean_counts_g1, y=mean_counts_g2))  
    p = p + labs(y=y_label, x=x_label)
    p = p + theme(axis.text=element_text(size=9), 
                  axis.title = element_text(size=9, face="bold"),
                  plot.title = element_text(size=9, face="bold")
    )
    p = p + theme(panel.background = element_rect(fill="white",colour ="black",size=0.5,linetype="solid"),
                  panel.grid.major = element_line(size=0.25,linetype='solid',colour="gray"), 
                  panel.grid.minor = element_line(size=0.25,linetype='solid',colour="gray"),
                  axis.text=element_text(size=12),axis.title=element_text(size=14,face="bold")) +
      ggtitle(plot_title)
    
    #pc <- 0.99
    #q1_g1 <- round(quantile(mean_counts_g1,(1-pc)/2))
    #q1_g2 <- round(quantile(mean_counts_g2,(1-pc)/2))
    
    #q2_g1 <- quantile(mean_counts_g1,(pc + (1-pc)/2)) 
    #q2_g2 <- quantile(mean_counts_g2,(pc+ (1-pc)/2))
    
    p.hexbin <- p + geom_hex(aes(fill="#000000",alpha=log10(..count..)), fill="#0000ff") 
    #scale_alpha_continuous("Log of Count", breaks=seq(0,10,1)) 
    #geom_hline(yintercept = q2_g1, size = 0.5,color="red",linetype = 2) +
    #geom_vline(xintercept = q2_g2, size = 0.5,color="red",linetype = 2) +
    #geom_hline(yintercept = q1_g1, size = 0.5,color="red",linetype = 2) +
    #geom_vline(xintercept = q1_g2, size = 0.5,color="red",linetype = 2) 
    #geom_smooth(method=lm) 
    
    ggsave(p.hexbin,file=paste0(out_dir,plot_file_name,".pdf"),width = 5,height = 6)  
    
  }
  
  out <- cor_test
  return <- out
  
}

### End of auxiliary functions 

#######################################
### Analysis group 1 vs group 2     ###
#######################################

input_data_directory <- "C:/Users/etien/Desktop/RStudioTest/"
output_directory <- "C:/Users/etien/Desktop/Graphs/"

file_group1_name <- "Anncaliia algerae hosts"
file_group2_name <- "2018"
comparison <- "Plasmodium falciparum 2018 vs hosts"
plot_file <- "2018"

results_cor  <- NULL

i_vec <- 1:7


for(i in i_vec){
  
  print(i)
  
  data_group_1 <- as.data.frame(read_excel(path=paste0(input_data_directory,file_group1_name,"_k=",i,".xlsx"),col_names=TRUE))
  
  ### checking if there are empty entries
  print(sum(is.na(data_group_1)) == 0) ## if TRUE there are not empty entries
  
  if(sum(is.na(data_group_1)) != 0 ){
    data_group_1[is.na(data_group_1)] <- 0 ### sum(is.na(data_group_2)) == 0
  }
  
  data_group_2 <- as.data.frame(read_excel(path=paste0(input_data_directory,file_group2_name,"_k=",i,".xlsx"),col_names=TRUE))
  
  ### checking if there are empty entries
  print(sum(is.na(data_group_2)) == 0) ## if TRUE there are not empty entries
  
  if(sum(is.na(data_group_2)) != 0 ){
    data_group_2[is.na(data_group_2)] <- 0 ### sum(is.na(data_group_2)) == 0
  }
  
  
  cor_results <- correlation.groups.f(data_g1=data_group_1,data_g2=data_group_2,
                                      comparison_label = paste0(comparison, ", k=",i, ","), 
                                      x_label = "hosts",
                                      y_label ="Plasmodium 2018",
                                      out_dir=output_directory,
                                      pc = 0.95,
                                      plot_file_name=paste0(plot_file,"_k",i),
                                      kmer=i)
  
  print(cor_results)
  results_cor <- rbind(results_cor,c(cor_results$p.value,cor_results$estimate))
  colnames(results_cor) <- c("p-value","rho")
  
}

print(results_cor)

