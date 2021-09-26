rm(list=ls())
library(dplyr)
library(curl)
library(tidyverse)
library(caret)
library(caTools)
library(C50)
library(ggplot2)
library(lattice)
library(caret)

df <- read.csv('C:/Users/shrey/Downloads/hackzurich_2021/month_agg.csv')
df <- df[-c(1)]
df[(df['A2_RSSI'] >= 2.0), 'A2_RSSI_1'] = "Excellent"
df[(df['A2_RSSI'] < 2.0) & (df['A2_RSSI'] >= 1.6), 'A2_RSSI_1'] = "Good"
df[(df['A2_RSSI'] < 1.6) & (df['A2_RSSI'] >= 1.2), 'A2_RSSI_1'] = "Fair"
df[(df['A2_RSSI'] < 1.2), 'A2_RSSI_1'] = "Weak"

df$A2_RSSI_1 <- as.factor(df$A2_RSSI_1)
write.csv(df,'tree_month_agg.csv')
summary(df)

df <- df[-c(5,6)] 
df$DisruptionCode <- as.factor(df$DisruptionCode)
df$EventCode <- as.factor(df$EventCode)
df$AreaNumber <- as.factor(df$AreaNumber)
df$DateTime <- as.Date(df$DateTime)
df$Track <- as.factor(df$AreaNumber)
levels(df$AreaNumber)
levels(df$Track)
summary(df)

split = sample.split(dataset$risk_factor, SplitRatio = 0.75)
training_set = subset(dataset, split == TRUE)
test_set = subset(dataset, split == FALSE)

nfolds <- 2
trControl <- trainControl(method  = "cv",
                          number  = nfolds)
fit <- train(form=risk_factor ~ .,
             data = training_set,
             method     = "C5.0",
             na.action = na.pass,
             trControl  = trControl,
             tuneLength = 2, #5
             control = C5.0Control(earlyStopping = FALSE),
             metric     = "Accuracy")

plot(fit)
saveRDS(fit, "train_track_file.rds")
summary(fit)

# Predicting the Test set results
y_pred = predict(my_model, newdata = test_set) #test_set is the csv file consisting of the variables without the final prediction
summary(y_pred) #prediction made by the machine learning model

# Making the Confusion Matrix
cm = table(test_set[,6], y_pred)
cm

confusionMatrix(cm)
plot(my_model)