# library(RSQLite)
# library(data.table)
library(ggplot2)
library(reshape2)

show_hunks_linerepo = function(num_hunks){

  p = ggplot(num_hunks, aes(x=hunkslines, color=project), environment = environment())
  p = p + stat_ecdf(geom='step')

  p = p + xlab('Number of hunks in line repositories') + ylab('')

  p = p + theme(panel.background = element_blank(), axis.line = element_line(colour = "black"))
  p = p + theme(panel.grid.major.x = element_line(size = 0.1, linetype = 'solid', colour = "gray"))
  p = p + theme(axis.title.x = element_text(size=12),axis.title.y = element_text(size=12)) 
  p = p + theme(axis.text.x = element_text(size=12),axis.text.y = element_text(size=12)) 
  p = p + theme(legend.title = element_text(size=12),legend.text = element_text(size=12))

  p = p + scale_x_continuous(breaks=seq(0,10,by=1), labels=seq(0,10,by=1))
  p = p + coord_cartesian(xlim = c(1,10)) 

  ggsave(paste0('./plot/num_hunks_linerepo.pdf'), width=8, height=4)

  print("in Line repo, show some proportions")
  p_list = c('linux', 'zephyr', 'camel', 'hadoop')
  for (p_name in p_list) {
    tmp_df = num_hunks[num_hunks$project==p_name,]
    pro = sum(tmp_df$hunkslines <= 1) / nrow(tmp_df) * 100
    print(p_name)
    print(pro)
  }
  # [1] "in Line repo, show some proportions"
  # [1] "linux"
  # [1] 68.7452
  # [1] "zephyr"
  # [1] 61.81025
  # [1] "camel"
  # [1] 61.79669
  # [1] "hadoop"
  # [1] 69.92519
  
}


show_hunks_tokenrepo = function(num_hunks){

  p = ggplot(num_hunks, aes(x=hunkstokens, color=project), environment = environment())
  p = p + stat_ecdf(geom='step')

  p = p + xlab('Number of hunks in token repositories') + ylab('')

  p = p + theme(panel.background = element_blank(), axis.line = element_line(colour = "black"))
  p = p + theme(panel.grid.major.x = element_line(size = 0.1, linetype = 'solid', colour = "gray"))
  p = p + theme(axis.title.x = element_text(size=12),axis.title.y = element_text(size=12)) 
  p = p + theme(axis.text.x = element_text(size=12),axis.text.y = element_text(size=12)) 
  p = p + theme(legend.title = element_text(size=12),legend.text = element_text(size=12))

  p = p + scale_x_continuous(breaks=seq(0,10,by=1), labels=seq(0,10,by=1))
  p = p + coord_cartesian(xlim = c(1,10)) 

  ggsave(paste0('./plot/num_hunks_tokenrepo.pdf'), width=8, height=4)
  
}


num_hunks = read.csv(paste0("./data/num_hunks.csv"), header=FALSE)
names(num_hunks) = c('project','linecid','tokencid','hunkslines','hunkstokens')
show_hunks_linerepo(num_hunks)
show_hunks_tokenrepo(num_hunks)
