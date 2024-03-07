library(reshape2)
library(ggplot2)

data_path = "./tables"



test = function(target){
  df = read.csv(paste0(data_path, "/", target, ".csv"))
  g <- ggplot(
      df,
      aes(
          x=Project,
          y=Value,
          fill=Target
      )
  )
  g <- g + geom_bar(stat="identity", alpha=1.0, position=position_dodge()) 
  g <- g + geom_text(aes(label=gsub("XXX", "\n", Label)), size = 4, vjust=-0.5, position = position_dodge(0.9))

  g <- g + scale_fill_grey(start=0.8, end=0.2)
  g <- g + theme_bw()
  g <- g + theme(axis.line = element_line(colour = "black"), legend.position='none',
                  panel.grid.major.y = element_line(colour = "grey50", linetype="dashed"),
                  panel.grid.major.x = element_blank())

  # g <- g + scale_x_discrete(labels=c('All', 'Bug', 'Clean', 'NoLab'))

  g <- g + theme(axis.title.y = element_text(size=15),axis.title.x = element_text(size=15),
                  axis.text.y = element_text(size=15),axis.text.x = element_text(size=15,angle = 30, vjust=0.8))
  g <- g + theme(legend.title = element_blank(), plot.margin = margin(0, 0, 0, 0, "cm"))


  g <- g + xlab('') + ylab('')
  # g <- g + scale_y_continuous(trans = "log10",
  #                             breaks = y_breaks_dict[[target]],
  #                             labels = y_breaks_label_dict[[target]])
  g <- g + coord_cartesian(ylim = c(0, 55))
  #g <- g + ylim(0,50)



  ggsave(file=paste0('./plot/', target, '.pdf'), plot = g, width = 8, height = 5)

}


target_data_list = c(
    'corrective',
    'adaptive',
    'perfective'
)
for (target in target_data_list) {
  test(target)
}

