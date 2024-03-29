setwd("~/Masters/Research/Main_Code")

library(ggplot2)
library(readr)
library(tidyr)
library(dplyr)
library(RColorBrewer)

#MULTIVARIATE DIM:p
p=4
HWMA_results_df <- read_csv(paste("results/multivariate_results/p",p,"_HWMA_ARL_SDRL_MRL_results.csv",sep = ''))
EWMA_results_df <- read_csv(paste("results/multivariate_results/p",p,"_EWMA_ARL_SDRL_MRL_results.csv",sep = ''))
EHWMA_results_df <- read_csv(paste("results/multivariate_results/p",p,"_EHWMA_ARL_SDRL_MRL_results.csv",sep = ''))
EEWMA_results_df <- read_csv(paste("results/multivariate_results/p",p,"_EEWMA_ARL_SDRL_MRL_results.csv",sep = ''))
MHWMA_results_df <- read_csv(paste("results/multivariate_results/p",p,"_MHWMA_ARL_SDRL_MRL_results.csv",sep = ''))
MEWMA_results_df <- read_csv(paste("results/multivariate_results/p",p,"_MEWMA_ARL_SDRL_MRL_results.csv",sep = ''))

cols_of_interest = c("ARL","Delta","Phi","Parameter_string","Scheme")

#add scheme
HWMA_results_df$Scheme <- "HWMA"
EHWMA_results_df$Scheme <- "EHWMA"
MHWMA_results_df$Scheme <- "MHWMA"

EWMA_results_df$Scheme <- "EWMA"
EEWMA_results_df$Scheme <- "EEWMA"
MEWMA_results_df$Scheme <- "MEWMA"

dontwants <- c("phi=0.1,phi2=0.09","phi=0.25,phi2=0.2")

EEWMA_results_df <- EEWMA_results_df[!(EEWMA_results_df$Parameter_string %in% dontwants),]
EHWMA_results_df <- EHWMA_results_df[!(EHWMA_results_df$Parameter_string %in% dontwants),]

#Alt HWMA, EWMA
Alt_HWMA <- data.frame(lapply(HWMA_results_df, rep, 2)) %>% arrange(Delta,Phi)
Alt_HWMA$Phi2 <- EHWMA_results_df$Phi2

Alt_EWMA <- data.frame(lapply(EWMA_results_df, rep, 2)) %>% arrange(Delta,Phi)
Alt_EWMA$Phi2 <- EEWMA_results_df$Phi2

main_mod_df <- rbind(HWMA_results_df[cols_of_interest],
                     EWMA_results_df[cols_of_interest],
                     MHWMA_results_df[cols_of_interest],
                     MEWMA_results_df[cols_of_interest])

main_ex_df <- rbind(Alt_HWMA,
                    Alt_EWMA,
                    EHWMA_results_df,
                    EEWMA_results_df)



#main_df <- rbind(HWMA_results_df[cols_of_interest],
#                 EHWMA_results_df[cols_of_interest],
#                 MHWMA_results_df[cols_of_interest])

#main_mod_df <- main_mod_df[main_mod_df$Phi < 0.5,]
main_mod_df <- main_mod_df[(main_mod_df$Delta >= 0.25)&(main_mod_df$Delta < 2),]
main_mod_df$Parameter_string <- as.factor(main_mod_df$Parameter_string)
main_mod_df$Delta <- as.factor(main_mod_df$Delta)
main_mod_df$Scheme <- factor(main_mod_df$Scheme,levels= c("EWMA","HWMA","MEWMA","MHWMA"))

main_mod_df$Phi <- paste("phi :",main_mod_df$Phi,sep = '')
main_mod_df$Delta <- paste("delta :",main_mod_df$Delta,sep = '')

main_ex_df <- main_ex_df[main_ex_df$Phi < 0.5,]
main_ex_df <- main_ex_df[(main_ex_df$Delta >= 0.25)&(main_ex_df$Delta < 1.75),]
main_ex_df$Parameter_string <- as.factor(main_ex_df$Parameter_string)
main_ex_df$Delta <- as.factor(main_ex_df$Delta)
main_ex_df$Scheme <- factor(main_ex_df$Scheme,levels= c("EWMA","HWMA","EEWMA","EHWMA"))

