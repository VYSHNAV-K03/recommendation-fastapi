from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder,LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from model import Autoencoder,build_ncf_model
from data import get_product_data, get_user_data, get_user_item_data,add_product,add_user
import os

app = FastAPI()

# Allow frontend origin
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or use ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

product_data = get_product_data()
product_data= pd.DataFrame(product_data)
user_data = get_user_data()
user_item_data = get_user_item_data()

# base pydantic model for request body
class RecommendationRequest(BaseModel):
    user_id: int
    item_id: int


def preprocess_content_data():
    content_df = pd.DataFrame(product_data, columns=['item_id', 'name', 'category', 'price', 'brand', 'rating', 'image_url'])

    categorical_columns = ['category', 'brand']
    numeric_columns = ['price', 'rating']

    # One-Hot Encoding for categorical columns
    encoder = OneHotEncoder(sparse_output=False)
    encoded_data = encoder.fit_transform(content_df[categorical_columns])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(categorical_columns))

    # Normalize numeric features
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(content_df[numeric_columns])
    scaled_df = pd.DataFrame(scaled_data, columns=numeric_columns)

    # Combine all features
    content_features = pd.concat([scaled_df, encoded_df], axis=1)
    content_features['item_id'] = content_df['item_id']

    return content_features, content_df  # also return the processed product_data

content_features, product_df = preprocess_content_data()

def content_based_recommendation(item_id: int, top_n: int = 2):
    item_row = product_df[product_df['item_id'] == item_id]
    if item_row.empty:
        raise HTTPException(status_code=404, detail="Item not found")

    # Get category of the item
    item_category = item_row.iloc[0]['category']

    # Filter both product_df and content_features for same category
    same_category_ids = product_df[product_df['category'] == item_category]['item_id']
    filtered_features = content_features[content_features['item_id'].isin(same_category_ids)]

    # Get item vector
    item_vector = filtered_features[filtered_features['item_id'] == item_id].drop('item_id', axis=1).values
    all_vectors = filtered_features.drop('item_id', axis=1).values

    # Calculate cosine similarity
    similarities = cosine_similarity(item_vector, all_vectors)[0]

    # Get top-N similar items
    indices = np.argsort(similarities)[::-1][1:top_n + 1]
    recommended_ids = filtered_features.iloc[indices]['item_id'].tolist()

    # Fetch details
    recommended_items = product_df[product_df['item_id'].isin(recommended_ids)][['item_id', 'name', 'image_url', 'price']]
    return recommended_items.to_dict(orient='records')

# Collaborative Filtering with Autoencoder
# Creates a matrix with users as rows, items as columns, and ratings as values.
user_item_matrix = user_item_data.pivot(index='user_id', columns='item_id', values='rating').fillna(0)
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(user_item_matrix)
print(scaled_data.shape[1])

# Gets the number of items (columns) — i.e., how many items each user is rating.
input_dim = scaled_data.shape[1]
autoencoder = Autoencoder(input_dim=input_dim)
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.fit(scaled_data, scaled_data, epochs=50, batch_size=2, verbose=0)

def collaborative_recommendation(user_id: int, top_n: int = 3):
    try:
        user_index = user_item_matrix.index.get_loc(user_id)
        user_data = scaled_data[user_index].reshape(1, -1)
        print(scaled_data[user_index].shape)
        print(user_data.shape)
        predictions = autoencoder(user_data).numpy()[0]
        top_indices = np.argsort(predictions)[::-1][:top_n]
        recommended_items = user_item_matrix.columns[top_indices].tolist()
        recommended_items_data = product_data[product_data['item_id'].isin(recommended_items)][['item_id', 'name', 'image_url', 'price']]
        return recommended_items_data.to_dict(orient='records')
    except KeyError:
        return []


def age_based_recommendation(user_id: int, top_n: int = 4):
    # Get current user's age
    current_user = user_data[user_data['user_id'] == user_id]
    if current_user.empty:
        raise HTTPException(status_code=404, detail="User not found")

    user_age = current_user.iloc[0]['age']

    # Find users with similar age (±5 years)
    similar_users = user_data[
        (user_data['age'] >= user_age - 5) & 
        (user_data['age'] <= user_age + 5) &
        (user_data['user_id'] != user_id)
    ]['user_id'].tolist()

    if not similar_users:
        return []

    # Get highly-rated items (rating >= 4) by similar users
    high_rated_items = user_item_data[
        (user_item_data['user_id'].isin(similar_users)) &
        (user_item_data['rating'] >= 4)
    ]['item_id'].value_counts().head(top_n).index.tolist()

    # Filter out items already rated by the current user
    rated_by_user = user_item_data[user_item_data['user_id'] == user_id]['item_id'].tolist()
    final_items = [item for item in high_rated_items if item not in rated_by_user]

    # Get item details
    recommended_items = product_data[product_data['item_id'].isin(final_items)][['item_id', 'name', 'image_url', 'price']]
    return recommended_items.to_dict(orient='records')


