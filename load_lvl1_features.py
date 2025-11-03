import pandas as pd

classID_dict = pd.read_csv(r"Data\charater_creation_data\Class_List.tsv", sep="\t")


def get_features(class_id):
	chosen_class = classID_dict.loc[classID_dict["id"] == class_id] #gets the row with the chosen class
		
	class_name = chosen_class["class"].iloc[0]

	feature_filepath = fr"Data\charater_creation_data\Level1_Features\{class_name}.tsv"
	features = pd.read_csv(feature_filepath, sep="\t")

	return features


def display_features_lvl1(features):
	names_list = []
	features_list = []

	for row in features.itertuples():
		names_list.append(row.name)
			
		description = row.description
        # Split by hyphens that indicate bullet points and reformat
		description = description.replace(' - ', '\n- ')  # Add line breaks before each bullet
		description = description.replace('.   ', '.<br><br>')
		features_list.append(description)
	
	list_len = len(names_list)

	return names_list,features_list,list_len