main_ex_df$Phi <- paste("phi[1] :",main_ex_df$Phi)
main_ex_df$Phi2 <- paste("phi[2] :",main_ex_df$Phi2)
main_ex_df$Delta <- paste("delta :",main_ex_df$Delta,sep = '')

#main_df <- main_df[main_df$Phi < 0.5,]
#main_df <- main_df[(main_df$Delta > 0)&(main_df$Delta < 2),]
#main_df$Parameter_string <- as.factor(main_df$Parameter_string)

#theme_linedraw()

theme_main <- function(){ 
  font <- "CenturySch"   #assign font family up front
  
  theme_gray() %+replace%    #replace elements we want to change
    
    theme(
      
      #grid elements
      #panel.grid.major = element_blank(),    #strip major gridlines
      #panel.grid.minor = element_blank(),    #strip minor gridlines
      #axis.ticks = element_blank(),          #strip axis ticks
      
      #since theme_minimal() already strips axis lines, 
      #we don't need to do that again
      
      #text elements
      plot.title = element_text(             #title
        family = font,            #set font family
        size = 16,                #set font size
        face = 'bold',            #bold typeface
        hjust = 0,                #left align
        vjust = 2),               #raise slightly
      
      plot.subtitle = element_text(          #subtitle
        family = font,            #font family
        size = 14),               #font size
      
      plot.caption = element_text(           #caption
        family = font,            #font family
        size = 9,                 #font size
        hjust = 1),               #right align
      
      axis.title = element_text(             #axis titles
        family = font,            #font family
        size = 13,
        face="bold"),               #font size
      
      axis.text = element_text(              #axis text
        family = font,            #axis famuly
        size = 12),                #font size
      
      axis.text.x = element_blank(),
      axis.ticks.x=element_blank(),
      
      strip.text.x = element_text(
        size = 12,
        color = "white"
      ),
      strip.text.y = element_text(
        size = 12,
        angle = 270,
        color = "white"
      ),
      strip.background = element_rect(
        color="#4a6fcc", fill="#4a6fcc", size=0.7, linetype="solid"
      ),
      panel.background = element_rect(fill = "lightgrey",
                                      colour = "lightgrey",
                                      size = 0.5, linetype = "solid"),
      panel.grid.major = element_line(size = 0.5, linetype = 'solid',
                                      colour = "white"), 
      panel.grid.minor = element_line(size = 0.25, linetype = 'solid',
                                      colour = "white")
      
      #since the legend often requires manual tweaking 
      #based on plot content, don't define it here
    )
}

mod_plot <- main_mod_df %>%
  ggplot(aes(x=Delta,y=ARL,fill=Scheme))+
  geom_col(size=1.3,position="dodge")+
  scale_fill_brewer(palette="RdBu")+
  facet_wrap(~Scheme) +
  facet_grid(rows = vars(Phi),cols = vars(Delta),scales = "free",labeller = label_parsed)+
  labs(title = paste("OOC ARL Performance (p=",p,")",sep=''))+
  xlab(expression(paste("Shift size: ", delta)))+
  theme_main()

print(mod_plot)
ggsave(plot=mod_plot,
       filename= paste("modified_schmes_compare_plot_multivariate_p",p,".png",sep = ''),
       path = "results/Plots",
       dpi=320,
       width=8.70,
       height=5.95,
)

ex_plot <- main_ex_df %>%
  ggplot(aes(x=Delta,y=ARL,fill=Scheme))+
  geom_col(size=1.3,position="dodge")+
  scale_fill_brewer(palette="RdBu")+
  #xlim(0.5,1.75)+
  #scale_x_continuous(limits = c(0.5,1.75), expand = c(0, 0))+
  facet_wrap(~Scheme) +
  facet_grid(Phi + Phi2 ~ Delta,scales = "free",labeller = label_parsed)+
  labs(title = paste("OOC ARL Performance (p=",p,")",sep=''))+
  xlab(expression(paste("Shift size: ", delta)))+
  theme_main()

print(ex_plot)
ggsave(plot=ex_plot,
       filename= paste("extended_schmes_compare_plot_multivariate_p",p,".png",sep = ''),
       path = "results/Plots",
       dpi=320,
       width=8.70,
       height=5.95,
)
