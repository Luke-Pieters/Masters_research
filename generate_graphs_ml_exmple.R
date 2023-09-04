setwd("~/Masters/Research/Main_Code")


library(ggplot2)
library(readr)
library(tidyr)
library(dplyr)
library(RColorBrewer)

MHWMA_ml_exmpl_data <- read_csv("results/pm/MHWMA_ml_exmpl_data.csv")
EHWMA_ml_exmpl_data <- read_csv("results/pm/EHWMA_ml_exmpl_data.csv")

x_values = seq(-4,4,0.5)
X0 = x_values**0
X1 = x_values**1
X2 = x_values**2

b0 = 3
b1 = 2
b2 = 5

Y = b0*X0 +b1*X1 +b2*X2

profile_data = data.frame("Y"=Y,"X"=X1)

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
                                      colour = "white")
      
      #since the legend often requires manual tweaking 
      #based on plot content, don't define it here
    )
}

display.brewer.pal(n = 8, name = 'RdBu')
brewer.pal(n = 8, name = 'RdBu')

colours <- c("TRUE"="#B2182B","FALSE"="#2166AC")

profile_plot <- profile_data %>%
  ggplot(aes(x=X,y=Y))+
  geom_hline(yintercept = 0,col="#2166AC",size=1,alpha=0.5)+
  geom_vline(xintercept = 0,col="#2166AC",size=1,alpha=0.5)+
  geom_path(size=1.3,col="#B2182B")+
  labs(title = "IC Profile")+
  xlim(-4,4)+
  xlab('X')+
  ylab('Y')+
  theme_main()

print(profile_plot)
ggsave(plot=profile_plot,
       filename= "pm_example.png",
       path = "results/Plots",
       dpi=320,
       width=8.70,
       height=5.95,
)

mod_plot <- MHWMA_ml_exmpl_data %>%
  ggplot(aes(x=t,y=T2,col=OOC,group=1))+
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = 14, fill = "#4393C3", alpha = .5, color = NA)+
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = 14, ymax = Inf, fill = "#D6604D", alpha = .5, color = NA)+
  geom_hline(yintercept = 14,col='#B2182B',linetype='dashed',size=1.3)+
  geom_text(aes(1,14,label = 'h=14', vjust = -1),col='#B2182B')+
  geom_path(size=1.3)+
  geom_point(size=3)+
  scale_color_manual(values = colours)+
  labs(title = "Charting statisitc for each sample")+
  xlab('t')+
  xlim(1,8)+
  ylab('T2')+
  theme_main()

print(mod_plot)
ggsave(plot=mod_plot,
       filename= "modified_ml_example_chart.png",
       path = "results/Plots",
       dpi=320,
       width=8.70,
       height=5.95,
)

ex_plot <- EHWMA_ml_exmpl_data %>%
  ggplot(aes(x=t,y=T2,col=OOC,group=1))+
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = 14, fill = "#4393C3", alpha = .5, color = NA)+
  annotate("rect", xmin = -Inf, xmax = Inf, ymin = 14, ymax = Inf, fill = "#D6604D", alpha = .5, color = NA)+
  geom_hline(yintercept = 14,col='#B2182B',linetype='dashed',size=1.3)+
  geom_text(aes(1,14,label = 'h=14', vjust = -1),col='#B2182B')+
  geom_path(size=1.3)+
  geom_point(size=3)+
  scale_color_manual(values = colours)+
  labs(title = "Charting statisitc for each sample")+
  xlab('t')+
  xlim(1,8)+
  ylab('T2')+
  theme_main()

print(ex_plot)
ggsave(plot=ex_plot,
       filename= "extended_ml_example_chart.png",
       path = "results/Plots",
       dpi=320,
       width=8.70,
       height=5.95,
)