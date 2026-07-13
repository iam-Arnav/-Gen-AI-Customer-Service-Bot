CONCEPTS = {
    "machine learning": {
        "Supervised Learning": [
            "Linear Regression",
            "Logistic Regression",
            "Decision Trees",
            "SVM"
        ],
        "Unsupervised Learning": [
            "K-Means",
            "DBSCAN",
            "PCA"
        ],
        "Deep Learning": [
            "CNN",
            "RNN",
            "Transformers"
        ]
    },

    "transformer": {
        "Architecture": [
            "Encoder",
            "Decoder"
        ],
        "Core Components": [
            "Self Attention",
            "Multi Head Attention",
            "Positional Encoding",
            "Feed Forward Network",
            "Layer Normalization"
        ]
    },

    "cnn": {
        "Layers": [
            "Convolution",
            "Pooling",
            "ReLU",
            "Fully Connected"
        ]
    },

    "bert": {
        "Components": [
            "Transformer Encoder",
            "Masked Language Model",
            "Token Embeddings",
            "Position Embeddings"
        ]
    },

    "reinforcement learning": {
        "Elements": [
            "Agent",
            "Environment",
            "Reward",
            "Policy",
            "Value Function"
        ]
    }
}


def get_concept_tree(name):

    key = name.lower().strip()

    return CONCEPTS.get(key)