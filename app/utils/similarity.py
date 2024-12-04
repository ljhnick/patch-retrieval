import numpy as np

def late_interaction(data_emb, query_emb, aggregation="max"):
    data_emb = np.array(data_emb)  # Shape: (n, 128)
    query_emb = np.array(query_emb)  # Shape: (m, 128)

    if data_emb.shape[1] != 128 or query_emb.shape[1] != 128:
        raise ValueError("Embedding dimensions must be 128.")

    interaction_scores = np.dot(query_emb, data_emb.T)

    if aggregation == "sum":
        final_scores = np.sum(interaction_scores, axis=1)
    elif aggregation == "max":
        final_scores = np.max(interaction_scores, axis=1)
    else:
        raise ValueError("Unsupported aggregation method. Use 'sum' or 'max'.")

    final_score = np.sum(final_scores)
    return final_score
