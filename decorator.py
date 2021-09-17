from time import sleep

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from jump.pipeline import Pipeline

pipeline = Pipeline(name="logistic_regression_training")


@pipeline.node
def load_data():
    x, y = load_iris(return_X_y=True)
    x_train, x_valid, y_train, y_valid = train_test_split(
        x, y, train_size=0.8, stratify=y
    )
    # artificially create bottleneck
    sleep(1.23)
    return x_train, y_train, x_valid, y_valid


@pipeline.node
def normalize_data(x_train, y_train, x_valid, y_valid):
    scaler = StandardScaler().fit(x_train)
    x_train = scaler.transform(x_train)
    x_valid = scaler.transform(x_valid)
    return (x_train, y_train, x_valid, y_valid)


@pipeline.node
def init_model():
    return LogisticRegression()


@pipeline.node
def train_model(model, x_train, y_train):
    model.fit(x_train, y_train)
    return model


@pipeline.node
def evaluate_model(model, x_valid, y_valid):
    acc = accuracy_score(model.predict(x_valid), y_valid)
    return acc


# Invoking a series of function calls will construct the pipeline behind the scene
x_train, y_train, x_valid, y_valid = normalize_data(*load_data())
model = init_model()
model = train_model(model, x_train, y_train)
acc = evaluate_model(model, x_valid, y_valid)
print("Validation accuracy: ", acc.val)

pipeline.visualize()



