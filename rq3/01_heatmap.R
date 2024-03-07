
library(ggplot2)
library(scales)
library(stringr)
library(hexbin)
# get the data

make_plot1 = function() {
   data <- read.csv("./data/heatmapSizes.csv")
   theme_set(theme_light(base_size = 14))
   data$added = ordered(data$added)
   data$deleted = ordered(data$deleted)
   data$Proportion = data$n1line / data$nl1commits
   data$Project = str_to_title(data$project)
   gg <- ggplot(data, aes(added,deleted,fill=Proportion),group=Project)
   gg<-gg + ggtitle(bquote("Proportion of One-line commits by number of added and removed tokens"))
   gg<-gg+  theme(plot.title = element_text(hjust = 0.5))
   gg <- gg + geom_tile(color='black')
   gg <- gg + scale_x_discrete("Tokens added")
   gg <- gg + scale_y_discrete("Tokens deleted")
   gg <- gg + scale_fill_gradient(low="#f5f0ff", high="blue", trans='sqrt')
   # gg <- gg + scale_fill_viridis(trans='sqrt')
   # gg <- gg + scale_fill_scico(palette = "davos", direction = 1, trans='sqrt')
   gg <- gg + facet_grid(cols=vars(data$Project))

   ggsave(paste0('./plot/heatOneLineTokens.pdf'), width=12, height=4)
   ggsave(paste0('./plot/heatOneLineTokens.png'), width=12, height=4)
}

make_plot2 = function() {
   data <- read.csv("./data/heatmapSizes.csv")
   theme_set(theme_light(base_size = 16))
   data$added = ordered(data$added)
   data$deleted = ordered(data$deleted)
   data$Proportion = data$n / data$ncommits
   data$Project = str_to_title(data$project)
   gg <- ggplot(data, aes(added,deleted,fill=Proportion),group=Project)
   gg<-gg + ggtitle(bquote("Proportion of all commits by number of added and removed tokens"))
   gg<-gg+  theme(plot.title = element_text(hjust = 0.5))
   gg <- gg + geom_raster()
   gg <- gg + scale_x_discrete("Tokens added")
   gg <- gg + scale_y_discrete("Tokens deleted")
   gg <- gg + scale_fill_gradient(low="#f5f0ff", high="blue", trans='sqrt')
   # gg <- gg + scale_fill_gradient(low="#f5f5f5", high="blue")
   gg <- gg + facet_grid(cols=vars(data$Project))

   ggsave(paste0('./plot/heatTokens.pdf'), width=12, height=4)
   ggsave(paste0('./plot/heatTokens.png'), width=12, height=4)
}

make_plot3 = function() {
   data <- read.csv("./data/maxtokenadded.csv")
   data$Project = str_to_title(data$project)
   data$maxtokens = as.factor(data$maxtokens)
   theme_set(theme_light(base_size = 16))
   gg <- ggplot(data, aes(x=maxtokens,y=prop1l,group=Project))
   gg <- gg + geom_line(aes(linetype=Project,color=Project), linewidth=1)
   gg <- gg + scale_x_discrete("Maximum number tokens\nadded or removed")
   gg<-gg + ggtitle('One-line commits')
   gg<-gg+  theme(plot.title = element_text(hjust = 0.5))
   gg <- gg + scale_y_continuous("Proportion")

   ggsave(paste0('./plot/token1lAccum.pdf'), width=6, height=4)
   ggsave(paste0('./plot/token1lAccum.png'), width=6, height=4)
}

make_plot1()
make_plot2()
make_plot3()