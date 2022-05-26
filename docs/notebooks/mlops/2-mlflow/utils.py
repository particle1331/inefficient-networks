import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from toolz import compose


def add_pickup_dropoff_pair(df):
    """Add product of pickup and dropoff locations."""
    
    df['PU_DO'] = df['PULocationID'].astype(str) + '_' + df['DOLocationID'].astype(str)
    return df


def preprocess_dataset(filename, transforms, categorical, numerical):
    """Return processed features dict and target."""
    
    # Load dataset
    df = pd.read_parquet(filename)

    # Add target column; filter outliers
    df['duration'] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    # Apply in-between transformations
    df = compose(*transforms[::-1])(df)

    # For dict vectorizer: int = ignored, str = one-hot
    df[categorical] = df[categorical].astype(str)

    # Convert dataframe to feature dictionaries
    feature_dicts = df[categorical + numerical].to_dict(orient='records')
    target = df.duration.values

    return feature_dicts, target


def plot_duration_distribution(model, X_train, y_train, X_valid, y_valid):
    """Plot true and prediction distribution."""
    
    fig, ax = plt.subplots(1, 2, figsize=(8, 3))

    sns.histplot(model.predict(X_train), ax=ax[0], label='pred', color='C0', stat='density', kde=True)
    sns.histplot(y_train, ax=ax[0], label='true', color='C1', stat='density', kde=True)
    ax[0].set_title("Train")
    ax[0].legend();

    sns.histplot(model.predict(X_valid), ax=ax[1], label='pred', color='C0', stat='density', kde=True)
    sns.histplot(y_valid, ax=ax[1], label='true', color='C1', stat='density', kde=True)
    ax[1].set_title("Valid")
    ax[1].legend();

    fig.tight_layout()
    return fig
