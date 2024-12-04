from gradio_client import Client, handle_file
from huggingface_hub import login


client = Client("AltarAI1/colqwen-embedding-api", hf_token="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")
result = client.predict(
		text="what glasses to wear",
		api_name="/predict"
)


result = client.predict(
		image=handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
		api_name="/predict_1"
)

print(result)