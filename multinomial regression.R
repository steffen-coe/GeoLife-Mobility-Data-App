setwd("C:/Users/ekino/Downloads/")
toy1 <- read.csv("full_geolife+weather.csv", header=TRUE)

# minimum trip time = 2.5 min, maximum trip time = 5 hours
df <- subset(data.frame(toy1), (toy1$time_total < 18000) & (toy1$time_total > 150))

modes <- as.factor(df$label)

num_modes <- recode(df$label, "walk" = 0, "bike" = 1, "bus" = 2, "subway" = 3, "taxi" = 4, "car" = 5)

date <- df$date
day <- as.factor(df$Converted_Start_Day)
start_hour <- as.factor(df$Converted_Start_Hour)
end_hour <- as.factor(df$Converted_End_Hour)
avg_vel <- df$vel_avg
total_dist <- df$distanceTotal
total_time <- as.numeric(df$time_total)
temp <- df$temp
rain <- df$precip
windspeed <- df$windspeed
humidity <- df$humidity
cloudcover <- df$cloudcover
# conditions <- as.factor(df$conditions)
hcr <- df$hcr # heading change rate: ratio btwn number of GPS points where a user changes direction with an angle > threshold 
              #and the total distance of the route
vcr <- df$vcr # velocity change rate: ratio btwn the number of GPS points with speed variation
              # above a certain threshold per unit of distance and the total distance of the route
npoints <- df$npoints # do not group walk/bike with this
sr <- df$sr # stop rate: ratio between the number of GPS points below a certain speed threshold per unit of distance and the total 
            # distance of the route... do not group walk/bike

## Visualizations
library(ggplot2)
ggplot(data=df, aes(x=label, y=sr,fill=label)) + geom_boxplot() + ylim(0,0.1) + xlab("mode") + ylab("stop rate")

ggplot(data=df, aes(x=label, y=hcr, fill=label)) + geom_boxplot() + ylim(0, 0.3) + xlab("mode") + ylab("heading change rate")

ggplot(data=df, aes(x=label, y=vcr, fill=label)) + geom_boxplot() + ylim(0,0.3) + xlab("mode") + ylab("velocity change rate")

ggplot(data=df, aes(x=label, y=npoints, fill=label)) + geom_boxplot() + ylim(0,2000) + xlab("mode") + ylab("number of observations")


X <- data.frame(day, start_hour, end_hour, avg_vel, total_dist, 
                total_time, temp, rain, windspeed, humidity, cloudcover, hcr, vcr, npoints, sr)

Y <- modes
#levels(Y) <- c("bike/walk", "bus/subway", "car/taxi", "bus/subway", "car/taxi", "bike/walk") # MOST SIMPLE
#levels(Y) <- c("walk/bike", "bus", "car/taxi", "subway", "car/taxi", "walk/bike") # MEDIUM COMPLEXITY
levels(Y) <- c("bike", "bus", "car", "subway", "taxi", "walk") # MOST COMPLEX
#levels(Y) <- c("bike", "bus", "car/taxi", "subway", "car/taxi", "walk") # Medium-high complexity

levels(X$day) <- c("Weekday", "Weekday", "Weekend", "Weekend", "Weekday", "Weekday", "Weekday")
#levels(X$day) <- c(5, 1, 6, 7, 4, 2, 3)
#X$day <- as.numeric(X$day)

levels(X$start_hour) <- c("off", "off", "off", "off", "off", "off","off","work","work","work","work","work","work","work","work","work","work","work","work","off","off","off","off","off")
# levels(X$start_hour) <- c(0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,0,0,0,0,0)
# X$start_hour <- as.numeric(X$start_hour)

levels(X$end_hour) <- c("off", "off", "off", "off", "off", "off","off","work","work","work","work","work","work","work","work","work","work","work","work","off","off","off","off","off")
# levels(X$end_hour) <- c(0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1,0,0,0,0,0)
# X$end_hour <- as.numeric(X$end_hour)

data <- data.frame(Y,X)
str(data)

#Correlation Tests
cor.test(num_modes, temp) # sig
cor.test(num_modes, humidity) # sig
cor.test(num_modes, rain)
cor.test(num_modes, windspeed) # sig
cor.test(num_modes, cloudcover)
cor.test(num_modes, npoints) # sig
cor.test(num_modes, total_dist) # sig > correlation too high
cor.test(num_modes, total_time)

day_T <- recode(df$Converted_Start_Day, "Monday" = 0, "Tuesday" = 1, "Wednesday" = 2, 
                "Thursday" = 3, "Friday" = 4, "Saturday" = 5, "Sunday" = 6)
cor.test(num_modes, day_T)

hour_s <- recode(X$start_hour, "off" = 0, "work" = 1)
cor.test(num_modes, hour_s) # sig
cor.test(num_modes, as.numeric(X$start_hour))

hour_e <- recode(X$end_hour, "off" = 0, "work" = 1)
cor.test(num_modes, hour_e) # sig
cor.test(num_modes, as.numeric(X$end_hour))

cor.test(num_modes, avg_vel) #sig > correlation too high
cor.test(num_modes, sr) #sig > correlation too high
cor.test(num_modes, vcr) #sig > correlation too high
cor.test(num_modes, hcr) #sig > correlation too high

#Correlation heat map
min_max_norm <- function(x) {
  (x - min(x)) / (max(x) - min(x))
}

data_norm <- as.data.frame(lapply(data[5:16], min_max_norm))

head(data_norm)

cor_matrix <- cor(data[5:16], method="spearman")

get_upper_tri <- function(cormat){
  cormat[lower.tri(cormat)]<- NA
  return(cormat)
}

