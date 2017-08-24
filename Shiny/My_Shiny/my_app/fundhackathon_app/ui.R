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


fund_image <- read.xlsx('data/Fund_Image.xlsx', sheetIndex = 1, encoding = 'UTF-8')



navbarPage('基金会影响力分析', id='nav',
           
           tabPanel("互动地图",
                    div(class="outer",
                        tags$style(type = "text/css", ".outer {position: fixed; top: 41px; left: 0; right: 0; bottom: 0; overflow: hidden; padding: 0}"),
                        leafletOutput("map",width = "100%", height = "100%"),
                        # Shiny versions prior to 0.11 should use class="modal" instead.
                        sidebarPanel(selectInput("Type", "Type", c(Data = "data", Map = "map"))),
                        conditionalPanel(
                          condition = "input.Type == 'map'",
                          id = "controls", class = "panel panel-default", fixed = TRUE,
                          draggable = TRUE, top = 60, left = "auto", right = 20, bottom = "auto",
                          width = 330, height = "auto",
                          
                          h2("Fund explorer"),
                          
                          checkboxGroupInput(inputId = "provinces", 
                                             label = "Provinces",
                                             choices = c(
                                               All = 0,
                                               Beijing = 1,
                                               Tianjing = 2,
                                               Shanghai = 3,
                                               Chongqing = 4,
                                               Hebei = 5,
                                               Shan1xi = 6,
                                               Liaoning = 7,
                                               Jilin = 8,
                                               Heilongjiang = 9,
                                               Jiangsu = 10,
                                               Zhejiang = 11,
                                               Anhui = 12,
                                               Fujian = 13,
                                               Jiangxi = 14,
                                               Shandong = 15,
                                               Henan = 16,
                                               Hubei = 17,
                                               Hunan = 18,
                                               Guangdong = 19,
                                               Hainan = 20,
                                               Sichuan = 21,
                                               Guizhou = 22,
                                               Yunnan = 23,
                                               Shan3xi = 24,
                                               Gansu = 25,
                                               Qinghai = 26,
                                               Taiwan = 27,
                                               Neimenggu = 28,
                                               Guangxi = 29,
                                               Xizang = 30,
                                               Ningxia = 31,
                                               Xinjiang = 32,
                                               Hongkong = 33,
                                               Macau = 34
                                             ),
                                             selected = 0,
                                             inline = TRUE
                          ),
                          checkboxGroupInput(inputId = "sectors", 
                                             label = "Sectors",
                                             choices = c(
                                               All = 0,
                                               Youth = 1,
                                               Sport = 2,
                                               Minority = 3,
                                               PublicSecurity = 4,
                                               Community = 5,
                                               Children = 6,
                                               Women = 7,
                                               Animal = 8,
                                               MentalHealth = 9,
                                               Science = 10,
                                               HealthCare = 11,
                                               Law = 12,
                                               Culture = 13,
                                               Art = 14,
                                               MedicalAssistance = 15,
                                               Farm = 16,
                                               Environment = 17,
                                               Volunteer = 18,
                                               Poverty = 19,
                                               PublicService = 20,
                                               OverseaChinese = 21,
                                               Senior = 22,
                                               Diability = 23,
                                               Disaster = 24,
                                               Employment = 25,
                                               International = 26,
                                               Education = 27,
                                               Nonprofit = 28
                                             ),
                                             selected = 0,
                                             inline = TRUE
                          )
                        )
                    )
           ),
           
           tabPanel("指标权重",
                    sidebarLayout(
                      sidebarPanel(
                        sliderInput('wbweight', '微博影响力权重', 
                                    min=0, max=100, value=40, step=1),
                        fluidRow(
                          column(3,numericInput("followerweight", "粉丝数权重", min = 0, max = 100, step = 5, value = 40)),
                          column(3,numericInput("followingweight", "关注数权重", min = 0, max = 100, step = 5, value = 10)),
                          column(3,numericInput("originalpostweight", "原创微博数权重", min = 0, max = 100, step = 5, value = 10)),
                          column(3,numericInput("postweight", "微博数权重", min = 0, max = 100, step = 5, value = 10))
                        ),
                        fluidRow(
                          column(3,numericInput("goodweight", "点赞数权重", min = 0, max = 100, step = 5, value = 10)),
                          column(3,numericInput("commentweight", "评论数权重", min = 0, max = 100, step = 5, value = 10)),
                          column(3,numericInput("forwardweight", "转发数权重", min = 0, max = 100, step = 5, value = 10))
                        ),
                        uiOutput('gsweight'),
                        uiOutput('newsweight'),
                        fluidRow(
                          column(6, tableOutput("restable1")),
                          column(6, tableOutput('restable2'))
                        ),
                        fluidRow(
                          h4("基金会地域分类"),
                          column(3,shinyjs::useShinyjs(),
                                 actionButton('eastButton',label='东部地区'),
                                 hidden(
                                   checkboxGroupInput(inputId = "east", 
                                                      label = "东部地区城市",
                                                      choices = c(
                                                        '全部' = 0,
                                                        '北京' = 1,
                                                        '天津' = 2,
                                                        '上海' = 3,
                                                        '河北' = 5,
                                                        '江苏' = 10,
                                                        '浙江' = 11,
                                                        '福建' = 13,
                                                        '山东' = 15,
                                                        '广东' = 19,
                                                        '海南' = 20,
                                                        '台湾' = 27,
                                                        '香港' = 33,
                                                        '澳门' = 34
                                                      ),
                                                      selected = 0,
                                                      inline = FALSE
                                   ))
                                 ),
                          column(3,shinyjs::useShinyjs(),
                                 actionButton('eastnorthButton',label='东北地区'),
                                 hidden(
                                   checkboxGroupInput(inputId = "eastnorth", 
                                                      label = "东北地区城市",
                                                      choices = c(
                                                        '全部' = 0,
                                                        '辽宁' = 7,
                                                        '吉林' = 8,
                                                        '黑龙江' = 9
                                                      ),
                                                      selected = 0,
                                                      inline = FALSE
                                   ))
                                 ),
                          column(3,shinyjs::useShinyjs(),
                                 actionButton('centralButton',label='中部地区'),
                                 hidden(
                                   checkboxGroupInput(inputId = "central", 
                                                      label = "中部地区城市",
                                                      choices = c(
                                                        '全部' = 0,
                                                        '山西' = 6,
                                                        '安徽' = 12,
                                                        '江西' = 14,
                                                        '河南' = 16,
                                                        '湖北' = 17,
                                                        '湖南' = 18
                                                      ),
                                                      selected = 0,
                                                      inline = FALSE
                                   ))
                                 ),
                          column(3,shinyjs::useShinyjs(),
                                 actionButton("westButton", label = "西部地区"),
                                 hidden(
                                   checkboxGroupInput(inputId = "west", 
                                                      label = "西部地区城市",
                                                      choices = c(
                                                        '全部' = 0,
                                                        '重庆' = 4,
                                                        '四川' = 21,
                                                        '贵州' = 22,
                                                        '云南' = 23,
                                                        '陕西' = 24,
                                                        '甘肃' = 25,
                                                        '青海' = 26,
                                                        '内蒙古' = 28,
                                                        '广西' = 29,
                                                        '西藏' = 30,
                                                        '宁夏' = 31,
                                                        '新疆' = 32
                                                      ),
                                                      selected = 0,
                                                      inline = FALSE
                                   ))
                                 )
                        ),
                        fluidRow(
                          h4("基金会领域分类"),
                          column(3,shinyjs::useShinyjs(),
                                 actionButton('internationalaffairButton',label='国际事务'),
                                 hidden(
                                   checkboxGroupInput(inputId = "internationalaffair", 
                                                      label = "国际事务子类",
                                                      choices = c(
                                                        '全部' = 0,
                                                        '侨务' = 21,
                                                        '国际事务' = 26
                                                      ),
                                                      selected = 0,
                                                      inline = FALSE
                                   ))
                                 ),
                          column(3,shinyjs::useShinyjs(),
                                 actionButton('cultureeducationButton',label='文化教育'),
                                 hidden(
                                   checkboxGroupInput(inputId = "cultureeducation", 
                                                      label = "文化教育子类",
                                                      choices = c(
                                                        '全部' = 0,
                                                        '青少年' = 1,
                                                        '体育' = 2,
                                                        '科学研究' = 10,
                                                        '文化' = 13,
                                                        '艺术' = 14,
                                                        '教育' = 27
                                                      ),
                                                      selected = 0,
                                                      inline = FALSE
                                   ))
                                  ),
                          column(3,shinyjs::useShinyjs(),
                                 actionButton('environmentButton',label='资源环境'),
                                 hidden(
                                   checkboxGroupInput(inputId = "environment", 
                                                      label = "资源环境子类",
                                                      choices = c(
                                                        '全部' = 0,
                                                        '动物保护' = 8,
                                                        '环境' = 17
                                                      ),
                                                      selected = 0,
                                                      inline = FALSE
                                   ))
                                 ),
                          column(3,shinyjs::useShinyjs(),
                                 actionButton('socialbenefitButton',label='社会福利'),
                                 hidden(
                                   checkboxGroupInput(inputId = "socialbenefit", 
                                                      label = "社会福利子类",
                                                      choices = c(
                                                        '全部' = 0,
                                                        '少数民族' = 3,
                                                        '公共安全' = 4,
                                                        '社区发展' = 5,
                                                        '儿童' = 6,
                                                        '妇女' = 7,
                                                        '心理健康' = 9,
                                                        '卫生保健' = 11,
                                                        '法律实施' = 12,
                                                        '医疗救助' = 15,
                                                        '三农' = 16,
                                                        '志愿服务' = 18,
                                                        '扶贫助困' = 19,
                                                        '公共服务' = 20,
                                                        '老年人' = 22,
                                                        '残疾' = 23,
                                                        '安全救灾' = 24,
                                                        '创业就业' = 25,
                                                        '公益事业发展' = 28
                                                      ),
                                                      selected = 0,
                                                      inline = FALSE
                                   ))
                                 )
                        ),
                        numericInput("threshold", "显示基金会数目", 10, min = 1, max = 605),
                        width = 4
                          
                    ),
                      
                    mainPanel(
                      tabsetPanel(
                        id = 'dataset',
                        tabPanel('TopFunds', DT::dataTableOutput("funddata"))
                      )
                    )
            )
          ),
          
          tabPanel("基金会用户画像",

                   selectInput("fund", "基金会名称", c("全部基金会"="", structure(as.numeric(fund_image$Index), names=as.character(fund_image$FundName))), multiple=TRUE),

                   DT::dataTableOutput("fundimage")
          )
          
)

