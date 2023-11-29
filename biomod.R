library(biomod2)
library(sp)
library(raster)

ext.1<-extent(-8, 52, 36, 61) 
bio.15 <- getData('worldclim',var='bio',res=2.5) 
bio.15<-crop(bio.15,ext.1) 
bio.15<-stack(bio.15)

bio.70<-getData('CMIP5',var='bio',res=2.5,rcp=85,model='AC',year=70)
bio.70<-crop(bio.70,ext.1)
bio.70<-stack(bio.70)
names(bio.70)<-names(bio.15)