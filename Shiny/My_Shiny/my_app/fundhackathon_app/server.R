source('helpers.R')

library(shinydashboard)
library(leaflet)
library(dplyr)
library(DT)
library(xlsx)
library(stringi)
library(shinyjs)
options(shiny.deprecation.messages=FALSE)
options(shiny.usecairo = FALSE)
options(encoding = "UTF-8")



# import static data
fund_data <- read.xlsx('data/Full_Data.xlsx',sheetIndex = 1,encoding = 'UTF-8')
province_data <- read.xlsx('data/Province.xlsx', sheetIndex = 1,encoding = 'UTF-8')
sector_data <- read.xlsx('data/Sector.xlsx', sheetIndex = 1,encoding = 'UTF-8')
fund_image <- read.xlsx('data/Fund_Image.xlsx', sheetIndex = 1, encoding = 'UTF-8')


function(input, output, session) {
  
  ## Interactive Map ###########################################
  
  SelectProvince <- reactive({
    
    provinces <- c()
    
    if(!is.null(input$east)){
      if(0 %in% as.numeric(input$east)){
        provinces <- c(provinces, as.numeric(province_data$ProvinceNum[which(as.numeric(province_data$RegionNum)==1)]))
      }else if(length(input$east)>0){
        provinces <- c(provinces, as.numeric(input$east))
      }
    }

    if(!is.null(input$eastnorth)){
      if(0 %in% as.numeric(input$eastnorth)){
        provinces <- c(provinces, as.numeric(province_data$ProvinceNum[which(as.numeric(province_data$RegionNum)==2)]))
      }else if(length(input$eastnorth)>0){
        provinces <- c(provinces, as.numeric(input$eastnorth))
      }
    }

    
    if(!is.null(input$central)){
      if(0 %in% as.numeric(input$central)){
        provinces <- c(provinces, as.numeric(province_data$ProvinceNum[which(as.numeric(province_data$RegionNum)==3)]))
      }else if(length(input$central)>0){
        provinces <- c(provinces, as.numeric(input$central))
      }
    }

    if(!is.null(input$west)){
      if(0 %in% as.numeric(input$west)){
        provinces <- c(provinces, as.numeric(province_data$ProvinceNum[which(as.numeric(province_data$RegionNum)==4)]))
      }else if(length(input$west)>0){
        provinces <- c(provinces, as.numeric(input$west))
      }
    }    

    
  })
  
  
  SelectSector <- reactive({
    
    sectors <- c()
    
    if(!is.null(input$internationalaffair)){
      if(0 %in% as.numeric(input$internationalaffair)){
        sectors <- c(sectors, as.numeric(sector_data$SectorNum[which(as.numeric(sector_data$ParentSectorNum)==4)]))
      }else if(length(input$internationalaffair)>0){
        sectors <- c(sectors, as.numeric(input$internationalaffair))
      }
    }

    if(!is.null(input$cultureducation)){
      if(0 %in% as.numeric(input$cultureeducation)){
        sectors <- c(sectors, as.numeric(sector_data$SectorNum[which(as.numeric(sector_data$ParentSectorNum)==1)]))
      }else if(length(input$cultureeducation)>0){
        sectors <- c(sectors, as.numeric(input$cultureeducation))
      }
    }

    if(!is.null(input$environment)){
      if(0 %in% as.numeric(input$environment)){
        sectors <- c(sectors, as.numeric(sector_data$SectorNum[which(as.numeric(sector_data$ParentSectorNum)==3)]))
      }else if(length(input$environment)>0){
        sectors <- c(sectors, as.numeric(input$environment))
      }
    }

    if(!is.null(input$socialbenefit)){
      if(0 %in% as.numeric(input$socialbenefit)){
        sectors <- c(sectors, as.numeric(sector_data$SectorNum[which(as.numeric(sector_data$ParentSectorNum)==2)]))
      }else if(length(input$socialbenefit)>0){
        sectors <- c(sectors, as.numeric(input$socialbenefit))
      }
    }    

    
  })

  

  
  
  # select funds in specified provinces
  ProvinceFundLocations <- reactive({
    
    provinces <- SelectProvince()
    
    if (is.null(provinces)){
      return()
    }else{
      idx <- which(as.numeric(fund_data$ProvinceNum)%in%as.numeric(provinces))
      fund_data[idx, ]
    }
  })
  
  
  # select funds in specified sectors
  SectorFundLocations <- reactive({
    
    fund_data <- ProvinceFundLocations()
    sectors <- SelectSector()
    
    if ((is.null(sectors)) | is.null(fund_data)){
      return()
    }else{
      idx <- c()
      for(k in 1:dim(fund_data)[1]){
        if(length(Reduce(intersect,list(strsplit(as.character(fund_data$SectorNum[k]), ",")[[1]],sectors)))>0){
          idx <- c(idx, k)
        }
      }
      fund_data[idx, ]
    }
  })
  

  
  ComputeScore <- reactive({
    
    fund_data <- SectorFundLocations()
    if(is.null(fund_data)){
      return()
    }else{
      fund_data['WeiboScore'] <- (fund_data$Num_follower * input$followerweight/100 + 
                                    fund_data$Num_following * input$followingweight/100 +
                                    fund_data$Num_original_post * input$originalpostweight/100 +
                                    fund_data$Num_post * input$postweight/100 +
                                    fund_data$Num_forward * input$forwardweight/100 +
                                    fund_data$Num_comment * input$commentweight/100 +
                                    fund_data$Num_good * input$goodweight/100) 
      fund_data['Score'] <- (input$gsweight/100) * fund_data$NumGS + 
        (input$newsweight)/100 * fund_data$NumNews +
        (100-input$gsweight-input$wbweight-input$newsweight)/100 * fund_data$Connection + 
        (input$wbweight/100) * fund_data$WeiboScore
      
      fund_data <- fund_data[order(fund_data$Score, decreasing = T),]
      
      if(dim(fund_data)[1] > input$threshold){
        fund_data <- fund_data[1:input$threshold,]
      }
    }

  })

  
  
  # plot map
  output$map <- renderLeaflet({
    
    fund_data <- ComputeScore()
    
    if (is.null(fund_data)){
      leaflet() %>%
        addTiles() %>%
        setView(lng = province_data$Longitude[1], lat = province_data$Latitude[1], zoom = 5)
    }else{
      leaflet() %>%
        addTiles() %>%
        setView(lng = province_data$Longitude[1], lat = province_data$Latitude[1], zoom = 5) %>%
        addMarkers(
          lng=jitter(fund_data$Lon, factor = 2),
          lat=jitter(fund_data$Lat, factor = 2),
          popup = paste('基金会名称:',fund_data$FundName,'<br>',
                        '基金会影响力得分:',fund_data$Score,'<br>',
                        '基金会影响力排名:',seq(1,dim(fund_data)[1],1),'<br>',
                        '基金会网址:',fund_data$Website))
      
    }
  
  })
  
  
  ## Data Explorer ###########################################
  observe({
    updateSliderInput(session, "gsweight", min =0,max=100)
    updateSliderInput(session, "wbweight", min =0,max=100)
  })
  output$gsweight <- reactiveUI(function(){
    sliderInput("gsweight", "谷歌搜索权重", min=0,max = 100 - input$wbweight, value = 0, step = 1)
  })
  output$newsweight <- reactiveUI(function(){
    sliderInput("newsweight", "新闻媒体权重", min=0,max = 100 - input$wbweight - input$gsweight, value = 0, step = 1)
  })
  
  output$restable1 <- renderTable({
    myvals<- c(input$wbweight, input$gsweight, input$newsweight, 100 - input$wbweight - input$gsweight - input$newsweight)
    data.frame('指标名称'=c("微博影响力", "谷歌搜索影响力", "新闻媒体影响力", "基金会关联影响力"),
               '指标权重'=myvals)
  })
  output$restable2 <- renderTable({
    myvals<- c(input$followerweight,input$followingweight, input$originalpostweight, input$postweight, input$goodweight, input$commentweight,input$forwardweight)
    data.frame('微博指标名称'=c('粉丝数',"关注数","原创微博数","微博数","点赞数",'评论数', "转发数"),
               '指标权重'=myvals)
  })
  
  observeEvent(input$eastButton,{toggle('east')})
  observeEvent(input$eastnorthButton,{toggle('eastnorth')})
  observeEvent(input$centralButton,{toggle('central')})
  observeEvent(input$westButton,{toggle('west')})
  observeEvent(input$internationalaffairButton,{toggle('internationalaffair')})
  observeEvent(input$cultureeducationButton,{toggle('cultureeducation')})
  observeEvent(input$environmentButton,{toggle('environment')})
  observeEvent(input$socialbenefitButton,{toggle('socialbenefit')})
  
  output$funddata <- DT::renderDataTable({
    
    fund_data <- ComputeScore()
    
    if (is.null(fund_data)){
      data <- data.frame('基金会名称'=as.character(),
                         '影响力总得分'=as.numeric(),
                         '微博影响力得分'=as.numeric(),
                         '谷歌影响力得分'=as.numeric(),
                         '新闻媒体影响力得分'=as.numeric(),
                         '基金会关联度影响力得分'=as.numeric())
    }else{
      data <- fund_data[,c('FundName','Score','WeiboScore','NumGS','NumNews','Connection')]
      colnames(data) <- c('基金会名称','影响力总得分','微博影响力得分','谷歌影响力得分','新闻媒体影响力得分','基金会关联度影响力得分')
    }
    
    df <- data %>%
      mutate(Action = paste('<a class="go-map" href="" fund-score="', 影响力总得分, '" fund-weibo="', 微博影响力得分, '" fund-google="', 谷歌影响力得分,
                            '" fund-news="', 新闻媒体影响力得分,'" fund-connection="', 基金会关联度影响力得分, '"><i class="fa fa-crosshairs"></i></a>', sep=""))
    action <- DT::dataTableAjax(session, df)
    
    DT::datatable(df, options = list(ajax = list(url = action)), escape = FALSE)

  })
  
  
  
  ## fund image ###########################################
  output$fundimage <- DT::renderDataTable({
    
    image <- fund_image[as.numeric(input$fund),c('FundName','FundAge','Location','Sector','OriginalCapital',
                                                 'NumVolunteer','NumEmployer','ProjectIncome','ProjectSpend',
                                                 'DonationAmount','SubsidizeAmount','NumProject','NumSpecialFund')]
    
    if (is.null(image)){
      image <- data.frame('名称'=as.character(),
                         '成立天数'=as.numeric(),
                         '地址'=as.numeric(),
                         '领域'=as.numeric(),
                         '原始资本'=as.numeric(),
                         '志愿者数'=as.numeric(),
                         '员工数'=as.numeric(),
                         '项目收入'=as.numeric(),
                         '项目支出'=as.numeric(),
                         '受捐赠金额'=as.numeric(),
                         '资助金额'=as.numeric(),
                         '项目数'=as.numeric(),
                         '专项基金数'=as.numeric())
    }else{
      colnames(image) <- c('名称','成立天数','地址','领域','原始资本','志愿者数',
                           '员工数','项目收入','项目支出','受捐赠金额','资助金额','项目数','专项基金数')
    }
    
    df <- image %>%
      mutate(Action = paste('<a class="go-map" href="" fund-age="', 成立天数, 
                            '" fund-capital="', 原始资本, '" fund-volunteer="', 志愿者数,
                            '" fund-employer="',员工数,'" fund-income="', 项目收入,
                            '" fund-outcome="',项目支出,'" fund-donation="', 受捐赠金额,
                            '" fund-subsidize="',资助金额,'" fund-project="', 项目数,
                            '" fund-specialfund="', 专项基金数,'"><i class="fa fa-crosshairs"></i></a>', sep=""))
    action <- DT::dataTableAjax(session, df)
    
    DT::datatable(df, options = list(ajax = list(url = action)), escape = FALSE)
    
  })

}