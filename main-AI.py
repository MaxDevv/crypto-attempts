import polars as pl
import tensorflow as tf
import numpy as np

# df = pl.read_csv("historical-price-data/ETH_1min.csv")
# moneroPrices = df.get_column("Open")[3_000_000:4_000_000][::60]
with open("historical-price-data/ethereum-descending-chrongraphical", "r") as f:
    moneroPrices = [float(i) for i in f.read().split("\n") if i != ""]


def prepare_data(prices, sequence_length=3):
    X, y = [], []
    for i in range(len(prices) - sequence_length):
        X.append(prices[i:i+sequence_length])
        y.append(1 if prices[i+sequence_length] > prices[i+sequence_length-1] else 0)
    return np.array(X), np.array(y)

# Prepare data
X, y = prepare_data(moneroPrices)
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Normalize data
mean = X_train.mean()
std = X_train.std()
X_train = (X_train - mean) / std
X_test = (X_test - mean) / std
# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(3,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Create checkpoint callback
checkpoint_path = "training_checkpoints/cp.weights.h5"
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    save_weights_only=True,
    save_best_only=True,
    monitor='val_loss',
    verbose=1
)

# Train model with checkpoint callback
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1, callbacks=[checkpoint_callback])

# load already trained model
model.load_weights("training_checkpoints/cp.weights.h5")


# Save the entire model
# model.save('saved_model.h5')



def simulate_ai(initial_balance=100):
    balance = initial_balance
    investment = 0
    
    for i in range(len(moneroPrices)-3):
        current_sequence = np.array([(moneroPrices[i:i+3] - mean) / std])
        prediction = model.predict(current_sequence, verbose=0)[0][0]
        
        current_price = moneroPrices[i+2]
        
        if prediction < 0.5:  # Predict price will go down
            toInvest = 5  # Use fixed values from best performing previous simulation
            if balance >= toInvest:
                investment += (toInvest/current_price)
                balance -= toInvest
        else:  # Predict price will go up
            toWithdraw = 5
            if investment >= (toWithdraw/current_price):
                balance += toWithdraw
                investment -= (toWithdraw/current_price)
        
        if i % 50 == 0:
            print(f"Step {i}: Balance: {balance + (investment * current_price)}, Investment: {investment}, Prediction: {prediction}")
    
    final_price = moneroPrices[-1]
    final_balance = balance + (investment * final_price)
    return final_balance

# Test the AI trading strategy
final_result = simulate_ai()
print(f"Final Balance with AI strategy: {final_result}")