# library(dplyr)
library(ggplot2)
library(reshape2)
library(stringr)

compute_percentage = function(df) {
  df$percent = round(100*(df$count/sum(df$count)), digits=1)
  #df$label = paste0(df$percent, '%XXX(', df$count, ')')
  df$label = paste0(df$percent, '%')
  return(df)
}

read_data = function(project_name_list, f_name_prefix, target_token_type_list) {
  df = data.frame(matrix(rep(NA, 5), nrow=1))[numeric(0), ]
  names(df) = c('token_types', 'count', 'percent', 'label', 'Project')

  for (p_name in project_name_list) {

    tmp = read.csv(paste0(f_name_prefix, p_name, ".csv"), header=FALSE)
    names(tmp) = c('token_types', 'count')
    tmp = compute_percentage(tmp)

    p_name_df = data.frame(c(str_to_title(p_name)))
    names(p_name_df) = 'Project'

    for (token_type in target_token_type_list) {
      df = rbind(df, cbind(tmp[tmp$token_types==token_type,], p_name_df))
    }

  }
  return(df)
}

# show top-10 frequently changed token types by bar plots
show_dist1 = function(project_name_list, target_token_type_list){

  df = read_data(project_name_list, "./data/changed_token_type_order_", target_token_type_list)


  # p = ggplot(df, aes(x=reorder(token_types, -count), y=count), fill=Project, environment = environment())
  p = ggplot(df, aes(x=token_types, y=percent, fill=Project), environment = environment())
  p = p + geom_bar(stat="identity", alpha=0.8, position = "dodge")
  #p = p + geom_text(aes(label=gsub("XXX", "\n", label), group=Project), size = 4, vjust=-0.5, position = position_dodge(0.9))
  p = p + geom_text(aes(label=label, group=Project), size = 4, vjust=-0.5, position = position_dodge(0.9))
  p = p + xlab('Number of changed token types (>5%)') + ylab('')

  p = p + theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
  panel.background = element_blank(), axis.line = element_line(colour = "black"))
  #, legend.position='top')
  p = p + theme(axis.title.x = element_text(size=16),axis.title.y = element_text(size=12)) 
  p = p + theme(axis.text.x = element_text(size=16, angle=0),axis.text.y = element_text(size=16)) 
  p = p + theme(legend.title = element_text(size=16),legend.text = element_text(size=16))

  #p = p + scale_x_continuous(breaks=seq(0,100,by=10), labels=seq(0,100,by=10))
  p = p + scale_x_discrete(limits=df['token_types'][0:3,])
  #p = p + coord_cartesian(ylim = c(0, max(df$count)*1.2))
  p = p + coord_cartesian(ylim = c(0, 60))

  ggsave(paste0('./plot/merged_num_changed_token_type.pdf'), width=12, height=4)
  ggsave(paste0('./plot/merged_num_changed_token_type.png'), width=12, height=4)
  
}


project_name_list = c('camel', 'hadoop', 'linux', 'zephyr')
target_token_type_list = c('name', 'literal', 'operator')
# c('name', 'literal', 'argument_list', 'operator')
show_dist1(project_name_list, target_token_type_list)

