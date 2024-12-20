from PearsonCorrelation import PearsonCorrelation
from CosineSimilarity import ItemBasedFilter

print(PearsonCorrelation.predict_for_user("1"))
print(ItemBasedFilter.getRecommendations("1"))

