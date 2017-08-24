install.packages('rsconnect')
library(rsconnect)
rsconnect::setAccountInfo(name='lucao', token='9DA02DCBF2BF733FEB3EFE582EAB43C8', secret='k++s4fxW/aX6ejktuaipIQaM5nYHmL/63OFDMkVV')
setwd('C:/Users/LuCao/Desktop/Fund_Hackathon/Shiny/My_Shiny/my_app/fundhackathon_app')
options(encoding = 'UTF-8')
rsconnect::deployApp()

