## Resources
The code and overleaf document is at the link below

|Name| URL|
|-|-|
|Code |https://github.com/adibMosharrof/wgw_extension |
|Overleaf|https://www.overleaf.com/project/62222cc5221483c56962e98f|

## CodeBase
The code has the following parts
- Predict Object Distribution
- Predict Nlcd Coarse Labels

### Dataset
CVUSA flickr and streetview images have been used in this project.

### Environment
The project has been written in python $3.9.5$  and the python environment can be created using the environment.yml file.

### Sh files
There are some .sh files in the project which can be used to run some of the modules in the project. 
- build_object_dataset.sh
- obj_dist.sh
- build_nlcd_dataset.sh
- nlcd.sh

## Object distribution dataset
Using off the shelf object detection library from pytorch, I created an object distribution dataset on the CVUSA dataset. The dataset is a csv file which has the following columns

```csv
aerial_path, latitude, longitude, person, bicycle, car .... (50 MS coco classes)

```
The columns that are MS Coco classes contain a number which indicates the number of objects of that category in the streetview/flickr image at that location

## Predicting object distributions using aerial images

Next a classification model has been trained on the object distribution dataset, which takes in as input an aerial image and predicts the frequency of object distributions.  Poisson distribution has been used here to predict the object counts

## CVUSA NLCD labels
A cvusa nlcd dataset has been created, which is a csv file that contains the following columns
```csv
aerial_path, latitude, longitude, nlcd_labels, nlcd_coarse_labels
```

## NLCD Coarse Label Prediction
Created a baseline model to predict the nlcd coarse label of a location given the aerial image. 
Another model has been created where the weights are initialized using the model that was trained to predict object distributions.


## Results of NLCD Coarse Label Prediction

Graphs of loss/accuracy of predicting the nlcd coarse labels on the full dataset is below

Pink = Weights initialized with Poisson distribution task
Orange = No pretraining

### Training Details
epochs 10
batch size 500 (pink)
batch size 450 (orange)
num_workers 8

It takes around 1 hour to finish 1 epoch on the full dataset. 
All the data is loaded from localdisk1 in gyrfalcon. 

### Observations
From the graphs below, we can observe that the pretraining helps in classifying the nlcd coarse labels. With pretraining, there is a higher accuracy from a much earlier step, similarly there is a smaller loss value at early steps. As the models are trained for more epochs, both of them seem to come closer.
### Train

#### Train accuracy
![Train Accuracy](images_readme/train_acc.svg)

#### Train Loss
![Train Loss](images_readme/train_loss.svg)

### Validation
#### Val accuracy
![Val Accuracy](images_readme/val_acc.svg)

#### Val Loss
![Val Loss](images_readme/val_loss.svg)

