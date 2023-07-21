setwd("~/Masters/Research/Main_Code")


library(ggplot2)
library(readr)
library(tidyr)
library(dplyr)
library(RColorBrewer)

HWMA_results_df <- read_csv("results/univariate_results/ced/HWMA_CED_results.csv")
EWMA_results_df <- read_csv("results/univariate_results/ced/EWMA_CED_results.csv")
EHWMA_results_df <- read_csv("results/univariate_results/ced/EHWMA_CED_results.csv")
EEWMA_results_df <- read_csv("results/univariate_results/ced/EEWMA_CED_results.csv")
MHWMA_results_df <- read_csv("results/univariate_results/ced/MHWMA_CED_results.csv")
MEWMA_results_df <- read_csv("results/univariate_results/ced/MEWMA_CED_results.csv")

cols_of_interest = c("Tau","ARL","Delta","Phi","Parameter_string","Scheme")

#add scheme
HWMA_results_df$Scheme <- "HWMA"
EHWMA_results_df$Scheme <- "EHWMA"
MHWMA_results_df$Scheme <- "MHWMA"

EWMA_results_df$Scheme <- "EWMA"
EEWMA_results_df$Scheme <- "EEWMA"
MEWMA_results_df$Scheme <- "MEWMA"

#Alt HWMA, EWMA
Alt_HWMA <- data.frame(lapply(HWMA_results_df, rep, 3)) %>% arrange(Delta,Phi)
Alt_HWMA$Phi2 <- EHWMA_results_df$Phi2

Alt_EWMA <- data.frame(lapply(EWMA_results_df, rep, 3)) %>% arrange(Delta,Phi)
Alt_EWMA$Phi2 <- EEWMA_results_df$Phi2

main_mod_df <- rbind(HWMA_results_df[cols_of_interest],
                     EWMA_results_df[cols_of_interest],
                     MHWMA_results_df[cols_of_interest],
                     MEWMA_results_df[cols_of_interest])

main_ex_df <- rbind(Alt_HWMA,
                    Alt_EWMA,
                    EHWMA_results_df,
                    EEWMA_results_df)

#MODIFIED
main_mod_df$Delta <- as.factor(main_mod_df$Delta)
main_mod_df$Scheme <- factor(main_mod_df$Scheme,levels= c("EWMA","HWMA","MEWMA","MHWMA"))
main_mod_df$Phi <- paste("phi :",main_mod_df$Phi,sep = '')
main_mod_df$Delta <- paste("delta :",main_mod_df$Delta,sep = '')
main_mod_df$ARL <- round(main_mod_df$ARL,1)

#EXTENDED
main_ex_df$Delta <- as.factor(main_ex_df$Delta)
main_ex_df$Scheme <- factor(main_ex_df$Scheme,levels= c("EWMA","HWMA","EEWMA","EHWMA"))
main_ex_df$Phi <- paste("phi[1] :",main_ex_df$Phi)
main_ex_df$Phi2 <- paste("phi[2] :",main_ex_df$Phi2)
main_ex_df$Delta <- paste("delta :",main_ex_df$Delta,sep = '')
main_ex_df$ARL <- round(main_ex_df$ARL,1)

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
  ggplot(aes(x=Tau,y=ARL,col=Scheme))+
  geom_path(size=1.3,linetype="dotdash")+
  scale_fill_brewer(palette="RdBu")+
  facet_wrap(~Scheme) +
  facet_grid(rows = vars(Phi),cols = vars(Delta),scales = "free",labeller = label_parsed)+
  labs(title = "CED ARL Performance")+
  xlab(expression(paste("ced: ", tau)))+
  theme_main()

print(mod_plot)
ggsave(plot=mod_plot,
       filename= "modified_CED_compare_plot_univariate.png",
       path = "results/Plots",
       dpi=320,
       width=8.70,
       height=5.95,
)