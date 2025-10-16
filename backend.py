# model_stub.py
"""
if not image_url:
return 0.0
url_low = image_url.lower()
if any(k in url_low for k in ['smile', 'happy', 'sunny', 'bright']):
return 0.5
if any(k in url_low for k in ['cry', 'sad', 'dark', 'gloom']):
return -0.5
return 0.0




def fuse_scores(text_score: float, image_score: float, network_influence: float) -> dict:
"""Simple fusion: weighted sum where network_influence acts as a weight modifier.


Returns raw fused score in [-1,1] and probability-like scores for categories.
"""
# base weights
w_text = 0.6
w_image = 0.2
w_network = 0.2


# if network influence high, give more weight to network signals (here we treat influence as amplifying negativity)
w_network = w_network * (0.5 + network_influence)


fused = (w_text * text_score) + (w_image * image_score) + (w_network * (0.2 * text_score))
# clamp
fused = max(-1.0, min(1.0, fused))


# map to categorical probabilities (simple soft mapping)
prob_normal = max(0.0, 1.0 - abs(fused))
prob_stressed = max(0.0, min(1.0, 0.5 * max(0, -fused) + 0.3 * network_influence))
prob_depressed = max(0.0, min(1.0, 0.6 * max(0, -fused) + 0.4 * network_influence))
prob_anxious = max(0.0, min(1.0, 0.4 * max(0, -fused) + 0.3 * (1 - abs(text_score))))


# normalize
s = prob_normal + prob_stressed + prob_depressed + prob_anxious
if s <= 0:
probs = {'normal': 1.0, 'stressed': 0.0, 'depressed': 0.0, 'anxious': 0.0}
else:
probs = {k: v / s for k, v in [('normal', prob_normal), ('stressed', prob_stressed), ('depressed', prob_depressed), ('anxious', prob_anxious)]}


# pick category
category = max(probs.items(), key=lambda x: x[1])[0]


return {
'fused_score': fused,
'probs': probs,
'category': category,
'text_score': text_score,
'image_score': image_score,
'network_influence': network_influence
}