upp <- get_upper_tri(cor_matrix)

library(reshape2)
melted_cormat <- melt(upp)

library(ggplot2)
ggplot(data = melted_cormat, aes(Var2, Var1, fill = value))+
  geom_tile(color = "white")+
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0, limit = c(-1,1), space = "Lab", 
                       name="Pearson\nCorrelation") +
  theme_minimal()+ 
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 12, hjust = 1))+
  coord_fixed()

summary(data[5:16]) # summary statistics
library(xtable)
xtable(summary(subset(data[5:16], select = -c(temp, rain, windspeed, humidity, cloudcover))))

# PCA
pca <- prcomp(data_norm, scale=TRUE)
print(pca)
summary(pca)
plot(pca)

# Create training data (70% of original dataset)
set.seed(5346)
train.ix <- sample(nrow(data),floor( nrow(data)) * 0.7 )
data.train <- data[train.ix,]
# Create testing data (30% of original dataset)
data.test <- data[-train.ix,]

trainX <- data.train[,-1]
rownames(trainX) = NULL
testX <- data.test[,-1]
rownames(testX) = NULL
trainY <- data.train[,1]
testY <- data.test[,1]

# LASSO
library(glmnet)
fit = glmnet(subset(trainX[,], select = -c(hcr, vcr, sr, avg_vel)), trainY, nlambda = 100, family = "multinomial")
fit2 = glmnet(trainX[,4:15],trainY, nlambda = 100, family = "multinomial") #plot without avg_vel

library(plotmo)
plot_glmnet(fit2, nresponse=4) #Full LASSO
plot_glmnet(fit, nresponse=4) # LASSO minus most important variables

# MLM: retrospective prediction
library(nnet)
mlogit <- multinom(Y ~ as.numeric(start_hour) + as.numeric(end_hour) + as.numeric(day) + temp + rain + cloudcover + windspeed + humidity, data = data.train, MaxNWts = 20000, maxit = 500)
summary(mlogit)
exp(coef(mlogit)) #odds ratios

library(VGAM) # not preferred due to high computation time + long summary table
m2logit <- vglm(Y ~ ., family = multinomial(), data = data.train)
summary(m2logit)

# MLM: future prediction
require(nnet)
m3logit <- multinom(Y ~ day + start_hour + end_hour + temp + rain + windspeed + humidity + cloudcover, data = data.train, MaxNWts = 20000, maxit = 500)
summary(m3logit)
exp(coef(m3logit))

library(caret)
mostimpvars <- varImp(mlogit) # including retrospective variables (vel, dist, time)
mostimpvars$Variables <- row.names(mostimpvars)
rownames(mostimpvars) = NULL
mostimpvars <- mostimpvars[order(-mostimpvars$Overall),]
mostimpvars

mostimpvars_f <- varImp(m3logit) # for future prediction
mostimpvars_f$Variables <- row.names(mostimpvars_f)
rownames(mostimpvars_f) = NULL
mostimpvars_f <- mostimpvars_f[order(-mostimpvars_f$Overall),]
mostimpvars_f

# Predict using MLM: retrospective prediction
preds <- predict(mlogit, type="class", newdata=subset(testX, select=-c(avg_vel, total_dist, total_time, hcr, vcr, sr, npoints)))
postResample(testY, preds)
summary(preds)

# Predict using MLM: future prediction
preds2 <- predict(m3logit, type="class", newdata=subset(testX, select=-c(avg_vel, total_dist, total_time, hcr, vcr, sr, npoints)))
postResample(testY, preds2)
summary(preds2)


totalAccuracy <- c()
maxit <- 500
cv <- 10
cvDivider <- floor(nrow(data) / (cv + 1))

for (cv in seq(1:cv)) {
  # assign chunk to data test
  dataTestIndex <- c((cv * cvDivider):(cv * cvDivider + cvDivider))
  dataTest <- data[dataTestIndex,]
  # everything else to train
  dataTrain <- data[-dataTestIndex,]
  
  require(nnet)
  mlogit_cv <- multinom(Y ~ ., data=dataTrain, maxit=maxit, trace=T) 
  
  pred_cv <- predict(mlogit_cv, newdata=dataTest, type="class")
  
  #  classification error
  require(caret)
  cv_ac <- postResample(dataTest$Y, pred_cv)[[1]]
  print(paste('Current Accuracy:',cv_ac,'for CV:',cv))
  totalAccuracy <- c(totalAccuracy, cv_ac)
}

mean(totalAccuracy)

#CV for future prediction (exclude sr, vcr, hcr, avg_vel)
totalAccuracy3 <- c()
maxit <- 500
cv <- 10
cvDivider <- floor(nrow(data) / (cv + 1))

for (cv in seq(1:cv)) {
  # assign chunk to data test
  dataTestIndex <- c((cv * cvDivider):(cv * cvDivider + cvDivider))
  dataTest <- data[dataTestIndex,]
  # everything else to train
  dataTrain <- data[-dataTestIndex,]
  
  require(nnet)
  m3logit_cv <- multinom(Y ~ day + start_hour + end_hour + temp + rain + windspeed + humidity + cloudcover, data=dataTrain, maxit=maxit, trace=T) 
  
  pred3_cv <- predict(m3logit_cv, newdata=dataTest, type="class")
  
  #  classification error
  require(caret)
  cv_ac3 <- postResample(dataTest$Y, pred3_cv)[[1]]
  print(paste('Current Accuracy:',cv_ac3,'for CV:',cv))
  totalAccuracy3 <- c(totalAccuracy3, cv_ac3)
}

mean(totalAccuracy3)



