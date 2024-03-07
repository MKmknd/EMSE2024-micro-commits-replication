# library(RSQLite)
# library(data.table)
# library(dplyr)
library(ggplot2)
library(reshape2)

#Setup paths
#wd = "/home/work_dir/exp42"
#setwd(wd)

#Load plotter
# source(plotterPath)

compute_percentage = function(df) {
  df$percent = round(100*(df$count/sum(df$count)), digits=1)
  df$label = paste0(df$percent, '%XXX(', df$count, ')')
  return(df)
}

# show top-10 frequently changed token types by bar plots
show_dist1 = function(p_name){
  
  df = read.csv(paste0("./data/changed_token_type_order_", p_name, ".csv"), header=FALSE)

  names(df) = c('token_types', 'count')

  df = compute_percentage(df)
  #print(df['token_types'])
  #print(df['token_types'][0:5,])

  p = ggplot(df, aes(x=reorder(token_types, -count), y=count), environment = environment())
  p = p + geom_bar(stat="identity", alpha=0.5)
  p = p + geom_text(aes(label=gsub("XXX", "\n", label)), size = 5, vjust=-0.5, position = position_dodge(0.9))
  p = p + xlab('Number of changed token types(Top-10)') + ylab('')

  p = p + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
  panel.background = element_blank(), axis.line = element_line(colour = "black"))
  #, legend.position='top')
  p = p + theme(axis.title.x = element_text(size=12),axis.title.y = element_text(size=12)) 
  p = p + theme(axis.text.x = element_text(size=12, angle=10),axis.text.y = element_text(size=12)) 
  p = p + theme(legend.title = element_text(size=12),legend.text = element_text(size=12))

  #p = p + scale_x_continuous(breaks=seq(0,100,by=10), labels=seq(0,100,by=10))
  p = p + scale_x_discrete(limits=df['token_types'][0:10,])
  p = p + coord_cartesian(ylim = c(0, max(df$count)*1.2))

  ggsave(paste0('./plot/num_changed_token_type_', p_name, '.pdf'), width=8, height=4)
  ggsave(paste0('./plot/num_changed_token_type_', p_name, '.png'), width=8, height=4)
  
}

# show top-10 frequently changed tokens by bar plots
show_dist2 = function(p_name){
  
  df = read.csv(paste0("./data/changed_token_order_", p_name, ".csv"), header=FALSE)

  names(df) = c('tokens', 'count')

  df = compute_percentage(df)

  p = ggplot(df, aes(x=reorder(tokens, -count), y=count), environment = environment())
  p = p + geom_bar(stat="identity", alpha=0.5)
  p = p + geom_text(aes(label=gsub("XXX", "\n", label)), size = 5, vjust=-0.5, position = position_dodge(0.9))
  p = p + xlab('Number of changed tokens (Top-10)') + ylab('')

  p = p + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
  panel.background = element_blank(), axis.line = element_line(colour = "black"))
  #, legend.position='top')
  p = p + theme(axis.title.x = element_text(size=12),axis.title.y = element_text(size=12)) 
  p = p + theme(axis.text.x = element_text(size=12, angle=10),axis.text.y = element_text(size=12)) 
  p = p + theme(legend.title = element_text(size=12),legend.text = element_text(size=12))

  #p = p + scale_x_continuous(breaks=seq(0,100,by=10), labels=seq(0,100,by=10))
  p = p + scale_x_discrete(limits=df['tokens'][0:10,])
  p = p + coord_cartesian(ylim = c(0, max(df$count)*1.2))

  ggsave(paste0('./plot/num_changed_token_', p_name, '.pdf'), width=8, height=4)
  ggsave(paste0('./plot/num_changed_token_', p_name, '.png'), width=8, height=4)
  
}


# show top-10 frequently replaced token types by bar plots
show_dist3 = function(p_name){
  
  df = read.csv(paste0("./data/replaced_token_type_order_", p_name, ".csv"), header=FALSE)

  names(df) = c('token_types', 'count')
  #print(df['token_types'])
  #print(df['token_types'][0:5,])

  df = compute_percentage(df)

  p = ggplot(df, aes(x=reorder(token_types, -count), y=count), environment = environment())
  p = p + geom_bar(stat="identity", alpha=0.5)
  p = p + geom_text(aes(label=gsub("XXX", "\n", label)), size = 5, vjust=-0.5, position = position_dodge(0.9))
  p = p + xlab('Number of replaced token types(Top-10)') + ylab('')

  p = p + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
  panel.background = element_blank(), axis.line = element_line(colour = "black"))
  #, legend.position='top')
  p = p + theme(axis.title.x = element_text(size=12),axis.title.y = element_text(size=12)) 
  p = p + theme(axis.text.x = element_text(size=12, angle=10),axis.text.y = element_text(size=12)) 
  p = p + theme(legend.title = element_text(size=12),legend.text = element_text(size=12))

  #p = p + scale_x_continuous(breaks=seq(0,100,by=10), labels=seq(0,100,by=10))
  p = p + scale_x_discrete(limits=df['token_types'][0:10,])
  p = p + coord_cartesian(ylim = c(0, max(df$count)*1.2))

  ggsave(paste0('./plot/num_replaced_token_type_', p_name, '.pdf'), width=8, height=4)
  ggsave(paste0('./plot/num_replaced_token_type_', p_name, '.png'), width=8, height=4)
  
}

# show top-10 frequently replaced tokens by bar plots
show_dist4 = function(p_name){
  
  df = read.csv(paste0("./data/replaced_token_order_", p_name, ".csv"), header=FALSE)

  names(df) = c('tokens', 'count')

  df = compute_percentage(df)

  p = ggplot(df, aes(x=reorder(tokens, -count), y=count), environment = environment())
  p = p + geom_bar(stat="identity", alpha=0.5)
  p = p + geom_text(aes(label=gsub("XXX", "\n", label)), size = 5, vjust=-0.5, position = position_dodge(0.9))
  p = p + xlab('Number of replaced tokens (Top-10)') + ylab('')

  p = p + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
  panel.background = element_blank(), axis.line = element_line(colour = "black"))
  #, legend.position='top')
  p = p + theme(axis.title.x = element_text(size=12),axis.title.y = element_text(size=12)) 
  p = p + theme(axis.text.x = element_text(size=12, angle=10),axis.text.y = element_text(size=12)) 
  p = p + theme(legend.title = element_text(size=12),legend.text = element_text(size=12))

  #p = p + scale_x_continuous(breaks=seq(0,100,by=10), labels=seq(0,100,by=10))
  p = p + scale_x_discrete(limits=df['tokens'][0:10,])
  p = p + coord_cartesian(ylim = c(0, max(df$count)*1.2))

  ggsave(paste0('./plot/num_replaced_token_', p_name, '.pdf'), width=8, height=4)
  ggsave(paste0('./plot/num_replaced_token_', p_name, '.png'), width=8, height=4)
  
}


project_name_list = c('camel', 'hadoop', 'linux', 'zephyr')
for (p_name in project_name_list) {
  show_dist1(p_name)
  show_dist2(p_name)
  show_dist3(p_name)
  show_dist4(p_name)
}

