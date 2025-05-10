
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Carregar o dataset vetorizado
df = pd.read_csv("../dataset/dataset_vetorizado.csv")

# Separar features e target
X = df.drop("is_top4", axis=1)
y = df["is_top4"]

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Avaliar o modelo
y_pred = clf.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print("Matriz de confusão:\n", confusion_matrix(y_test, y_pred))
print("Relatório de classificação:\n", classification_report(y_test, y_pred))

# Salvar modelo treinado
joblib.dump(clf, "random_forest_tft.pkl")
print("[OK] Modelo salvo como model/random_forest_tft.pkl")
