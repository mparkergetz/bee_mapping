library(biomod2)
library(sp)
library(raster)


setwd("/home/mpgetz/repos/bee_mapping/")

my_data <- read.csv("points.csv")
head(my_data)
my_data$X <- NULL

my_data$presence <- rep(1, nrow(my_data))

head(my_data)
coordinates(my_data) <- ~lon + lat

head(my_data)
str(my_data)

setwd("data/wc2.1_30s_bio")
tiff_files <- list.files(pattern = "\\.tif$", full.names = TRUE)

env_rasters <- list()
for (file in tiff_files) {
  raster_name <- basename(file)
  env_rasters[[raster_name]] <- raster(file)
}
env_stack <- stack(env_rasters)

formatted_data <- BIOMOD_FormatingData(
  resp.var = my_data,
  expl.var = env_stack,
  resp.xy = my_data,
  resp.name = 'presence',
  PA.nb.absences = 100000
)


# # Example: Modeling
# myBiomodModelOut <- BIOMOD_Modeling(
#   myBiomodData,
#   models = c('GLM', 'RF', 'MaxEnt'), # Choose the models you want to use
#   models.options = myBiomodModelOptions,
#   NbRunEval = 1,
#   DataSplit = 70,
#   VarImport = 0,
#   models.eval.meth = c('TSS', 'ROC')
# )