# Encode user and item IDs
user_encoder = LabelEncoder()
item_encoder = LabelEncoder()

user_item_data['user'] = user_encoder.fit_transform(user_item_data['user_id'])
user_item_data['item'] = item_encoder.fit_transform(user_item_data['item_id'])

num_users = user_item_data['user'].nunique()
num_items = user_item_data['item'].nunique()

ncf_model = build_ncf_model(num_users, num_items)

X = [user_item_data['user'].values, user_item_data['item'].values]
y = user_item_data['rating'].values

ncf_model.fit(X, y, epochs=20, batch_size=4, verbose=0)


def ncf_recommendation(user_id: int, top_n: int = 2):
    if user_id not in user_data['user_id'].values:
        return []

    user_idx = user_encoder.transform([user_id])[0]

    # Get all item indices
    all_item_ids = product_data['item_id'].values
    all_item_indices = item_encoder.transform(all_item_ids)

    # Prepare input
    user_input = np.full_like(all_item_indices, user_idx)
    predictions = ncf_model.predict([user_input, all_item_indices], verbose=0).flatten()

    # Exclude already rated items
    rated_items = user_item_data[user_item_data['user_id'] == user_id]['item_id'].values
    unrated_mask = ~np.isin(all_item_ids, rated_items)

    recommended_indices = np.argsort(predictions[unrated_mask])[::-1][:top_n]
    recommended_items = all_item_ids[unrated_mask][recommended_indices]

    return product_data[product_data['item_id'].isin(recommended_items)][['item_id', 'name', 'image_url']].to_dict(orient='records')


class Product(BaseModel):
    item_id: int
    name: str
    category: str
    price: float
    brand: str
    rating: float
    image_url: str

class User(BaseModel):
    user_id: int
    name: str
    age: int
    location: str

@app.post("/add_product")
def create_product(product: Product):
    result = add_product(product.dict())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    os.utime("main.py", None) 
    return result

@app.post("/add_user")
def create_user(user: User):
    result = add_user(user.dict())
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    os.utime("main.py", None)
    return result

@app.get('/items/{item_id}')
def get_item(item_id: int):
    
    item = product_data[product_data['item_id'] == item_id].to_dict(orient='records')
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item[0]

@app.get('/users/{user_id}')
def get_user(user_id: int):
    user = user_data[user_data['user_id'] == user_id].to_dict(orient='records')
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user[0]

@app.get('/items')
def get_all_items():
    return product_data.to_dict(orient='records')

@app.get('/users')
def get_all_users():
    return user_data.to_dict(orient='records')


@app.post('/recommend/content-based')
def recommend_content(request: RecommendationRequest):
    return {"recommendations": content_based_recommendation(request.item_id)}

@app.post('/recommend/collaborative')
def recommend_collaborative(request: RecommendationRequest):
    return {"recommendations": collaborative_recommendation(request.user_id)}

@app.post('/recommend/hybrid')
def hybrid_collab_age_recommendation(request: RecommendationRequest):
    print("userid",request.user_id)
    collab_recs = collaborative_recommendation(request.user_id)
    print(collab_recs)
    age_recs = age_based_recommendation(request.user_id)
    print(age_recs)
    combined = {item['item_id']: item for item in collab_recs + age_recs}
    return {"recommendations": list(combined.values())}

@app.post('/recommend/mixed')
def recommend_mixed(request: RecommendationRequest):
    
    content_recs = content_based_recommendation(request.item_id)
    collab_recs = collaborative_recommendation(request.user_id)
    combined_recs = {item['item_id']: item for item in content_recs + collab_recs}
    return {"recommendations": list(combined_recs.values())}

@app.post('/recommend/ncf')
def recommend_ncf(request: RecommendationRequest):
    return {"recommendations": ncf_recommendation(request.user_id)}


if __name__ == "__main__":  
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
