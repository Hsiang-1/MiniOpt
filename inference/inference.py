from transformers import AutoModelForCausalLM, AutoTokenizer
from prompts.rl_prompt import SYSTEM_PROMPT


model_name = ""    # your post-training model path

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# first case of nl4opt_test.jsonl
question = """There has been an oil spill in the ocean and ducks need to be taken to shore to be cleaned either by boat or by canoe. A boat can take 10 ducks per trip while a canoe can take 8 ducks per trip. Since the boats are motor powered, they take 20 minutes per trip while the canoes take 40 minutes per trip. In order to avoid further environmental damage, there can be at most 12 boat trips and at least 60% of the trips should be by canoe. If at least 300 ducks need to be taken to shore, how many of each transportation method should be used to minimize the total amount of time needed to transport the ducks?"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": question},
    {"role": "assistant", "content": "<think>"}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=16384
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(response)