setwd("~/Masters/Research/Main_Code")


library(ggplot2)
library(readr)
library(tidyr)
library(dplyr)
library(RColorBrewer)

MHWMA_results_df <- read_csv("results/univariate_results/dist/MHWMA_dist_results.csv")
EHWMA_results_df <- read_csv("results/univariate_results/dist/EHWMA_dist_results.csv")

cols_of_interest = c("ARL","Phi","Distribution","MIN","Q25","MRL","Q75","MAX")
main_mod_df = MHWMA_results_df[cols_of_interest]
main_mod_df$Distribution <- factor(main_mod_df$Distribution,
                                   levels = c("N(0,1)",
                                              "t(10)",
                                              "GAM(1,1)",
                                              "GAM(10,1)",
                                              "LogN(0,1)",
                                              "X2(30)"))

main_mod_df$Phi <- paste("phi :",main_mod_df$Phi,sep = '')

cols_of_interest = c("ARL","Phi","Phi2","Distribution","MIN","Q25","MRL","Q75","MAX")
main_ex_df = EHWMA_results_df[cols_of_interest]
main_ex_df$Distribution <- factor(main_ex_df$Distribution,
                                   levels = c("N(0,1)",
                                              "t(10)",
                                              "GAM(1,1)",
                                              "GAM(10,1)",
                                              "LogN(0,1)",
                                              "X2(30)"))

main_ex_df <- main_ex_df[((main_ex_df$Phi2 %in% c(0.01,0.09))&(main_ex_df$Phi == 0.1))|((main_ex_df$Phi2 %in% c(0.05,0.2))&(main_ex_df$Phi == 0.25)),]


main_ex_df$Phi <- paste("phi[1] :",main_ex_df$Phi)
main_ex_df$Phi2 <- paste("phi[2] :",main_ex_df$Phi2)

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
                                      colour = "white"),
      legend.position = "none"
      
      #since the legend often requires manual tweaking 
      #based on plot content, don't define it here
    )
}

mod_plot <- main_mod_df %>%
  ggplot(aes(x=Distribution,y=ARL,fill=Distribution))+
  geom_boxplot(aes(
    lower = Q25, 
    upper = Q75, 
    middle = MRL, 
    ymin = MIN, 
    ymax = MAX),
    stat = "identity")+
  geom_point(aes(y=ARL),fill='black')+
  geom_hline(yintercept = 200,col='red',linetype='dashed',size=1.2)+
  scale_fill_brewer(palette="RdBu")+
  facet_wrap(~Distribution) +
  facet_grid(rows = vars(Phi),scales = "free",labeller = label_parsed)+
  labs(title = "IC ROBUSTNESS")+
  xlab("Distribution")+
  ylab("RL")+
  ylim(0,550)+
  theme_main()

print(mod_plot)
ggsave(plot=mod_plot,
       filename= "modified_dist_plot.png",
       path = "results/Plots",
       dpi=320,
       width=8.70,
       height=5.95,
)


ex_plot <- main_ex_df %>%
  ggplot(aes(x=Distribution,y=ARL,fill=Distribution))+
  geom_boxplot(aes(
    lower = Q25, 
    upper = Q75, 
    middle = MRL, 
    ymin = MIN, 
    ymax = MAX),
    stat = "identity")+
  geom_point(aes(y=ARL),fill='black')+
  geom_hline(yintercept = 200,col='red',linetype='dashed',size=1.2)+
  scale_fill_brewer(palette="RdBu")+
  facet_wrap(~Distribution) +
  facet_grid(rows = vars(Phi,Phi2),scales = "free",labeller = label_parsed)+
  labs(title = "IC ROBUSTNESS")+
  xlab("Distribution")+
  ylab("RL")+
  ylim(0,550)+
  theme_main()

print(ex_plot)
ggsave(plot=ex_plot,
       filename= "extended_dist_plot.png",
       path = "results/Plots",
       dpi=320,
       width=8.70,
       height=5.95,
)