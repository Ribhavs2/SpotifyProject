import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np

#from refresh import Refresh

class Analysis:
    def __init__(self):
        self.df = pd.DataFrame()
        self.df_train = pd.DataFrame()
        self.df_test = pd.DataFrame()
        self.training_model = pd.DataFrame()
        self.fpr = []
        self.tpr = []
        self.auc = 0
    

    def load_dataframes(self):

        print("----------------------------------------")
        print("Loading Dataframes...")

        df_gym = pd.read_csv('gym.csv')
        df_gym["Include"] = 1

        df_hindi = pd.read_csv("hindi.csv")
        df_hindi["Include"] = 0
      

        df_night = pd.read_csv("night.csv")
        df_night["Include"] = 0
    

        df_sleep = pd.read_csv('sleep.csv')
        df_sleep["Include"] = 0
        

        df_spark = pd.read_csv('spark.csv')
        df_spark["Include"] = 0

        df_collect = [df_gym, df_hindi, df_night, df_sleep, df_spark]
        self.df = pd.concat(df_collect, ignore_index=True)
        self.df = self.df[self.df["time_signature"] != 1]
        self.df = self.df[self.df["key"] != -1]
        self.df = self.df.dropna()
        self.df = self.df.drop_duplicates(subset = ['id'])

        print("Dataframes Loaded")
    

    def build_model(self):
        print("--------------------------------------")
        print("Building Model...")

        self.df_train, self.df_test = train_test_split(self.df, test_size=0.20, random_state=123)

        # Using mod2_train to train model
        print("Using mod2_train to train model...")
        self.training_model = smf.logit(formula = 'Include ~ danceability + loudness + speechiness + acousticness', data = self.df_train).fit()
        
        print("Model built using danceability + loudness + speechiness + acousticness")
        print("Model summary:")
        print(self.training_model.summary())
    
    def testing_model(self):
        print("------------------------------------")
        print("Testing Model...")

        self.df_test['phat_test'] = self.training_model.predict(exog=dict(self.df_test))   

        self.fpr, self.tpr, score = roc_curve(y_true=self.df_test['Include'], y_score=self.df_test['phat_test'])
        self.auc= roc_auc_score(y_true=self.df_test['Include'], y_score=self.df_test['phat_test']) 

        print("Report:")
        print("LLF Value:", self.training_model.llf)
        print("AIC Score:", self.training_model.aic)
        print("BIC Score:", self.training_model.bic)

        #self.plot_roc()

    
    
    def plot_roc(self, lw=2):
        plt.plot(self.fpr, self.tpr, color='darkorange', lw=lw,
                label='ROC curve (area = '+str(np.round(self.auc,3))+')')
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend(loc="lower right")
        plt.show()

    
    def tpr_fpr_thresh(self, threshold):
        yhat = 1*(self.df_test["phat_test"] >= threshold)
        tn, fp, fn, tp = confusion_matrix(y_true=self.df_test["Include"], y_pred=yhat).ravel()
        tpr = tp / (fn + tp)
        fpr = fp / (fp + tn)

        return pd.DataFrame({'threshold': [threshold],
                             'tpr': [tpr],
                             'fpr': [fpr]})
    
    def print_thresholds(self):
        for thresh in np.arange(0,1,0.01):
            print(self.tpr_fpr_thresh(thresh))


analysis_obj1 = Analysis()
analysis_obj1.load_dataframes()
analysis_obj1.build_model()
analysis_obj1.testing_model()
analysis_obj1.print_thresholds()

training_model = analysis_obj1.training_model
threshold = 0.9999





           
        

        
        

    
    

