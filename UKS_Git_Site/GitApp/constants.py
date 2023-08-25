
from .models import Label



def create_default_labels():
  label_names = ["bug","documentation","duplicate","enhancement","good first issue","help wanted","invalid","question","wontfix"]
  label_colors = ["#d73a4a","#0075ca","#cfd3d7","#a2eeef","#7057ff","#008672","#e4e669","#d876e3","#ffffff"]
  default_labels = []

  for i in range(0,len(label_names)):
      default_labels.append(Label(id=i+1, name = label_names[i],description = "", color = label_colors[i]))
  return default_labels