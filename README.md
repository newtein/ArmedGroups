# ArmedGroups

Step-1: Data Creation (dir: /)
Feature Engineering and obtaining NAG_DETAILS_*.csv file. Note, this file would contain all the designed features from the NAGs dataset. The machine learning model will take this file as the input. 

Filename (Modulename): Description
make_data.py (MakeData) --> Primary file for feature engineering. It depends on the following files.
DeprivationScore.py (DeprivationModule) --> Calculates deprivation scores.
nag_support_network.py (NAGSupportNetwork) --> Calculates network science metrics.
conditional_probability.py (IdeologicalProbabilityModule) --> Calulates probabilistic trends in ideology. 
conditional_prob_obj.py (ObjectiveProbabilityModule) --> Calulates probabilistic trends in objective.
battle_related_deaths.py (BRDModule) --> calculates time taken to commit BRDs. 
get_longevity.py (LongevityModule) --> calculates lifespan. 

Step-2: Descriptive Analyses (dir: git_status/)

Filename: Description
Analysis0.ipynb: File to create boxplots. 
Ananlysis2_deprivation_caluclation and Analysis3_deprivation_plot: File to plot most avaiable and least available supports (Fig. 2)
geoCoding.ipynb: Geocoding for figure 3.
Analysis_Identities: To plot figure 4.
correlations.ipynb: To plot figure 6.
BRD.ipynb: File to correlate BRD features.

Step-3: Association Analysis (dir: /association analysis)
Filename: Description
data_modelling_v1_missing_values.ipynb --> imputing missing values
data_modelling_v2_hyperparameter_tunity --> Hyperparameter tunity
data_modelling_v2_shap --> SHAP analysis









