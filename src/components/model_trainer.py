# Training the model

import os 
import sys 
from dataclasses import dataclass 

from catboost import CatBoostRegressor

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
)

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from sklearn.metrics import r2_score
from src.exception import CustomException
from src.logger import logging

from src.utils import save_object
from src.utils import evaluate_model


@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Splitting training and Test input data")
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                "Random Forest":RandomForestRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "AdaBoost":AdaBoostRegressor(),
                "Linear Regression":LinearRegression(),
                "KNN":KNeighborsRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "CatBoost":CatBoostRegressor(verbose=False),
                "XGBoost":XGBRegressor()
            }

            model_report:dict=evaluate_model(x_train,y_train,x_test,y_test,models)

            # to get best model
            best_model_score=max(sorted(model_report.values()))

            #To get best model name 
            best_model_name= list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]


            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            
            logging.info("Best found model on both training and training dataset")


            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(x_test)

            r2score=r2_score(y_test,predicted)
            return r2score
        
        
        except Exception as e:
            raise CustomException(e,sys)